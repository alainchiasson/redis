import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_redis_data_path(host):
    d = host.file("/data")

    assert d.is_directory


def test_redis_installed(host):
    redis = host.package("redis")

    assert redis.is_installed


def test_cluster_test_dir(host):
    f = host.file('/home/vagrant/cluster-test')

    assert f.exists


def test_redis_subdirs(host):
    f = host.file('/home/vagrant/cluster-test/7000')

    assert f.exists


def test_redis_subdirs(host):
    f = host.file('/home/vagrant/cluster-test/7001')

    assert f.exists


def test_redis_subdirs(host):
    f = host.file('/home/vagrant/cluster-test/7002')

    assert f.exists


def test_redis_subdirs(host):
    f = host.file('/home/vagrant/cluster-test/7003')

    assert f.exists


def test_redis_subdirs(host):
    f = host.file('/home/vagrant/cluster-test/7004')

    assert f.exists


def test_redis_subdirs(host):
    f = host.file('/home/vagrant/cluster-test/7005')

    assert f.exists
