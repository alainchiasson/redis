import os

import testinfra.utils.ansible_runner
import pytest

# define the array of ports - base the configs on.

ports = [
    ("7000"),
    ("7001"),
    ("7002"),
]

redis_data_root = "/opt/data/redis/"
redis_log_root = "/opt/log/redis/"
redis_run_root = "/opt/run/redis/"

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


# Verify that package was installed
def test_redis_installed(host):
    redis = host.package("redis")

    assert redis.is_installed


# Verify the datapath
def test_redis_data_path(host):
    d = host.file(redis_data_root)

    assert d.is_directory


@pytest.mark.parametrize("port", ports)
def test_redis_data_subdirs(host, port):

    f = host.file(redis_data_root + port)

    assert f.exists
    assert f.is_directory


# Verify that the configs are correct
@pytest.mark.parametrize("port", ports)
def test_redis_conf_files(host, port):
    # We are testing for this, but the shutdown script hardcodes /etc location.

    f = host.file("/etc/redis_" + port + ".conf")

    assert f.exists
    assert f.is_file
    # The following does not work as expected. Need to find out why
    assert f.contains("port " + port)


@pytest.mark.parametrize("port", ports)
def test_redis_systemd_conf(host, port):
    f = host.file("/usr/lib/systemd/system/redis_" + port + ".service")

    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("port", ports)
def test_redis_service_ports(host, port):
    p = host.socket("tcp://127.0.0.1:" + port)

    assert p.is_listening


@pytest.mark.parametrize("port", ports)
def test_redis_service(host, port):
    p = host.service("redis_" + port)

    assert p.is_running
    assert p.is_enabled
