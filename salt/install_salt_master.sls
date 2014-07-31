salt_source:
  file.managed:
  - name: /etc/apt/sources.list.d/saltstack-salt-trusty.list
  - source: salt://minions/files/saltstack-salt-trusty.list
salt_pkg:
  pkg.installed:
  - name: salt-master
  - skip_verify: True
  - require:
    - file: salt_source
#salt_service:
#  service.running:
#  - name: salt-master
#  - require:
#    - file: salt_conf
#  - watch:
#    - file: salt_conf
