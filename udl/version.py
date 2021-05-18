import subprocess

try:
    _project_version = subprocess.Popen(
        ["git", "describe", "--tags", "--long"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    ).communicate()[0].decode("utf-8").strip()

    if _project_version == "":
        _project_version = "0.0.0"

    _revision_count = subprocess.Popen(
        ["git", "log", "--oneline"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    ).communicate()[0].decode("utf-8").count("\n")

    VERSION = _project_version + "-" + str(_revision_count)

except FileNotFoundError:
    VERSION = "unknown"
