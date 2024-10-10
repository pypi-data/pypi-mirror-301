from importlib.metadata import PackageNotFoundError, version

# add version information
__version__: str
"""Version info."""


def _get_version() -> str:
    """Get the current installed version of the package.

    Returns:
        str: "_unknown_" if the version metadata is missing (e.g. running from sources)
    """
    try:
        return version("colorevo")
    except PackageNotFoundError:
        # swtchd is not installed
        return "_unknown_"


__version__ = _get_version()
