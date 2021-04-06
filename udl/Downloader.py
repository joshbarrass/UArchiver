import datetime
import fnmatch
import tempfile
import os
import sys
from urllib.parse import urlparse
import traceback

import udl.errors
from udl.Loader import load_kernels
from udl.utils import strip_http, copy_dir_content, rmdir_or_warn
from udl import returncodes

def download(url, outdir=None, *args):
    """Download the URL with any matching kernels until the download
succeeds."""
    # generate an output directory based on the domain name and
    # current time
    if outdir is None:
        outdir = urlparse(url).netloc + datetime.datetime.now(
        ).strftime("_%Y%m%d%H%M%S")

    outdir = os.path.abspath(outdir)

    # check if the directory exists and make it if necessary
    if not os.path.exists(outdir):
        # get the mode of the parent dir for matching
        mode = os.stat(
            os.path.abspath(os.path.join(outdir, ".."))
        ).st_mode
        # want to match mode
        umask = os.umask(0)
        os.mkdir(outdir, mode=mode)
        os.umask(umask)
    elif not os.path.isdir(outdir):
        raise FileExistsError
    else:
        # get the mode of the output dir for matching
        mode = os.stat(os.path.abspath(outdir)).st_mode

    # load the kernels
    kernels = load_kernels()

    # set a temporary exit code for "not run anything yet"
    exit_code = -1

    # strip http/s if it exists
    to_match = strip_http(url)

    # store the current working directory
    original_cwd = os.path.abspath(os.getcwd())

    # loop through domains and lists of kernels
    for domain, ks in kernels.items():
        # if the domain matches the pattern...
        if fnmatch.fnmatch(to_match, domain):
            # ...loop through the available kernels for this domain
            for k in ks:
                # change to the original cwd before using the kernel
                os.chdir(original_cwd)

                # try using the kernel -- if a keyboard interrupt
                # occurs, raise it further, otherwise just specify
                # that the kernel failed
                try:
                    # create new kernel
                    kernel = k()

                    # create the temporary directories for the kernel
                    # to work in
                    with tempfile.TemporaryDirectory() as tempdir:
                        with tempfile.TemporaryDirectory() as dldir:
                            if kernel.ALLOW_UMASKING:
                                umasked = True
                                # make umask match mode
                                umask = os.umask(~mode & 0o777)
                            else:
                                umasked = False
                            # attempt to download
                            exit_code = kernel.download(
                                url, tempdir, dldir, *args
                            )
                            if umasked:
                                os.umask(umask)
                            # check that files were actually written
                            if len(os.listdir(dldir)) == 0:
                                exit_code = returncodes.NOTHING_DOWNLOADED
                            # if download is successful, copy the
                            # files to the real output dir
                            if exit_code == returncodes.SUCCESS:
                                # TODO: move, not copy
                                copy_dir_content(dldir, outdir)
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except Exception as e:
                    exit_code = returncodes.FAIL
                    print(
                        "Warning: error occurred in kernel:\n{}"
                        .format(e),
                        file=sys.stderr
                    )
                    print("Displaying traceback")
                    print("-" * 20)
                    traceback.print_exc()
                    print("-" * 20)
                    continue

        # if the exit code is a success, end the loop now
                if exit_code == returncodes.SUCCESS:
                    break
        if exit_code == returncodes.SUCCESS:
            break

    # change back to the original working directory
    os.chdir(original_cwd)

    if exit_code != returncodes.SUCCESS:
        rmdir_or_warn(outdir)
        if exit_code == -1:
            raise udl.errors.NoMatchingKernelError(
                "No kernels matched the url"
            )
        raise udl.errors.NoWorkingKernelError(
            "No kernels were able to download the file"
        )
