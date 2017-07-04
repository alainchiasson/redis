Redis
=========

The role is to deploy a redis cluster across multiple machines.

Requirements
------------

Prior to running the roles, the following must be in place :

- Access to an RPM with the EPEL redis RPM (In testing we add the EPEL repo)
- A version of Ruby installed (In testing we use the Centos packages)

Optionaly:
- An Ansible group where the nodes are to be installed.
- An Ansible group where the management node can be installed

Role Usage
----------

The role is currently broken into 3 parts:
 - redis/core : to install the required components for redis
 - redis/node : which will configure everything for a node, and get it running
 - redis/cluster : Use to create the cluster from the individual nodes

Example 1: A single host with 3 master-nodes, no replication.

```
 - hosts: all
   become: true
   roles:
     - redis/core
     - { role: redis/node, redis_port: 7000 }
     - { role: redis/node, redis_port: 7001 }
     - { role: redis/node, redis_port: 7002 }
     - { role: redis/cluster, redis_cluster_replicas: 0, redis_node_list: "{{ groups['all'] | map('extract', hostvars, ['ansible_eth0', 'ipv4', 'address']) | arraypermute( [':'] ) | arraypermute( [7000,7001,7002] ) }}" }
```

Example 2: 3 host cluster, with 3 master nodes with 1 replicas (6 nodes total). Notice that we define a node as management to install the management application.

```
- hosts: redis-nodes
  become: true
  roles:
    - redis/core
    - { role: redis/node, redis_port: 7000 }
    - { role: redis/node, redis_port: 7001 }

- hosts: redis-mgt
  become: true
  roles:
    - { role: redis/cluster, redis_cluster_replicas: 1, redis_node_list: "{{ groups['redis-nodes'] | map('extract', hostvars, ['ansible_eth1', 'ipv4', 'address']) | arraypermute( [':'] ) | arraypermute( [7000,7001] ) | list }}" }

```

Role Variables
--------------


## Redis

The following user variable can be redefined for the redis.

| Variable | Description | Default |
|----------|-------------|---------|
| redis_data_dir | The root of the data directory | /var/lib/redis |
| redis_log_dir | The root direcotry for redis logs | /var/log/redis |
| redis_run_dir | The root direcotry for redis runtime information | /var/run/redis |
| redis_conf_dir | The root directry for redis node configuraitons | /etc/ |

The role currently only supports Centos / rpm based installs.

The role will install the redis package(which creates seom default configs and directories - that we may ignore )

The following variables are also defined, but should not be chagned:

| Variable | Description | Default |
|----------|-------------|---------|
| redis_packages | A list of packages required to install redis | [ redis ] |
| redis_port |  The default port that redis will listen to. | 6379 |


NOTE: redis_port can be overridden in the redis/node deployment.
## Redis/Node

The redis nodes are dif

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
| redis_port | The Port the redis instance should listen to. Used in all steps of the deployment | 6379 |
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

deploy with default listen port (6379)

```
- hosts: all
  become: true
  roles:
    - redis
```

Deploy 3 redis nodes alternate ports (7001, 7002, 7003)

```
- hosts: all
  become: true
  roles:
    - { name: redis, redis_port: 7000 }
    - { name: redis, redis_port: 7001 }
```

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).


NOTES:
----------

Issue with include_role. I had tried the follwoing :

in playbook :

```
roles:
  - { role: redis, redis_ports: [7000, 7001] }
```

And in role:redis, at the end, I had :

```
 - name: Create all the nodes.
   include_role:
     name: redis/node
   vars:
     redis_port: "{{ item }}"
   with_items:
     - "{{ redis_ports }}"

```

While it did work, the redis role was executed for every machine, then the loop was also run
for every machine as well - so machine x machine !!

Looking for a "execute once" - I think in dynamic vs static include.  I tried the
allow_duplicates: False option and it did not work.

## Goal playbook ? Maybe not. Works great if it is only one node.
#
# roles:
#   - redis-deploy
#   - redis-mgt
#   - { name: redis, redis_port: 7000 }
#   - { name: redis, redis_port: 7001 }
#   - { name: redis, redis_port: 7002 }
#   - redis-cluster

## take2:
#
# - hosts: redis-nodes
#   roles:
#   - { name: redis-cluster, redis_cluster_num_master: 3, redis_cluster_replicas: 1 }
#
# Questions is how does this distribute the nodes across the entire clsuter ?
#

## take3:
#
#  Define nodes per server and build the cluster from an array
#
#


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
No cluster enabled:

127.0.0.1:7000> cluster info
cluster_state:fail
cluster_slots_assigned:0
cluster_slots_ok:0
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:1
cluster_size:0
cluster_current_epoch:0
cluster_my_epoch:0
cluster_stats_messages_sent:0
cluster_stats_messages_received:0
127.0.0.1:7000> exit
[vagrant@redis-1-multi-node ~]$ exit
logout
Shared connection to 127.0.0.1 closed.

After cluster enabled :

[vagrant@redis-1-multi-node ~]$ redis-cli -c -p 7000 cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:3
cluster_stats_messages_sent:117
cluster_stats_messages_received:117
[vagrant@redis-1-multi-node ~]$
