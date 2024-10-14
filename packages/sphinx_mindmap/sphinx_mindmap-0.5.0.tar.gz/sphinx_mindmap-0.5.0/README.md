# sphinx_mindmap

## About

The sphinx_mindmap is a web application written in HTML, CSS, and JavaScript, provided as a Sphinx extension. It renders [plantuml mindmap](https://plantuml.com/mindmap-diagram) using [visjs network](https://visjs.github.io/vis-network/docs/network/). It was tested only with [sphinx_book_theme](https://pypi.org/project/sphinx-book-theme/)

## Goals and Realization

* Packaging and dependency management: [poetry](https://python-poetry.org/docs/basic-usage)
* Development: [vscode devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) 
* CI/CT using [github actions](https://docs.github.com/en/actions)
  * package generation 
  * documentation generation and deployment to github pages

## Installation

TBD  
You can install [sphinx_mindmap](https://pypi.org/project/sphinx_mindmap/) with pip

    pip install sphinx_mindmap

Alternatively (Linux)

    git clone https://github.com/mi-parkes/sphinx_mindmap.git
    cd sphinx_mindmap
    
	poetry install
	poetry build
    
    # you can then install the package in your virtual environment
    pip install dist/sphinx_mindmap*.whl

## Activation

In your conf.py configuration file, add `sphinx_mindmap` to your extensions list:

    extensions = [
      ...
      'sphinx_mindmap'
      ...
    ]
    ...

You can embedd a HTML frame with plantuml mindmap rendering by using the following directive in your .rst file(s)

    .. mindmap:: ../../_static/puml/sphinx_needs_data_explorer.puml

Current limitation: mindmaps can be stored only in `_static` directory or its subdirectories
