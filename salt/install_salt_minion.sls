salt_source:
  file.managed:
  - name: /etc/apt/sources.list.d/saltstack-salt-trusty.list
  - source: salt://minions/files/saltstack-salt-trusty.list
salt_pkg:
  pkg.installed:
  - name: salt-minion
  - skip_verify: True
  - require:
    - file: salt_source
salt_conf:
  file.managed:
  - name: /etc/salt/minion
  - source: salt://minions/files/minion
  - template: jinja
  - defaults:
    minion_id: {{grains['host']}}
  - require:
    - pkg: salt_pkg
salt_service:
  service.running:
  - name: salt-minion
  - require:
    - file: salt_conf
  - watch:
    - file: salt_conf
