collectd_pkg:
   pkg:
   - pkgs: '["build-essential","librrd-dev","libsensors4-dev","libsnmp-dev","collectd"]'
   - installed
collectd_conf:
   file.managed:
   - name: /etc/collectd/collectd.conf
   - source: salt://collectd/conf/collectd_agent.conf
   - require:
     - pkg: collectd_pkg
collectd_service:
  service.running:
  - name: collectd
  - require:
    - file: collectd_conf
  - watch:
    - file: collectd_conf


#  pkg.installed:
#  - name: librrd2-dev
#  - skip_verify: True
#  pkg.installed:
#  - name: libsensors4-dev
#  - skip_verify: True
#  pkg.installed:
#  - name: libsnmp-dev
#  - skip_verify: True
#  pkg.installed:
#  - name: collectd
#  - skip_verify: True
#salt_conf:
#  file.managed:
#  - name: /etc/salt/minion
#  - source: salt://minions/files/minion
#  - template: jinja
#  - defaults:
#    minion_id: {{grains['host']}}
#  - require:
#    - pkg: salt_pkg
#salt_service:
#  service.running:
#  - name: salt-minion
#  - require:
#    - file: salt_conf
#  - watch:
#    - file: salt_conf
