from osc_lib import utils

from config.manager import Manager

DEFAULT_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'config'
API_VERSIONS = {
    '1': 'config.plugin'
}
API_VERSION_OPTION = 'os_config_api_version'


# Required by the OSC plugin interface
def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """
    plugin_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    client = plugin_client()
    return client


# Required by the OSC plugin interface
def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """

    # this hack changes the default value for the --os-cloud ArgumentParser action
    # somehow setting OS_CLOUD is being ignored; maybe this code is too late for that
    for action in parser._actions:
        if action.dest == 'cloud':
            action.default = Manager.get_current_context(fail_silently=True)

    return parser
