# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

## 🧳 Prerequisites

- A working [Python](https://www.python.org/downloads/) environment.
- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- [uv](https://astral.sh/)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will need to create a new environment

Then run

```bash
git clone https://github.com/awesome-panel/panel-mermaid.git
cd panel-mermaid
uv pip install -e .[examples,dev,test]
```

You can run all tests via

```bash
ruff check
pytest tests
```

Please run this command and fix any failing tests if possible before you `git push`.

### 🚢 Release a new package on Pypi

Update the version in the [pyproject.toml](pyproject.toml).

Then run all tests as described above

Then you can build

```bash
uv build
```

and upload

```bash
uv publish --username awesome-panel
```

to release the package 📦. To upload to *Test Pypi* first, you can add the `--test` flag.