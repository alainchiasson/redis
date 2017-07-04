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

 There is also the ```redis``` role which only contains the common default, of which
 all other roles are dependant (see meta/main.yml)

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

Example 2: 3 host cluster (defined in redis-nodes), with 3 master nodes with 1 replicas (6 nodes total). Notice that we define a node as management to install the management application.

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
This role has been developed with the goal to simplify the deployment of a redis cluster
across multiple nodes.

## Redis/Core

The following user variable can be redefined for the redis/core.

| Variable | Description | Default |
|----------|-------------|---------|
| redis_data_dir | The root of the data directory | /var/lib/redis |
| redis_log_dir | The root direcotry for redis logs | /var/log/redis |
| redis_run_dir | The root direcotry for redis runtime information | /var/run/redis |
| redis_conf_dir | The root directry for redis node configuraitons | /etc/ |

NOTE: The role currently only supports Centos / rpm based installs. The role will install the redis package - which creates some default configs and
 directories - but will be ignored

The following variables are also defined, but not usualy  redefined in this role.:

| Variable | Description | Default |
|----------|-------------|---------|
| redis_packages | A list of packages required to install redis | [ redis ] |
| redis_port |  The default port that redis will listen to. | 6379 |


NOTE: redis_port can be overridden in the redis/node deployment.
## Redis/Node

The redis node role will configure and start a redis node on a specific port. Tasks
performed by the redis/node role include:

- Creating the data sub-direcotries ( under redis_data_dir as redis_data_dir/<port>)
- Configure a custom redis.conf file ( under redis_conf_dir as redis_conf_dir/redis_<port>.conf )
- Configure a custom systemd service definition ( In system standard location as redis_<port>.service )
- Add the listening ports to the SElinux security contexts ( for RPM based systems )
- Start the configured redis node.

The following variables can be redefined by users of this role:

| Variable | Description | Default |
|----------|-------------|---------|
| redis_port | The port that redis will listen to. | 6379 |

This port number is used to configure all above items. This is a sane default
as the host cannot have more than one redis instance listening to a single port.
The default redis shutdown script uses this information to derive the proper config.

## Redis/cluster

Redis cluster will take a series of cluster nodes, and configure them in a single
cluster based on configurable parameters. This has been done to simplefy the
deployment of the cluster.

The follwing are commonly overridden when creating the cluster:

| Variables | Description | Default |
|-----------|-------------|---------|
| redis_cluster_replicas | The number of replicas each master requires | 0 |
| redis_node_list | a list of 'IP:PORT' endpoint combinations | see defaults |


Other variables used that should not be overridden:

| Variables | Description | Default |
|-----------|-------------|---------|
| redis_conf_dir | to create a "cluster defined" flag for idempotency | see redis/core |

Other notes:
- In the redis.io ```redis-trib``` ruby application, we added a ```--yes``` flag to accept the
proposed configuration without waiting for user input.
- redis-trib does an inteligent distribution of the nodes based on number of
replicas, number of nodes and hosts. One assumption is that different IP's are
different hosts. It will rotate through the servers to increase availability in
case of a host failure.

Dependencies
------------

No external role or Ansible module dependancies.

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
