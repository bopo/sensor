# -*- coding: utf-8 -*-

import os

from fabric.api import cd, env, local, run, task
from fabric.contrib import project

env.roledefs = {
    'dev': ['root@103.200.97.197'],
    'pre': [''],
}

env.excludes = (
    "*.pyc", "*.db", ".DS_Store", ".coverage", ".git", ".hg", ".tox", ".idea/",
    'assets/', 'runtime/', 'db.sqlite3', 'tests', 'docs', '__pycache__',
    'env.docker', 'env.server', 'docs')

env.remote_dir = '/home/site/sensor/server'
env.local_dir = '.'


@task
def init():
    '''远程初始化 docker 部署'''
    run('make build')
    run('make setup')
    run('make docs')


@task
def unix():
    '''文本文件 windows 格式转 unix 格式'''
    local('find . "*.txt" | xargs dos2unix')
    local('find . "*.md" | xargs dos2unix')
    local('find . "*.py" | xargs dos2unix')
    local('find . "Makefile" | xargs dos2unix')


@task(alias='ci')
def commit():
    '''提交源码仓库'''
    local('git commit -m "first commit"')


@task
def push():
    '''提交源码仓库'''
    local('git push -u origin develop')


@task
def stat():
    '''更新静态文件'''
    with cd(env.remote_dir):
        run('python manage.py collectstatic --noinput')


@task
def sync():
    '''同步服务器代码'''
    project.rsync_project(
        remote_dir=env.remote_dir,
        local_dir=env.local_dir,
        exclude=env.excludes,
        delete=False
    )


@task
def migr():
    '''合并数据文件'''
    with cd(env.remote_dir):
        run('''python manage.py migrate''')


@task()
def init():
    '''初始化服务'''
    local_dir = os.getcwd() + os.sep
    project.rsync_project(
        remote_dir=env.remote_dir,
        local_dir=local_dir,
        exclude=env.excludes,
        delete=True
    )

    run('/usr/bin/supervisorctl device start')


@task()
def rest():
    '''重启服务'''
    run('/usr/bin/supervisorctl restart device')


@task
def stop():
    '''停止服务'''
    run('/usr/bin/supervisorctl device stop')


@task
def pack(time=None):
    '''文件打包'''
    local('tar zcfv ./release.tgz '
          '--exclude=.git '
          '--exclude=.tox '
          '--exclude=.svn '
          '--exclude=.idea '
          '--exclude=*.tgz '
          '--exclude=*.pyc '
          '--exclude=.vagrant '
          '--exclude=tests '
          '--exclude=storage '
          '--exclude=database '
          '--exclude=.DS_Store '
          '--exclude=.phpintel '
          '--exclude=.template '
          '--exclude=db.sqlite3 '
          '--exclude=Vagrantfile .')
