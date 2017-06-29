import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')



# Verify that package was installed
def test_redis_installed(host):
    redis = host.package("redis")

    assert redis.is_installed

# define the array of ports - base the configs on.

ports = [
    ("7000"),
    ("7001"),
    ("7002"),
    ("7003"),
    ("7004"),
    ("7005"),
    ("7006"),
    ("7007"),
]

# Verify the datapath
def test_redis_data_path(host):
    d = host.file("/var/lib/redis")

    assert d.is_directory


@pytest.mark.parametrize("port", ports)
def test_redis_subdirs(host, port):

    f = host.file("/var/lib/redis/" + port)

    assert f.exists
    assert f.is_directory

# Verify that the configs are correct
@pytest.mark.parametrize("port", ports)
def test_redis_subdirs(host, port):

    f = host.file("/etc/redis_" + port + ".conf")

    assert f.exists
    assert f.is_file
    # The following does not work as expected. Need to find out why
    assert f.contains("port " + port)
