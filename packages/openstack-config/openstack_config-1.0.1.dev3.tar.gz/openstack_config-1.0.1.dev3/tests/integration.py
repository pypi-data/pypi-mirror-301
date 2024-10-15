import os
import subprocess
from os import unlink

DEFAULT_CONFIG = """clouds:
  company_eigenbedarf_ham1: # this is a comment
    auth:
      auth_url: http://localhost:1/v3 # some comment over here
      project_id: 93ccca2e1cfb4571879ada911500e2bf
    auth_type: v3s11
    region_name: ham1
    s11:
      organization_id: company-eigenbedarf
  openstack: # this is also a comment
    auth:
      auth_url: http://localhost:1/v3
      username: s.user@domain.tld
      project_id: 0adb386b76164af9b3035b1b9cbd1072
      project_name: company-syseleven-employee-suser # and some more
      user_domain_name: Default
    regions:
    - INFRA
    interface: public
    identity_api_version: 3"""

OPENSTACK_CONFIG_PATH = os.path.join(
    os.path.expanduser(os.path.join('~', '.config')), 'openstack'
)
CLOUDS_CONFIG_PATH = os.path.join(OPENSTACK_CONFIG_PATH, 'clouds.yaml')
CONTEXT_CONFIG_PATH = os.path.join(OPENSTACK_CONFIG_PATH, 'context')


def deploy_clouds_config(content):
    os.makedirs(OPENSTACK_CONFIG_PATH, exist_ok=True)
    with open(CLOUDS_CONFIG_PATH, 'w') as f:
        f.write(content)


def remove_clouds_config():
    try:
        unlink(CLOUDS_CONFIG_PATH)
    except FileNotFoundError:
        pass


def deploy_context_config(content):
    os.makedirs(OPENSTACK_CONFIG_PATH, exist_ok=True)
    with open(CONTEXT_CONFIG_PATH, 'w') as f:
        f.write(content)


def remove_context_config():
    try:
        unlink(CONTEXT_CONFIG_PATH)
    except FileNotFoundError:
        pass


def cli(params=''):
    p = subprocess.Popen(f'openstack {params}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = ''
    for line in p.stdout.readlines():
        buf += line.decode()
    retval = p.wait()
    return retval, buf


def test_get_contexts_without_clouds_config_fails():
    # listing contexts without clouds.yaml should error
    remove_clouds_config()
    code, buf = cli('config get-contexts')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_get_contexts_with_clouds_config_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    code, buf = cli('config get-contexts -f value')
    assert code == 0
    assert buf == """company_eigenbedarf_ham1\nopenstack\n"""


def test_getting_context_without_any_config_succeeds():
    remove_clouds_config()
    remove_context_config()
    code, buf = cli('config current-context')
    assert code == 0
    assert buf == "None\n"


def test_getting_context_without_clouds_config_fails():
    remove_clouds_config()
    deploy_context_config("doesnotexist")
    code, buf = cli('config current-context')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_setting_context_without_clouds_config_fails():
    remove_clouds_config()
    remove_context_config()
    code, buf = cli('config use-context doesnotexist')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_setting_invalid_context_with_clouds_config_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config use-context doesnotexist')
    assert code == 2
    assert "invalid choice: 'doesnotexist' (choose from '" in buf
    assert "company_eigenbedarf_ham1" in buf
    assert "openstack" in buf


def test_setting_context_with_clouds_config_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config use-context company_eigenbedarf_ham1')
    assert code == 0
    assert buf == ""

    code, buf = cli('config current-context')
    assert code == 0
    assert buf == "company_eigenbedarf_ham1\n"


def test_rename_context_without_cloud_config_fails():
    remove_clouds_config()
    remove_context_config()
    code, buf = cli('config rename-context foo bar')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_rename_unknown_context_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config rename-context doesnotexist bar')
    assert code == 2
    assert "invalid choice: 'doesnotexist' (choose from" in buf
    assert "company_eigenbedarf_ham1" in buf
    assert "openstack" in buf


def test_rename_context_already_exists_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config rename-context company_eigenbedarf_ham1 openstack')
    assert code == 1
    assert buf == "Context already exists\n"


def test_rename_context_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config rename-context company_eigenbedarf_ham1 something_else')
    assert code == 0
    assert buf == ""


def test_rename_currently_set_context_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config use-context company_eigenbedarf_ham1')
    assert code == 0
    assert buf == ""

    code, buf = cli('config current-context')
    assert code == 0
    assert buf == "company_eigenbedarf_ham1\n"

    code, buf = cli('config rename-context company_eigenbedarf_ham1 something_else')
    assert code == 0
    assert buf == ""

    # current context should be renamed, too
    code, buf = cli('config current-context')
    assert code == 0
    assert buf == "something_else\n"


def test_delete_non_existing_context_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config delete-context doesnotexist')
    assert code == 2
    assert "invalid choice: 'doesnotexist' (choose from" in buf
    assert "company_eigenbedarf_ham1" in buf
    assert "openstack" in buf


def test_delete_existing_context_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()
    code, buf = cli('config delete-context company_eigenbedarf_ham1')
    assert code == 0
    assert buf == ""

    code, buf = cli('config get-contexts -f value')
    assert code == 0
    assert buf == """openstack\n"""


def test_delete_currently_set_context_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config use-context company_eigenbedarf_ham1')
    assert code == 0
    assert buf == ""

    code, buf = cli('config current-context')
    assert code == 0
    assert buf == "company_eigenbedarf_ham1\n"

    code, buf = cli('config delete-context company_eigenbedarf_ham1')
    assert code == 0
    assert buf == ""

    # current context should be reset
    code, buf = cli('config current-context')
    assert code == 0
    assert buf == "None\n"


def test_unset_without_cloud_config_fails():
    remove_clouds_config()
    remove_context_config()

    code, buf = cli('config unset foo.bar.baz')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_unset_unknown_specification_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config unset foo.bar.baz')
    assert code == 0
    assert "could not access 'foo', part 0 of Path('foo', 'bar', 'baz'), got error: KeyError('foo')" in buf


def test_unset_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config unset clouds.openstack.regions')
    assert code == 0
    assert buf == ""

    code, buf = cli('config view')
    assert code == 0
    expected_config = DEFAULT_CONFIG.replace('    regions:\n    - INFRA\n', '')
    assert buf == expected_config + "\n\n"


def test_set_without_cloud_config_fails():
    remove_clouds_config()
    remove_context_config()

    code, buf = cli('config set foo.bar.baz something')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_set_unknown_specification_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config set foo.bar.baz something')
    assert code == 0
    assert "could not access 'foo', part 0 of Path('foo', 'bar', 'baz'), got error: KeyError('foo')" in buf


def test_set_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config set clouds.openstack.regions.0 region1')
    assert code == 0
    assert buf == ""

    code, buf = cli('config view')
    assert code == 0
    expected_config = DEFAULT_CONFIG.replace('- INFRA\n', '- region1\n')
    assert buf == expected_config + "\n\n"


def test_use_project_without_cloud_config_fails():
    remove_clouds_config()
    remove_context_config()

    code, buf = cli('config use-project something')
    assert code == 1
    assert buf == "Config file is empty or does not exist\n"


def test_use_project_without_active_context_fails():
    deploy_clouds_config(DEFAULT_CONFIG)
    remove_context_config()

    code, buf = cli('config use-project something')
    assert code == 1
    assert buf == "Please activate a context via use-context first\n"


def test_use_project_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    deploy_context_config('openstack')

    code, buf = cli('config use-project something')
    assert code == 0
    assert buf == ""

    code, buf = cli('config view')
    assert code == 0
    expected_config = DEFAULT_CONFIG.replace('project_id: 0adb386b76164af9b3035b1b9cbd1072', 'project_id: something')
    assert buf == expected_config + "\n\n"


def test_get_projects_v3s11_auth_succeeds():
    deploy_clouds_config(DEFAULT_CONFIG)
    deploy_context_config('openstack')

    code, buf = cli('config get-projects')
    assert code == 1
    assert buf == "No password entered, or found via --os-password or OS_PASSWORD\n"

    deploy_context_config('company_eigenbedarf_ham1')

    # create dummy openstack-s11-auth token to avoid local oauth flow
    s11auth_config_path = os.path.join(
        os.path.expanduser(os.path.join('~', '.config')), 'openstack-s11auth'
    )
    os.makedirs(s11auth_config_path, exist_ok=True)
    with open(os.path.join(s11auth_config_path, 'auth'), 'w') as f:
        f.write('dummy')

    code, buf = cli('config get-projects')
    assert code == 1
    assert "HTTPConnectionPool(host='localhost', port=1): Max retries exceeded with url: /v3/auth/tokens" in buf
