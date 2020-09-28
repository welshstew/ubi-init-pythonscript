FROM registry.redhat.io/ubi8/ubi-init:latest

RUN dnf install -y python3 \
    && pip3 install paramiko \
  	&& dnf clean all \
  	&& rm -rf /var/cache/yum

ADD lib/systemd/system/*.service /lib/systemd/system/
ADD script/*.py /home
ADD health/*.sh /home

RUN systemctl enable helloworld.service \
    && systemctl enable transfer.service \
    && chmod +x /home/*.sh

CMD [ "/sbin/init" ]