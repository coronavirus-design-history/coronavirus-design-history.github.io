import os
import pathlib
import shutil
import fire
import sass
import staticjinja
import yaml

from datetime import datetime

from pynpm import NPMPackage

from website.filters import formatdatestring
from website.readers import read_markdown
from website.renderers import render_markdown


class StaticSite:

    @staticmethod
    def generate(working_dir):
        """Generate pages for a static site"""

        try:
            # get path to output directory
            base_dir = pathlib.Path(working_dir).absolute()
            site_dir = os.path.join(base_dir, "docs")

            # clear output directory
            for file in os.scandir(site_dir):
                if os.path.isdir(file.path):
                    shutil.rmtree(file.path)
                elif file.name != ".gitkeep":
                    os.remove(file.path)

            # create temp directory for assembling site
            temp_dir = os.path.join(base_dir, "_temp")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            current_dir = pathlib.Path(__file__).absolute().parent
            site_source_dir = os.path.join(current_dir, "site")
            shutil.copytree(site_source_dir, temp_dir)
            shutil.copy(
                os.path.join(current_dir, "package.json"),
                os.path.join(temp_dir, "package.json"),
            )

            # compile any scss (copy assets to _assets, then run compile)
            assets = os.path.join(temp_dir, "assets")
            if os.path.exists(assets):

                # install npm packages
                npm = NPMPackage(assets)
                npm.install()

                # create temporary duplicate of the assets dir
                _assets = os.path.join(temp_dir, "_assets")
                shutil.copytree(assets, _assets)
                shutil.rmtree(assets)

                # compile assets
                sass.compile(
                    dirname=(_assets, assets),
                    output_style="compressed",
                    include_paths=[temp_dir],
                )

                # tidy up
                shutil.rmtree(_assets)
                shutil.rmtree(os.path.join(temp_dir, "node_modules"))
                os.remove(os.path.join(temp_dir, "package.json"))
                os.remove(os.path.join(temp_dir, "package-lock.json"))


            config = yaml.safe_load(open(os.path.join(current_dir, "_config.yaml")))
            data = {
                "config": config,
                "generated_at": datetime.now(),
            }
            # Override of base url from config
            if os.getenv("BASE_URL", False):
                data["config"]["base_url"] = os.getenv("BASE_URL")

            # Generate and render web view
            web = staticjinja.Site.make_site(
                searchpath=temp_dir,
                outpath=site_dir,
                contexts=[
                    (".*.md", read_markdown),
                ],
                rules=[
                    (".*.md", render_markdown),
                ],
                encoding="utf8",
                followlinks=False,
                extensions=None,
                staticpaths=["example.csv"],
                env_globals=data,
                env_kwargs={"trim_blocks": True, "lstrip_blocks": True},
                mergecontexts=False,
                filters={"formatdatestring": lambda s: formatdatestring(s)},
            )
            web.render()
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)


if __name__ == "__main__":
    fire.Fire(StaticSite)
