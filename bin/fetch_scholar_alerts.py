#!/usr/bin/env python3
"""
Fetch Google Scholar alert emails from Gmail and output their text content.

The script connects to Gmail via IMAP using an App Password, selects the
configured label (default: "RSE"), reads all unread messages, decodes any
Google Scholar redirect URLs embedded in the email bodies so that the
doi.org / arxiv.org URLs are exposed, and prints the combined text to
stdout.  The caller (typically the scholar_alerts workflow) pipes this
output into doi_to_bib.py --input.

Required environment variables:
    GMAIL_ADDRESS       Gmail address to log in with.
    GMAIL_APP_PASSWORD  App Password generated for that account.

Optional environment variables:
    GMAIL_LABEL         Gmail label to check (default: RSE).

After processing, unread messages are marked as read so they will not be
picked up again on the next run.
"""

import email
import email.message
import html
import imaplib
import os
import re
import sys
from email.header import decode_header, make_header
from urllib.parse import parse_qs, unquote, urlparse

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GMAIL_IMAP_HOST = 'imap.gmail.com'
GMAIL_IMAP_PORT = 993

_DEFAULT_LABEL = 'RSE'

# ---------------------------------------------------------------------------
# IMAP helpers
# ---------------------------------------------------------------------------


def connect(address: str, app_password: str) -> imaplib.IMAP4_SSL:
    """Open an authenticated IMAP-over-SSL connection to Gmail."""
    conn = imaplib.IMAP4_SSL(GMAIL_IMAP_HOST, GMAIL_IMAP_PORT)
    conn.login(address, app_password)
    return conn


def select_label(conn: imaplib.IMAP4_SSL, label: str) -> None:
    """Select a Gmail label as the active IMAP mailbox."""
    # Gmail exposes labels as IMAP folders; quote the name in case it
    # contains spaces or special characters.
    status, detail = conn.select(f'"{label}"')
    if status != 'OK':
        decoded = detail[0].decode(errors='replace') if detail else ''
        print(
            f"ERROR: Could not select Gmail label '{label}': {decoded}",
            file=sys.stderr,
        )
        sys.exit(1)


def fetch_unread_ids(conn: imaplib.IMAP4_SSL) -> list:
    """Return a list of message IDs (bytes) that are currently unseen."""
    status, data = conn.search(None, 'UNSEEN')
    if status != 'OK' or not data or not data[0]:
        return []
    return data[0].split()


def fetch_raw_message(conn: imaplib.IMAP4_SSL, msg_id: bytes) -> bytes | None:
    """Fetch the full RFC-822 bytes for a single message."""
    status, data = conn.fetch(msg_id, '(RFC822)')
    if status != 'OK' or not data or data[0] is None:
        return None
    return data[0][1]


def mark_as_read(conn: imaplib.IMAP4_SSL, msg_ids: list) -> None:
    """Set the \\Seen flag on all *msg_ids*."""
    if not msg_ids:
        return
    id_list = b','.join(msg_ids)
    conn.store(id_list, '+FLAGS', r'\Seen')


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------


def _decode_part(part: email.message.Message) -> str:
    """Decode a MIME part to a Unicode string."""
    payload = part.get_payload(decode=True)
    if payload is None:
        return ''
    charset = part.get_content_charset() or 'utf-8'
    return payload.decode(charset, errors='replace')


def extract_text(msg: email.message.Message) -> str:
    """
    Return all human-readable text from *msg*, including both plain-text
    and HTML parts.  HTML tags are stripped and HTML entities are unescaped
    so that embedded URLs are left in their natural form.
    """
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype in ('text/plain', 'text/html'):
                text = _decode_part(part)
                if ctype == 'text/html':
                    text = _strip_html(text)
                parts.append(text)
    else:
        text = _decode_part(msg)
        if msg.get_content_type() == 'text/html':
            text = _strip_html(text)
        parts.append(text)
    return '\n'.join(parts)


def _strip_html(raw: str) -> str:
    """
    Minimal HTML processing:

    1. Expand href attributes so the URLs appear in the plain text (they
       would otherwise be lost when tags are removed).
    2. Remove all remaining HTML tags.
    3. Unescape HTML entities.
    """
    # Expose href values before stripping tags so URL patterns still match
    raw = re.sub(
        r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>',
        lambda m: m.group(0) + ' ' + m.group(1) + ' ',
        raw,
        flags=re.IGNORECASE,
    )
    # Remove tags
    raw = re.sub(r'<[^>]+>', ' ', raw)
    # Unescape entities (&amp; → &, %xx in URLs, etc.)
    raw = html.unescape(raw)
    return raw


# ---------------------------------------------------------------------------
# Google Scholar redirect decoding
# ---------------------------------------------------------------------------

_SCHOLAR_REDIRECT = re.compile(
    r'https?://scholar\.google\.com/scholar_url\?[^\s<>"\']+',
    re.IGNORECASE,
)


def decode_scholar_redirects(text: str) -> str:
    """
    Google Scholar alert emails wrap article URLs in redirect URLs:

        https://scholar.google.com/scholar_url?url=https%3A%2F%2Fdoi.org%2F...

    Replace each such redirect with the decoded target URL so that the
    doi.org / arxiv.org patterns in doi_to_bib.py can match them.
    """

    def _replace(match: re.Match) -> str:
        redirect_url = html.unescape(match.group(0))
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)
        if 'url' in params:
            return unquote(params['url'][0])
        return redirect_url

    return _SCHOLAR_REDIRECT.sub(_replace, text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    address = os.environ.get('GMAIL_ADDRESS', '').strip()
    app_password = os.environ.get('GMAIL_APP_PASSWORD', '').strip()
    label = os.environ.get('GMAIL_LABEL', _DEFAULT_LABEL).strip()

    if not address or not app_password:
        print(
            'ERROR: Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD environment variables.',
            file=sys.stderr,
        )
        sys.exit(1)

    print(f'Connecting to Gmail ({address}) …', file=sys.stderr)
    conn = connect(address, app_password)

    print(f"Selecting label '{label}' …", file=sys.stderr)
    select_label(conn, label)

    msg_ids = fetch_unread_ids(conn)
    print(
        f"Found {len(msg_ids)} unread message(s) in label '{label}'.",
        file=sys.stderr,
    )

    if not msg_ids:
        conn.logout()
        return

    all_text: list[str] = []
    for msg_id in msg_ids:
        raw = fetch_raw_message(conn, msg_id)
        if raw is None:
            print(f'  WARNING: Could not fetch message {msg_id}.', file=sys.stderr)
            continue
        msg = email.message_from_bytes(raw)
        subject = str(make_header(decode_header(msg.get('Subject', ''))))
        print(f'  Processing: {subject}', file=sys.stderr)
        text = extract_text(msg)
        text = decode_scholar_redirects(text)
        all_text.append(text)

    mark_as_read(conn, msg_ids)
    print(f'Marked {len(msg_ids)} message(s) as read.', file=sys.stderr)

    conn.logout()

    # Print combined text to stdout — the workflow pipes this into doi_to_bib.py
    print('\n\n'.join(all_text))


if __name__ == '__main__':
    main()
