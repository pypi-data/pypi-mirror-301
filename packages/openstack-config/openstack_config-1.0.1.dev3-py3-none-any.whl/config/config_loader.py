import errno
import os

import platformdirs

# copied from openstack/config/loader.py

PLATFORMDIRS = platformdirs.PlatformDirs(
    'openstack', 'OpenStack', multipath='/etc'
)
CONFIG_HOME = PLATFORMDIRS.user_config_dir

# snaps do set $HOME to something like
# /home/$USER/snap/openstackclients/$SNAP_VERSION
# the real home (usually /home/$USERNAME) is stored in $SNAP_REAL_HOME
# see https://snapcraft.io/docs/environment-variables
SNAP_REAL_HOME = os.getenv('SNAP_REAL_HOME')
if SNAP_REAL_HOME:
    UNIX_CONFIG_HOME = os.path.join(
        os.path.join(SNAP_REAL_HOME, '.config'), 'openstack'
    )
else:
    UNIX_CONFIG_HOME = os.path.join(
        os.path.expanduser(os.path.join('~', '.config')), 'openstack'
    )
UNIX_SITE_CONFIG_HOME = '/etc/openstack'

SITE_CONFIG_HOME = PLATFORMDIRS.site_config_dir

CONFIG_SEARCH_PATH = [
    os.getcwd(),
    CONFIG_HOME,
    UNIX_CONFIG_HOME,
    SITE_CONFIG_HOME,
    UNIX_SITE_CONFIG_HOME,
]
YAML_SUFFIXES = ('.yaml', '.yml')
JSON_SUFFIXES = ('.json',)
CONFIG_FILES = [
    os.path.join(d, 'clouds' + s)
    for d in CONFIG_SEARCH_PATH
    for s in YAML_SUFFIXES + JSON_SUFFIXES
]


def get_config_path():
    for path in CONFIG_FILES:
        if os.path.exists(path):
            try:
                with open(path) as _:
                    return path
            except OSError as e:
                if e.errno == errno.EACCES:
                    # Can't access file so let's continue to the next
                    # file
                    continue
    return None
