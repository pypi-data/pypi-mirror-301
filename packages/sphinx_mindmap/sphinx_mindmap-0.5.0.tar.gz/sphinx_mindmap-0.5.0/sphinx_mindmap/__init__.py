import re
import sphinx
from os import makedirs, path
import shutil
from sphinx.util import logging
from sphinx.errors import ExtensionError
from docutils.nodes import Element, Node
from docutils import nodes
from docutils.parsers.rst import directives
from typing import Any
from sphinx.util.docutils import SphinxDirective

__version__ = "0.5.0"
__display_version__ = __version__

logger = logging.getLogger(__name__)

_ROOT_DIR = path.abspath(path.dirname(__file__))
_FILES1 = (
    (
        "vis-network",
        "",
    ),
    (
        "jquery",
        "",
    ),
)
_FILES2 = (
    (
        "mindmap.html",
        "",
    ),
)

static_directory = "_static"
target_directory = static_directory + "/sphinx_mindmap"


class sphinx_mindmap_ExtensionError(ExtensionError):
    pass


def copy_files_or_directories(app, files, dest):
    try:
        makedirs(path.join(app.outdir, target_directory), exist_ok=True)
        for filename, integrity in files:
            ifile = path.join(_ROOT_DIR, static_directory, filename)
            ofile = path.join(app.outdir, dest, filename)
            if path.isdir(ifile):
                if path.exists(ofile):
                    shutil.rmtree(ofile)
                shutil.copytree(ifile, ofile)
            elif path.isfile(ifile):
                shutil.copyfile(ifile, ofile)
    except shutil.Error as err:
        for src, dst, msg in err.args[0]:
            logger.critical(f"Error copying {src} to {dst}: {msg}")
        raise sphinx_mindmap_ExtensionError("Something went wrong in my extension")
    except OSError as err:
        logger.critical(f"Error: {err}")
        raise sphinx_mindmap_ExtensionError("Something went wrong in my extension")


def add_files(app, config):
    if sphinx.version_info[:2] >= (5, 0) and not getattr(
        app, "sphinx_mindmap_installed", False
    ):
        copy_files_or_directories(app, _FILES1, target_directory)
        copy_files_or_directories(app, _FILES2, static_directory)
        app.sphinx_mindmap_installed = True


def boolean_spec(argument: Any) -> bool:
    if argument == "true":
        return True
    elif argument == "false":
        return False
    else:
        raise ValueError("unexpected value. true or false expected")


class mindmap(SphinxDirective):
    """
    This directive renders a mind map defined in PlantUML format and
    visualizes it using the vis.js network library.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    # option_spec = {
    #     "page-index": directives.nonnegative_int,
    #     "page-name": directives.unchanged,
    #     "transparency": boolean_spec,
    #     "export-scale": directives.positive_int,
    #     "export-width": directives.positive_int,
    #     "export-height": directives.positive_int,
    # }

    def run(self) -> list[Node]:
        current_source = self.arguments[0]
        prefix = re.sub(r"^(\.\./)*.*", "\\1", current_source)
        current_sourcex = re.sub(r"^(\.\./)*", "", current_source).replace(
            prefix + static_directory, "."
        )
        iframe_html = f'<iframe src="{prefix}{static_directory}/mindmap.html?file={current_sourcex}&expanded=true&inc=17" width="100%" height="600px" frameBorder="0"></iframe>'
        iframe_node = nodes.raw("", iframe_html, format="html")
        return [iframe_node]


def setup(app):
    app.connect("config-inited", add_files)
    directives.register_directive("mindmap", mindmap)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }
