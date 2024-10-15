from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("oqc-qcaas-client")
except PackageNotFoundError:
    __version__ = "unknown"
