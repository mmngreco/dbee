from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import typer


def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
