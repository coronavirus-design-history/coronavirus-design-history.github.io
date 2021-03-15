# Placeholder

This is not ready yet

## Software developers

If you are a software developer and want to run a local copy, first install Python 3 and Pip3, then follow these instructions:

```
git clone [THIS REPOSITORY] digital-design-history
cd digital-design-history
python3 -m venv env
source env/bin/activate
make web
```

To serve the site locally:

```
python3 -m http.server --directory docs
```

### Publishing online

This tools is designed to be published on GitHub Pages. There is a GitHub Action that generates the site and copies it to a separate branch (gh-pages) on commit. You will need to enable Github Pages for that branch in the settings of your repository.


### Tools and scripts

* `python3 -m generate .` will generate the static website
* `python3 -m website.tools updatetimestamp` will update the `updated` attribute in datapackage.json based on the latest edit in the `data/` directory.
* `pytest` will run unit tests
