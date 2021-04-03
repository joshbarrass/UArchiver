import os
import sys
from distutils.dir_util import copy_tree
import cgi
import urllib.parse
from urllib.request import Request, urlopen, urlretrieve

def strip_http(url):
    """Strip http or https from the front of a url if it exists"""
    if url[:8].lower() == "https://":
        return url[8:]
    if url[:7].lower() == "http://":
        return url[7:]
    return url

def copy_dir_content(src_dir, dest_dir):
    """Move the contents of the source dir to the destination dir"""
    copy_tree(src_dir, dest_dir)

def rmdir_or_warn(directory):
    try:
        os.rmdir(directory)
    except OSError:
        print(
            "Warning: Failed to remove directory {}".format(directory),
            file=sys.stderr
        )

def download_original_name(url, outdir=".", useragent=None):
    """Download a file to a particular directory using the filename
provided by the server"""
    if useragent:
        req = Request(
            url, data=None, headers={
                "User-Agent": useragent,
            }
        )
    else:
        req = url

    # https://stackoverflow.com/a/49733575/7471232
    remotefile = urlopen(req)
    blah = remotefile.info()['Content-Disposition']
    if blah is not None:
        value, params = cgi.parse_header(blah)
        filename = params["filename"]
    else:
        filename = urllib.parse.unquote_plus(
            os.path.basename(remotefile.geturl())
        ).replace(" ", "_")
    urlretrieve(url, os.path.join(outdir, filename))
