from udl.errors import UnimplementedError

class KernelBase:
    # List of domains this kernel works for
    DOMAINS = []
    # Whether or not the os umask should be changed before download
    ALLOW_UMASKING = True

    def __init__(self):
        pass

    def download(self, url, tempdir, outdir, *args):
        """Download from a URL, with a given temp dir and output dir."""
        raise UnimplementedError(
            "Download for this kernel was not implemented"
        )
