 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Build & Test](https://github.com/michal2612/mkdocs-exclude-unused/actions/workflows/build.yml/badge.svg)
 ![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-exclude-unused)


# mkdocs-exclude-unused

A simple MkDocs plugin that automatically removes all .md files not included in the nav section of your mkdocs.yaml file.

## How to use

Simply add plugin to your mkdocs .yml file

```
plugins:
  - mkdocs-exclude-unused
```
## Example
In your mkdocs.yaml your nav section looks like this:

    nav:
      - Main: index.md
      - Page1: Page1.md

But in your docs folder you have:

    docs/
	    index.md
	    Page1.md
	    Page2.md

**Mkdocs will create .html file for each of .md file even if it's not mentioned in 'nav' section!**

Page2.md can be used in other mkdocs.yml files, or it may be required in the docs folder for other reasons.
After running `mkdocs build` or `mkdocs serve`, warnings will be generated if Page2.md is missing from the navigation, preventing you from building in `--strict` mode. This plugin solves the problem by removing unused pages.

