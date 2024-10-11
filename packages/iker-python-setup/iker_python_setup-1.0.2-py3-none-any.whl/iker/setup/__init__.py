import importlib.metadata
import os

try:
    __version__ = importlib.metadata.version("iker-python-setup")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "version_string_local",
    "version_string_scm",
    "version_string",
    "setup",
]


def read_version_tuple(cwd: str | None = None,
                       *,
                       default: (int, int, int) = (0, 0, 0),
                       version_file: str = "VERSION",
                       patch_env_var: str = "BUILD_NUMBER",
                       strict: bool = False) -> (int, int, int):
    if cwd is None:
        cwd = os.getcwd()
    try:
        with open(os.path.join(cwd, version_file)) as fh:
            major_str, minor_str, *patch_strs = fh.read().strip().split(".")

        major = max(0, int(major_str))
        minor = max(0, int(minor_str))

        patch_str = patch_strs[0] if len(patch_strs) > 0 else os.getenv(patch_env_var)
        patch = 0 if patch_str is None else min(999999, max(0, int(patch_str)))

        return major, minor, patch
    except Exception as e:
        if strict:
            raise e
    return default


def version_string_local(cwd: str | None = None) -> str:
    major, minor, patch = read_version_tuple(cwd, strict=True)
    return f"{major}.{minor}.{patch}"


def version_string_scm(cwd: str | None = None) -> str:
    from setuptools_scm import ScmVersion
    from setuptools_scm import get_version
    if cwd is None:
        cwd = os.getcwd()

    def find_scm_root(cd: str) -> str:
        cd = os.path.abspath(cd)
        for item in os.listdir(cd):
            if os.path.isdir(os.path.join(cd, item)) and item == ".git":
                return cd
        pd = os.path.dirname(cd)
        if pd == cd:
            raise ValueError("Cannot find SCM root properly")
        return find_scm_root(pd)

    def version_scheme_callback(scm_version: ScmVersion) -> str:
        major, minor, patch = read_version_tuple(cwd, strict=True)
        if scm_version.branch == "master" or os.getenv("GIT_BRANCH", "") == "master":
            return f"{major}.{minor}.{patch}"
        return f"{major}.{minor}.{0}"

    def local_scheme_callback(scm_version: ScmVersion) -> str:
        if scm_version.branch == "master" or os.getenv("GIT_BRANCH", "") == "master":
            return ""
        node_datetime = scm_version.time.strftime("%Y%m%d%H%M%S")
        if scm_version.dirty:
            return scm_version.format_with("+{node_datetime}.{node}.dirty", node_datetime=node_datetime)
        return scm_version.format_with("+{node_datetime}.{node}", node_datetime=node_datetime)

    return get_version(root=find_scm_root(cwd),
                       version_scheme=version_scheme_callback,
                       local_scheme=local_scheme_callback,
                       normalize=True)


def version_string(cwd: str | None = None):
    try:
        return version_string_scm(cwd)
    except Exception:
        return version_string_local(cwd)


def setup():
    from setuptools import setup
    setup(version=version_string())
