from distutils.dir_util import copy_tree

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
