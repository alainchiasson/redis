Role Name
=========

The role is to deploy and manage a redis cluster across multiple machines.

Requirements
------------

Prior to running the roles, the following must be in place :

- Access to a REPO with the redis RPM (In testing we add the EPEL repo)
- A version of Ruby installed (In testing we use the Centos packages)
- An defined group where the nodes are to e installed. (default is redis_nodes)

Either:
- Access to a repo with rubygems-redis (In testing we use EPEL repo)
- GEM installed so we can use the ruby gem embeded in this role. (May remove)

Role Variables
--------------

### Cluster variables

| Variables | Description | Default |
|-----------|-------------|---------|
| redis_num_masters | The number of redis masters to configure. The Number of masters need to be greater than the pool of servers to install on | 3 |
| redis_num_replicas | the number of replicas to use (0 for no slaves) | 1 |

Both these numbers will determin the total number of nodes to deploy ( eg: 3,1 will
mean 6 nodes )

### Node variables

The following variables will be used for each node deployed. These are base
directories and node data will be segregated based on the running port :

| Variable | Description | Default |
|----------|-------------|---------|
| redis_data_dir | Directory that will hold the persistent data for redis (eg: Data, cluster state)| /var/lib/redis |
| redis_log_dir | Directory where log files will be placed | /var/log/redis |
| redis_run_dir | Directory where runtime information will be storred (eg: pid file )| /var/run/redis |

Each node will have either a directory ( eg: /ver/lib/redis/7000/ ) or a file
( eg: /var/log/redis/redis_7000.log ). No node will have

Dependencies
------------

No external role or Ansible module dependancies.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: redis_nodes
      roles:
         - { name: redis }


License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).


NOTES:
----------

After an initial installation of redis :

```
rpm -ql redis

# results :
# /etc/logrotate.d/redis
# /etc/redis-sentinel.conf
# /etc/redis.conf
# /etc/systemd/system/redis-sentinel.service.d
# /etc/systemd/system/redis-sentinel.service.d/limit.conf
# /etc/systemd/system/redis.service.d
# /etc/systemd/system/redis.service.d/limit.conf
# /usr/bin/redis-benchmark
# /usr/bin/redis-check-aof
# /usr/bin/redis-check-rdb
# /usr/bin/redis-cli
# /usr/bin/redis-sentinel
# /usr/bin/redis-server
# /usr/bin/redis-shutdown
# /usr/lib/systemd/system/redis-sentinel.service
# /usr/lib/systemd/system/redis.service
# /usr/lib/tmpfiles.d/redis.conf
# /usr/share/doc/redis-3.2.3
# /usr/share/doc/redis-3.2.3/00-RELEASENOTES
# /usr/share/doc/redis-3.2.3/BUGS
# /usr/share/doc/redis-3.2.3/CONTRIBUTING
# /usr/share/doc/redis-3.2.3/MANIFESTO
# /usr/share/doc/redis-3.2.3/README.md
# /usr/share/licenses/redis-3.2.3
# /usr/share/licenses/redis-3.2.3/COPYING
# /var/lib/redis
# /var/log/redis
# /var/run/redis
```

And what these files are :

```
for x in `rpm -ql redis`; do file $x; done

# /etc/logrotate.d/redis: ASCII text
# /etc/redis-sentinel.conf: ASCII text
# /etc/redis.conf: ASCII text
# /etc/systemd/system/redis-sentinel.service.d: directory
# /etc/systemd/system/redis-sentinel.service.d/limit.conf: ASCII text
# /etc/systemd/system/redis.service.d: directory
# /etc/systemd/system/redis.service.d/limit.conf: ASCII text
# /usr/bin/redis-benchmark: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=e9d9974aa6b362834bf544c53ab964ffa39dbaf4, stripped
# /usr/bin/redis-check-aof: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=b46a75afd814646dfdd855ec39aa9f536d494230, stripped
# /usr/bin/redis-check-rdb: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=ff43457dbc36180a951428e87d5cc7182b2de156, stripped
# /usr/bin/redis-cli: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=d73ac4121eefc9c6bbfe8dc7e5e24b771cfe5e0a, stripped
# /usr/bin/redis-sentinel: symbolic link to `redis-server'
# /usr/bin/redis-server: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, BuildID[sha1]=ff43457dbc36180a951428e87d5cc7182b2de156, stripped
# /usr/bin/redis-shutdown: Bourne-Again shell script, ASCII text executable
# /usr/lib/systemd/system/redis-sentinel.service: ASCII text
# /usr/lib/systemd/system/redis.service: ASCII text
# /usr/lib/tmpfiles.d/redis.conf: ASCII text
# /usr/share/doc/redis-3.2.3: directory
# /usr/share/doc/redis-3.2.3/00-RELEASENOTES: UTF-8 Unicode text
# /usr/share/doc/redis-3.2.3/BUGS: ASCII text
# /usr/share/doc/redis-3.2.3/CONTRIBUTING: ASCII text, with very long lines
# /usr/share/doc/redis-3.2.3/MANIFESTO: ASCII text
# /usr/share/doc/redis-3.2.3/README.md: ASCII text, with very long lines
# /usr/share/licenses/redis-3.2.3: directory
# /usr/share/licenses/redis-3.2.3/COPYING: ASCII text, with very long lines
# /var/lib/redis: directory
# /var/log/redis: directory
# /var/run/redis: directory
```


Installation step by step - manual:
------------------------------------

# install EPEL repo ( this will be assumed )
```
yum install -y epel-release
```

# Insatll redis from repo ( this is where we start )
```
yum install -y redis
```

# We may want to adjust the retention in log rotate. Create a seperate module
# to manage this.
```
cat /etc/logrotate.d/redis

/var/log/redis/*.log {
    weekly
    rotate 10
    copytruncate
    delaycompress
    compress
    notifempty
    missingok
}
```
# Startup is also install - this will need to be edited for multi machine
```
cat /usr/lib/systemd/system/redis.service

# [Unit]
# Description=Redis persistent key-value database
# After=network.target
#
# [Service]
# ExecStart=/usr/bin/redis-server /etc/redis.conf --daemonize no
# ExecStop=/usr/bin/redis-shutdown
# User=redis
# Group=redis
#
# [Install]
# WantedBy=multi-user.target
```

Copy notes:
-----------
