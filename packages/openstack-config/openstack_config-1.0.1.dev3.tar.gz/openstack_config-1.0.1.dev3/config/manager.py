import os

from ruamel.yaml import YAML

from config.config_loader import get_config_path, UNIX_CONFIG_HOME

CURRENT_CONTEXT_PATH = UNIX_CONFIG_HOME + '/context'

MISSING_CONFIG_ERROR = Exception("Config file is empty or does not exist")
INVALID_CONFIG_TYPE_ERROR = Exception("Can only work on YAML files, not JSON")
UNKNOWN_CONTEXT_ERROR = Exception("Config file does not contain the given context")


class Manager:
    def __init__(self):
        pass

    @staticmethod
    def get_config_filename():
        return get_config_path()

    @staticmethod
    def get_config():
        config_filename = Manager().get_config_filename()
        if config_filename is None:
            raise MISSING_CONFIG_ERROR

        if config_filename.endswith('json'):
            raise INVALID_CONFIG_TYPE_ERROR

        with open(config_filename) as f:
            yaml = YAML()
            code = yaml.load(f)

        return yaml, code

    @staticmethod
    def get_current_context(fail_silently=False):
        # warning: this method is called every time
        try:
            with open(CURRENT_CONTEXT_PATH, 'r') as f:
                current_context = str(f.readline()).strip()

                # we need to check for existence or the CLI will just error
                # and the user might not know why
                try:
                    _, config = Manager().get_config()
                    if current_context not in config.get('clouds', {}).keys():
                        return None
                except Exception as e:
                    if not fail_silently:
                        raise e
                    return None

                return current_context
        except IOError:
            return None

    @staticmethod
    def set_current_context(context):
        if context != 'none' and context not in Manager.get_context_names():
            raise UNKNOWN_CONTEXT_ERROR

        try:
            os.makedirs(UNIX_CONFIG_HOME, exist_ok=True)
        except OSError as e:
            raise e

        with open(CURRENT_CONTEXT_PATH, 'w') as f:
            f.write(context if context != 'none' else '')
            f.flush()

    @staticmethod
    def get_context_names():
        _, config = Manager.get_config()
        return config.get('clouds', {}).keys()

    @staticmethod
    def rename_context(current_context, new_context):
        if current_context not in Manager.get_context_names():
            raise UNKNOWN_CONTEXT_ERROR

        if new_context in Manager.get_context_names():
            raise Exception('Context already exists')

        is_current_context = current_context == Manager.get_current_context(fail_silently=True)

        yaml, code = Manager().get_config()
        code['clouds'][new_context] = code['clouds'].pop(current_context)
        Manager.write_config(yaml, code)

        # convenience: also change the current context, if affected
        if is_current_context:
            Manager.set_current_context(new_context)

    @staticmethod
    def delete_context(context):
        if context not in Manager.get_context_names():
            raise UNKNOWN_CONTEXT_ERROR

        is_current_context = context == Manager.get_current_context(fail_silently=True)

        yaml, code = Manager().get_config()
        del code['clouds'][context]
        Manager.write_config(yaml, code)

        # convenience: also change the current context, if affected
        if is_current_context:
            Manager.set_current_context('none')

    @staticmethod
    def write_config(yaml, code):
        with open(Manager().get_config_filename(), 'w') as f:
            yaml.dump(code, f)
            f.flush()
