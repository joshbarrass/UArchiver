import os
import re

from udl.Base import KernelBase
import udl.returncodes as returncodes
from udl.utils import download_original_name

class Kernel(KernelBase):
    DOMAINS = [
        "www.thingiverse.com/thing:*", "thingiverse.com/thing:*"
    ]

    def __init__(self):
        super().__init__()
        self.matcher = re.compile(
            "^https?://www.thingiverse.com/thing:(\\d+)"
        )

    def download(self, url, tempdir, outdir, *args):
        # extract thing ID with regex
        match = self.matcher.match(url)
        if match is None:
            return returncodes.FAIL
        thing_ID = match.groups()[0]

        dl_url = "https://www.thingiverse.com/thing:{}/zip".format(
            thing_ID
        )

        download_original_name(dl_url, outdir)

        return returncodes.SUCCESS
