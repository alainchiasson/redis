Redis role development
======================

These are quick notes for folowup development.

Development Environment
-----------------------

This role was developed using the molecule test framework that allows automation
of infrastructure testing. See the various ```INSTALL.rst``` files for additional
information.

Scenarios
---------

The current scenario validate proper deployment for the following:

- Defaults - where nothing is custom. Currently the role ONLY deploys in cluster
  mode, so 3 nodes are required.
- Single-node - where we deploy 3 nodes on a single host.
- multi-node : Where a 3 master + 3 Slave infrastructure is deployed accross
  hosts. This is closer to a typical deployment.

Other notes:
------------

In testing, the server names are not defiend, so we had to derive them from the
IP's. To get the node endpoints we had to combine the IP's with the node ports.
We created a custom jinja2 filter for this : arraypermute(array)

Usage:

{{ array1 | arraypermute( array2 ) | list }}

If Array1 = [ a,b,c,d ]
and Array2 = [ 1,2,3 ]

the resulting array will be every combination, namely :

[ a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3 ]

Notes on usage:
---------------
A sane way to use this role, is to label hosts [ redis-nodes ] and create a
[ redis-ports ] array. The ansible roles should be run on all redis-nodes, and
redis/node should loop over the ports array, redefining the ```redis_ports```
variable. NOTE: there is currently no way to loop over a role.

```
- hosts: redis-nodes
  role:
  - redis/core
  - { role: redis/node, redis_ports: redis_ports[0] }
  - { role: redis/node, redis_ports: redis_ports[1] }
  - { role: redis/cluster, redis_cluster_replicas: 1, redis_node_list: {{ group['redis-nodes'] | arraypermute( [:] ) | arraypermute( redis_ports ) | list }}}
```


TODO (quick thoughts)
------
- More error checking
- Test on ubunutu ( if we push to galaxy )
- Increase management tasks - eg: add a layer of slaves, add a master etc.)
- Review ansible redis module (may have done work for nothing)
- Create a "redis/config" role for more hands on redis.conf values.
- add security - how to propagate config to clients ?
- add logrotate - should be easy -  base is already there.
