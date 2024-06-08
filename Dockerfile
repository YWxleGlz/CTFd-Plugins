FROM ctfd/ctfd:3.7.0

COPY plugins/ /opt/CTFd/CTFd/plugins/

ENTRYPOINT ["/opt/CTFd/docker-entrypoint.sh"]
