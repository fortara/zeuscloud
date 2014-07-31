collectd_pkg:
   pkg:
   - pkgs: '["build-essential","librrd-dev","libsensors4-dev","libsnmp-dev","collectd"]'
   - installed
apache_pkg:
   pkg:
   - pkgs: '["apache2","php5","php5-gd","libapache2-mod-php5"]'
   - installed
collectd_conf:
   file.managed:
   - name: /etc/collectd/collectd.conf
   - source: salt://collectd/conf/collectd_server.conf
   - require:
     - pkg: collectd_pkg
collectd_service:
  service.running:
  - name: collectd
  - require:
    - file: collectd_conf
  - watch:
    - file: collectd_conf

