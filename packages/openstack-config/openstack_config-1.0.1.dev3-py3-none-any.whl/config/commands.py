import os

import requests
from glom import glom, PathAccessError
from openstackclient.identity.v3.project import ListProject
from osc_lib.command import command

from config.manager import Manager

GLUE_API_URL = "https://iam.apis.syseleven.de/v1"
GLOM_ERROR = "Check the actual config (openstack config view) or the glom syntax (https://glom.readthedocs.io/en/latest/tutorial.html)"
NO_ACTIVE_CONTEXT_ERROR = "Please activate a context via use-context first"


class CurrentContext(command.Command, Manager):
    """Display the current context"""

    auth_required = False

    def get_parser(self, prog_name):
        return super(CurrentContext, self).get_parser(prog_name)

    def take_action(self, parsed_args):
        print(self.get_current_context())


class UseContext(command.Command, Manager):
    """Set the current context for all operations (use none to reset)"""

    auth_required = False

    def get_parser(self, prog_name):
        parser = super(UseContext, self).get_parser(prog_name)
        contexts = set(self.get_context_names())
        contexts.add('none')
        parser.add_argument(
            'context',
            metavar='<context>',
            choices=contexts,
        )
        return parser

    def take_action(self, parsed_args):
        self.set_current_context(parsed_args.context)


class RenameContext(command.Command, Manager):
    """Rename a context from the clouds.yaml file"""

    auth_required = False

    def get_parser(self, prog_name):
        parser = super(RenameContext, self).get_parser(prog_name)
        parser.add_argument(
            'current_context',
            metavar='<current_context>',
            choices=self.get_context_names(),
        )
        parser.add_argument(
            'new_context',
            metavar='<new_context>',
        )
        return parser

    def take_action(self, parsed_args):
        self.rename_context(parsed_args.current_context, parsed_args.new_context)


class DeleteContext(command.Command, Manager):
    """Delete the specified context from the clouds.yaml"""

    auth_required = False

    def get_parser(self, prog_name):
        parser = super(DeleteContext, self).get_parser(prog_name)
        parser.add_argument(
            'context',
            metavar='<context>',
            choices=self.get_context_names(),
        )
        return parser

    def take_action(self, parsed_args):
        self.delete_context(parsed_args.context)


class GetContexts(command.Lister, Manager):
    """Describe one or many contexts"""

    auth_required = False

    def get_parser(self, prog_name):
        return super(GetContexts, self).get_parser(prog_name)

    def take_action(self, parsed_args):
        return (
            ['NAME'],
            [{v: v} for v in self.get_context_names()]
        )


class Set(command.Command, Manager):
    """Set an individual value in a clouds.yaml file"""

    auth_required = False

    def get_parser(self, prog_name):
        parser = super(Set, self).get_parser(prog_name)
        parser.add_argument(
            'property_name',
            metavar='<property_name>',
        )
        parser.add_argument(
            'property_value',
            metavar='<property_value>',
        )
        return parser

    def take_action(self, parsed_args):
        yaml, code = Manager().get_config()

        # this is just for checking the existence
        # will panic if target not found
        try:
            glom(code, parsed_args.property_name)
        except PathAccessError as e:
            print(e.get_message())
            print(GLOM_ERROR)
            return

        # we cant delete the result directly, so we have to resolve the parent item
        # and manually invoke del on the child element
        parent_spec = '.'.join(parsed_args.property_name.split('.')[0:-1])
        parent = glom(code, parent_spec)

        tmp = parsed_args.property_name.split('.')
        child_spec = tmp[len(tmp) - 1]

        if child_spec.isdigit():
            child_spec = int(child_spec)

        value = parsed_args.property_value
        if value.isdigit():
            value = int(value)
        elif value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False

        parent[child_spec] = value
        self.write_config(yaml, code)


class Unset(command.Command, Manager):
    """Unset an individual value in a clouds.yaml file"""

    auth_required = False

    def get_parser(self, prog_name):
        parser = super(Unset, self).get_parser(prog_name)
        parser.add_argument(
            'property_name',
            metavar='<property_name>',
        )
        return parser

    def take_action(self, parsed_args):
        yaml, code = Manager().get_config()

        # this is just for checking the existence
        # will panic if target not found
        try:
            glom(code, parsed_args.property_name)
        except PathAccessError as e:
            print(e.get_message())
            print(GLOM_ERROR)
            return

        # we cant delete the result directly, so we have to resolve the parent item
        # and manually invoke del on the child element
        parent_spec = '.'.join(parsed_args.property_name.split('.')[0:-1])
        parent = glom(code, parent_spec)

        tmp = parsed_args.property_name.split('.')
        child_spec = tmp[len(tmp) - 1]

        if child_spec.isdigit():
            child_spec = int(child_spec)

        del parent[child_spec]
        self.write_config(yaml, code)


class View(command.Command, Manager):
    """Display merged clouds.yaml settings or a specified clouds.yaml file"""

    auth_required = False

    def get_parser(self, prog_name):
        return super(View, self).get_parser(prog_name)

    def take_action(self, parsed_args):
        with open(self.get_config_filename()) as f:
            print(f.read())


class GetProjects(ListProject, Manager):
    _description = "List all projects that are currently accessible"

    def is_v3s11_auth(self):
        current_context = self.get_current_context(fail_silently=True)
        if current_context:
            _, code = self.get_config()
            if code['clouds'][current_context].get('auth_type', None) == 'v3s11':
                return True
        return False

    def get_parser(self, prog_name):
        if self.is_v3s11_auth():
            # let's omit all the fancy parameters we can't handle
            return command.Lister.get_parser(self, prog_name)

        return ListProject.get_parser(self, prog_name)

    def take_action(self, parsed_args):
        if self.is_v3s11_auth():
            # until this point, we did authenticate and can access the JWT cache
            token = GetProjects.get_cached_jwt()

            projects = []
            r = requests.get(f'{GLUE_API_URL}/orgs', headers={'Authorization': 'Bearer ' + token})
            if not r.ok:
                raise Exception(r.text)

            for org in r.json():
                r = requests.get(f"{GLUE_API_URL}/orgs/{org['id']}/projects",
                                 headers={'Authorization': 'Bearer ' + token})
                if not r.ok:
                    raise Exception(r.text)

                for project in r.json():
                    projects.append({
                        project['id']: project['id'],
                        project['name']: project['name'],
                        org['name']: org['name'],
                        ','.join(project['tags']): ','.join(project['tags'])
                    })

            return (
                ['ID', 'Name', 'Organization', 'Tags'],
                projects
            )

        return ListProject.take_action(self, parsed_args)

    @staticmethod
    def get_cached_jwt():
        path = os.path.join(os.path.expanduser(os.path.join('~', '.config')), 'openstack-s11auth/auth')
        if os.path.exists(path):
            try:
                with open(path) as f:
                    return f.readline()
            except OSError as e:
                raise Exception(e)
        return None


class UseProject(command.Command, Manager):
    """Override the project in the current context within the clouds.yaml"""

    auth_required = False

    def get_parser(self, prog_name):
        parser = super(UseProject, self).get_parser(prog_name)
        contexts = set(self.get_context_names())
        contexts.add('none')
        parser.add_argument(
            'project_id',
            metavar='<project_id>',
        )
        return parser

    def take_action(self, parsed_args):
        current_context = self.get_current_context()
        if not current_context:
            return NO_ACTIVE_CONTEXT_ERROR

        yaml, code = Manager().get_config()
        code['clouds'][current_context]['auth']['project_id'] = parsed_args.project_id
        Manager.write_config(yaml, code)
