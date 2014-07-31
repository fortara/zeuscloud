/etc/sudoers.d/zinfra:
  file.managed:
    - source: salt://account/sudoer_zinfra
    - mode: 440
    - owner: root
    - group: root

/tmp/pass:
  file.managed:
    - source: salt://account/pass_zinfra
    - mode: 440
    - owner: root
    - group: root

useradd -m -d /home/zinfra -k /etc/skel -s /bin/bash zinfra:
  cmd.run:
    - unless: test -d /home/zinfra

chpasswd -e</tmp/pass && rm -f /tmp/pass:
  cmd.run:
    - onlyif: test -d /home/zinfra
