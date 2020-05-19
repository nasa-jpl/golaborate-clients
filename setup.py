"""HTTP client library for NKT SuperK lasers based on go-hcit."""

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(use_scm_version=False)
