from fabric.context_managers import cd, prefix, settings, lcd
from fabric.contrib import django
from fabric.decorators import task, roles
from fabric.api import local
from fabric.operations import run, sudo
from fabric.state import env
from fabric.tasks import execute
from contextlib import contextmanager as _contextmanager

django.settings_module('muscn.settings')

from django.conf import settings as dj_settings

DATABASES = dj_settings.DATABASES

env.user = 'user'
env.roledefs = {
    'prod': ['202.51.74.199', ],
    'cdn': ['202.51.74.190', ],
}

paths = {
    'project_dir': '/home/xtranophilist/pro/muscn/',
    'remote_static': '/home/user/static/',
    'project_name': 'muscn',
}

hosts = [obj[0] for obj in env.roledefs.items()]
addresses = [address for address_list in [role[1] for role in env.roledefs.items()] for address in address_list]


# Mod from http://stackoverflow.com/a/5359988/328406
@_contextmanager
def virtualenv(env_path):
    with cd(env_path):
        env_activate = 'source {}/bin/activate'.format(env_path.rstrip('/'))
        with prefix(env_activate):
            yield


def remove_lines(text, matches):
    if type(matches) is not list:
        matches = [matches]
    lines = text.splitlines()
    for match in matches:
        lines = [line for line in lines if match not in line]
    return "\n".join(lines)


@task
def test():
    local("./manage.py test -v 2 --keepdb")


@task
def push_prod():
    local("git push prod master")


@task
@roles('prod', 'cdn')
def flush_pagespeed_cache():
    with settings(warn_only=True):
        sudo('touch /var/ngx_pagespeed_cache/cache.flush', shell=False)


@task
def webpack_compile():
    local('webpack -p')


# fantasysport/static/dist
@task
@roles('prod')
def sync_static():
    local("rsync -avz -e 'ssh -p 22' %s %s@%s:%s" % (
        paths['project_dir'] + 'static/', env.user, env.roledefs.get('cdn')[0], paths['remote_static']))


@task
def collect_static():
    with virtualenv(paths['project_dir'] + 'env/') and lcd(paths['project_dir'] + paths['project_name']):
        local('python manage.py collectstatic --noinput')


@task
def deploy_prod():
    # Because we don't want to run `webpack -p` on server, neither keep dist on VCS
    execute(webpack_compile)
    execute(sync_static)
    # Just push to the load balancer, git post-receive hook does the rest.
    execute(push_prod)
    execute(flush_pagespeed_cache)


@task
@roles('prod')
def manage_prod(command):
    with virtualenv(paths['prod_env']), cd(paths['prod_app']), settings(warn_only=True):
        run('./manage.py {}'.format(command))


@task
def deploy():
    local("git checkout master")
    execute(deploy_prod)


@task
@roles(hosts)
def uptime():
    run('uptime')
    
@task
def backend_deploy():
    local("git checkout master")
    execute(push_prod)

