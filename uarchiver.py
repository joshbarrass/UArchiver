#!/usr/bin/env python3
"""Ultimate Archiver.

Usage:
  uarchiver [--directory=<dir>] <url>
  uarchiver -a [--directory=<dir>] <url>

  uarchiver (-h | --help)
  uarchiver --version

Options:

  -a --auto             Automatically determine downloader kernel (default).
  -d --directory=<dir>  Set output folder to <dir>.

"""

from docopt import docopt

from udl.Downloader import download

VERSION = "1.0-pre"

if __name__ == "__main__":
    args = docopt(__doc__, version=VERSION)

    outdir = None
    if args["--directory"]:
        outdir = args["--directory"]

    # select operation mode
    if args["--auto"]:
        download(args["<url>"], outdir=outdir)
    else:
        # no option specified -- default to auto
        download(args["<url>"], outdir=outdir)
