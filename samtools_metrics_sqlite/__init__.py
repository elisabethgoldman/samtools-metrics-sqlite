try:
    from samtools_metrics_sqlite._version import version

    __version__ = version
except ImportError:
    __version__ = '0'
