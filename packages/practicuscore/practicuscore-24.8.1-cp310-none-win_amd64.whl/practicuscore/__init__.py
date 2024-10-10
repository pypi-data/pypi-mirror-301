"""
Practicus AI Core Library
=========================

Overview
--------
Practicus AI Core library allows you to work on DataFrames, Practicus AI Workers and more.

Sample Usage
------------
import practicuscore as prt
prt.some_operation()
"""
from .log_manager import get_logger, Log, set_logging_level
from .region_manager import regions
from .engine_helper import engines
from .experiment_helper import experiments
from .workflow_helper import workflows
from .model_helper import models
from .app_helper import apps
from .notebook_helper import notebooks
from .cli import main


__version__ = '24.8.1'
logger = get_logger(Log.SDK)


def _add_region_methods_to_globals():
    # For convenience. Allows: prt.current_region() instead of prt.regions.current_region()
    try:
        import inspect

        def is_cython_function(obj):
            return callable(obj) and (inspect.isfunction(obj) or obj.__class__.__name__ == 'cython_function_or_method')

        _region_methods = {}
        for name, method in inspect.getmembers(regions, predicate=is_cython_function):
            if not name.startswith("_"):
                _region_methods[name] = method

        globals().update(_region_methods)
    except:
        logger.error(
            "Could not add regions methods to globals for convenience. Please use them as prt.regions.  ",
            exc_info=True)


_add_region_methods_to_globals()


def trust_local_certificates():
    try:
        from .core_conf import core_conf_glbl
        if core_conf_glbl.network__trust_local_certificates:
            logger.debug("Trusting SSL certificates in local OS store.")
            import truststore
            truststore.inject_into_ssl()
    except:
        logger.error("Could not trust local operating system certificate store. "
                     "Your private Certificate Authority (CA) certs might not work.", exc_info=True)


trust_local_certificates()


if __name__ == "__main__":
    main()
