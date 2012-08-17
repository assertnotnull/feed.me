from django.conf import settings

try:
    from fabric.api import *
    from fabric.contrib.console import confirm
    from fabric.operations import put
    from fabric.api import env, run, local
    from fabric.context_managers import lcd, prefix, cd
    from fabric.utils import abort
except ImportError, e:
    print 'Python Fabric should be installed to use this script'

import re, sys, os

# globals

env.project = 'infojdemapps'
env.apps = ['socal']

# environments

def prod():
    """Select the prod environment for future commands."""
    env.hosts = ['infojdem.com']
    env.user = 'pgauthier'
    env.python = '/var/local/python/env/%s/bin/python' % env.project
    env.base_dir = '/var/local/python/' # base_dir should contain the project
    _env_init()

def _env_init():
    env.django_dir = os.path.join(env.base_dir, env.project)
    env.pip = env.python.replace('bin/python', 'bin/pip')

def local_conf():
    pass

# tasks

def test(app_name):
    "Run the test suite and bail out if it fails"
    with settings(warn_only=True):
        result = local("python manage.py test %s" % app_name)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def tests():
    for app in env.apps:
        test(app)

def first_deploy(url=None):
    """Perform all the steps in a standard deployment"""
    tests()
    clonegit(url)
    update_requirements()
    syncdb()

def deploy(ref='master'):
    tests()
    push()
    pull(ref)

def push():
    local('git push')

def sinit(app):
    if app is not None:
        local('python manage.py schemamigration %s --initial' % app)
    else:
        print'Missing application'

def sauto(app):
    if app is not None:
        local('python manage.py schemamigration %s --auto' % app)
    else:
        print 'Missing application'

def clonegit(url=None):
    if url is not None:
        with cd(env.base_dir):
            run('git clone %s' % url)
    else:
        abort('Missing valid url to pass to git clone')

def pull(ref='master'):
    """Update the git repository to the given branch or tag"""
    with cd(env.django_dir):
        run('git fetch')
        run('git fetch --tags')
        run('git checkout %s' % ref)

        is_tag = (ref == run('git describe --all %s' % ref).strip())
        if not is_tag:
            run('git pull origin %s' % ref)

            #run('git submodule update')

def update_requirements():
    """Update Python dependencies"""
    with cd(env.django_dir):
        run(env.pip + ' install -r requirements.txt')

def syncdb():
    """Update database tables"""
    with cd(env.django_dir):
        with prefix('workon %s' % env.project):
            run(env.python + ' manage.py syncdb --noinput')
            run(env.python + ' manage.py migrate')

def custom(command=None):
    with cd(env.django_dir):
        with prefix('workon %s' % env.project):
            run(env.python + ' manage.py %s' % command)

def update_statics():
    """Tell Django staticfiles to update said files."""
    with cd(env.django_dir):
        run(env.python + ' manage.py collectstatic --noinput')

#local commands for creation -- begin

DIRECTORY_NAME_REGEXP = r'^[a-zA-Z_].[\w_-]+$'
SOURCE_DIRECTORY_NAME = 'src'

PACKAGES_LIST = [
    'Django==1.3.1',
    'south',
    ]

def create_virtual_env():
    local('virtualenv --no-site-packages .')

def create_project_directory(name):
    if name is None:
        print 'You should provide project name to use this script'
        sys.exit()
    if not re.match(DIRECTORY_NAME_REGEXP, name):
        print 'Incorrect name, name can contain only numbers, letters, dash '\
              'and underscore and should start with letter or underscore'
        exit(1)
    else:
        local('mkdir %s' % name)


def install_packages():
    for package in PACKAGES_LIST:
        local('pip install %s' % package)


def create_django_project(name):
    local('mkdir %s' % SOURCE_DIRECTORY_NAME)
    local('mkdir static')
    local('mkdir media')
    local('python ./bin/django-admin.py startproject %s %s' % (name, SOURCE_DIRECTORY_NAME))


def update_settings(name):
    with open('settings.py', 'r') as base_settings:
        content = base_settings.read().replace('%%%project_name%%%', name)
        with open(os.path.join(name, SOURCE_DIRECTORY_NAME, name, 'settings.py'), 'w') as settings:
            settings.write(content)


def start_project(name=None):
    create_project_directory(name)
    with lcd(name):
        create_virtual_env()
        ve_activate_prefix = os.path.join(os.getcwd(), name, 'bin', 'activate')
        print ve_activate_prefix
        with prefix('. %s' % ve_activate_prefix):
            install_packages()
            create_django_project(name)
            update_settings(name)
            manage_py_path = os.path.join(SOURCE_DIRECTORY_NAME, 'manage.py')
            local('python %s collectstatic' % manage_py_path)
# end creation commands