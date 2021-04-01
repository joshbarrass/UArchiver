import os

import youtube_dl

from udl.Base import KernelBase
import udl.returncodes as returncodes

class Kernel(KernelBase):
    DOMAINS = ["youtube.com/watch*", "www.youtube.com/watch*"]

    def download(self, url, tempdir, outdir, *args):
        os.chdir(outdir)
        ytdl = youtube_dl.YoutubeDL({"format": "bestvideo+bestaudio"})
        ytdl.download([url])

        return returncodes.SUCCESS
