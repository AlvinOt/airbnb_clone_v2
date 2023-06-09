#!/usr/bin/python3
"""
Distributes archive to web servers
"""

from fabric.api import run, put, env, sudo
from os.path import isfile


env.hosts = ['54.146.64.244', '100.26.228.145']


def do_deploy(archive_path):
    """ Distributes archive to servers """
    if not isfile(archive_path):
        return False
    try:
        localpath = archive_path.split('/')[1]
        newpath = localpath.split('.')[0]
        rempath = "/data/web_static/releases/"

        put(archive_path, "/tmp/".format(localpath))
        sudo("mkdir -p {}{}".format(rempath, newpath))
        sudo("tar -xzf /tmp/{} -C {}{}".format(localpath, rempath, newpath))
        sudo("rm /tmp/{}".format(localpath))
        sudo("cp -r {0}{1}/web_static/* {0}{1}/".format(rempath, newpath))
        sudo("rm -rf {}{}/web_static".format(rempath, newpath))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {}{}/ /data/web_static/current".format(rempath, newpath))
        return True
    except:
        return False
