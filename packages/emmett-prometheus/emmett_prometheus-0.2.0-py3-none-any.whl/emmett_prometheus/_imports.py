try:
    from emmett.__version__ import __version__

    _major, _minor, _ = __version__.split(".")
    if _major < 2 or (_major == 2 and _minor < 6):
        from .__version__ import __version__ as extver

        raise RuntimeError(f"Emmett-Prometheus {extver} requires Emmett >= 2.6.0")

    from emmett import request, response, websocket
except ImportError:
    from emmett55 import request, response, websocket
