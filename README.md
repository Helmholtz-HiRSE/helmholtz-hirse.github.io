# HiRSE Website

<https://www.helmholtz-hirse.de/>

## Getting the code

Our repository is

    <https://github.com/Helmholtz-HiRSE/helmholtz-hirse.github.io> 

Follow these steps to fork the repository and get the code:

    <https://docs.github.com/en/get-started/quickstart/fork-a-repo>

## First steps

Enter the repository folder and create a branch:

    git checkout -b <YOUR_BRANCH>

### Install Dependencies

The website is build with the static site generator [jekyll](https://jekyllrb.com/). To install it on your system see the [documentation](https://jekyllrb.com/docs/installation/).

After the installation of jekyll some other things are needed. In the repository folder do

    bundle install

As an alternative of installing dependencies on your system, you can use the jekyll docker image

    docker pull jekyll/jekyll

### Local development

To automatically refresh the page with each change you make to the source files:

   bundle exec jekyll serve --livereload

Check your results by loading <http://localhost:4000/>.

### Local development - the docker way

Local development with docker

Jekyll can be run inside a docker container:

    docker run --rm \
    --volume="$PWD:/srv/jekyll:Z" \
    --publish [::1]:4000:4000 \
    jekyll/jekyll \
    jekyll serve

Jekyll will recognize them and rebuild the site.
Check your results by reloading <http://localhost:4000/>.
Livereload is not possible.

Should you prefer the root-less approach via podman, try

    podman run --rm \
    --volume="$PWD:/srv/jekyll:Z" \
    --publish [::1]:4000:4000 \
    -e JEKYLL_ROOTLESS=1 \
    docker.io/jekyll/jekyll \
    jekyll serve

### What to find where

The overview pages are markdown files in the main folder.
All subpages are organized in subfolders:

    ├──assets       --> place for images
    ├──_events      --> pages for events
    ├──_codes       --> pages for codes

All other files and folders are for structure and design of the page.

### Create a pull request

After you are happy with your changes, push the changes into your fork

    git push origin <YOUR_BRANCH> 

and create a pull request as described here:

<https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork>
