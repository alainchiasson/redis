import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_redis_data_path(host):
    data_dir = host.file("/data")

    assert data_dir.is_directory


def test_redis_installed(host):
    redis = host.package("redis")

    assert redis.is_installed
