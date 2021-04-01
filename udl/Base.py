from udl.errors import UnimplementedError

class KernelBase:
    DOMAINS = []

    def __init__(self):
        pass

    def download(self, url, tempdir, outdir, *args):
        """Download from a URL, with a given temp dir and output dir."""
        raise UnimplementedError(
            "Download for this kernel was not implemented"
        )
