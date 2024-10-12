import os
import sys
from typing import Optional

from ..prodigy_teams_pam_sdk.recipe_utils import AnyProps, Props

APP_NAME = "prodigy-teams-recipes"
CYGWIN = sys.platform.startswith("cygwin")
MSYS2 = sys.platform.startswith("win") and ("GCC" in sys.version)
# Determine local App Engine environment, per Google's own suggestion
APP_ENGINE = "APPENGINE_RUNTIME" in os.environ and "Development/" in os.environ.get(
    "SERVER_SOFTWARE", ""
)
WIN = sys.platform.startswith("win") and not APP_ENGINE and not MSYS2


def merge_props(x: Optional[AnyProps], y: Optional[AnyProps]) -> AnyProps:
    """Merge two sets of field props."""
    if x is None and y is None:
        return Props()
    elif x is None:
        assert y is not None
        return y.copy()
    elif y is None:
        assert x is not None
        return x.copy()
    else:
        x_ = x.dict(exclude_defaults=True)
        y_ = y.dict(exclude_defaults=True)
        for key in y_.keys():
            if key not in x_:
                x_[key] = getattr(y, key)
        output = x.__class__(**x_)
        return output


# Source: https://github.com/pallets/click/blob/cba52fa76135af2edf46c154203b47106f898eb3/src/click/utils.py#L408
def get_app_dir(
    app_name: str = APP_NAME, roaming: bool = True, force_posix: bool = False
) -> str:
    """
    Returns the config folder for the application.  The default behavior
    is to return whatever is most appropriate for the operating system.
    """
    # TODO: separate the user configuration from the cache and use appdirs.py paths

    def _posixify(name: str) -> str:
        return "-".join(name.split()).lower()

    def _get_sys_platform() -> str:
        # This is dumb but the linter complains that code is unreachable
        # if we use the literal value
        return sys.platform

    if WIN:
        key = "APPDATA" if roaming else "LOCALAPPDATA"
        folder = os.environ.get(key)
        if folder is None:
            folder = os.path.expanduser("~")
        return os.path.join(folder, app_name)
    if force_posix:
        return os.path.join(os.path.expanduser(f"~/.{_posixify(app_name)}"))
    if _get_sys_platform() == "darwin":
        return os.path.join(
            os.path.expanduser("~/Library/Application Support"), app_name
        )
    return os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        _posixify(app_name),
    )
