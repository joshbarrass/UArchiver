import importlib, os

from udl.Base import KernelBase
from udl.utils import strip_http

_IGNORED_FILES = ["__pycache__", "__init__.py"]

_current_dir = os.path.abspath(os.path.dirname(__file__))

_kernel_dir = os.path.join(_current_dir, "kernels")

# create the dir if possible
if not os.path.exists(_kernel_dir):
    os.mkdir(_kernel_dir)
if not os.path.isdir(_kernel_dir):
    raise FileExistsError(
        "Directory '{}' is already a file".format(_kernel_dir)
    )

def load_kernels(kernel_dir=None):
    if kernel_dir is None:
        kernel_dir = _kernel_dir

    # list all the files in the kernel dir
    _kernel_files = [
        f for f in os.listdir(kernel_dir)
        if f not in _IGNORED_FILES and f[-1] != "~"
    ]

    # determine which files are valid kernels
    kernels = {}
    for _f in _kernel_files:
        _abspath = os.path.join(kernel_dir, _f)
        # must be either a .py file or a directory to be imported
        if os.path.splitext(_f)[-1].lower(
        ) != ".py" and not os.path.isdir(_abspath):
            continue
        # import the kernel file/package
        _imported_kernel = importlib.import_module(
            "udl.kernels." + os.path.splitext(_f)[0]
        )
        # try to access the Kernel class
        try:
            # ensure the kernel inherits from KernelBase
            if KernelBase in _imported_kernel.Kernel.__bases__:
                _domains = _imported_kernel.Kernel.DOMAINS
        except AttributeError:
            # kernel did not contain a Kernel class -- ignore
            continue
        # add the kernel to each of the domains it supports
        for _domain in _domains:
            _domain = strip_http(_domain)
            if _domain not in kernels:
                kernels[_domain] = [_imported_kernel.Kernel]
            else:
                kernels[_domain].append(_imported_kernel.Kernel)

    return kernels
