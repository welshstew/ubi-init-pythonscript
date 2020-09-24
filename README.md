# ubi-init-pythonscript

Simple example using the rhel8 ubi-init base image with systemd, adding python and some scripts and running those python scripts as systemd services on container start.

Build with:
```
podman build -t quay.io/swinches/ubi-init-pythonscript:latest .
```

The container will attempt to pull a file from a server via ssh.  Add environment variables to a file named `transfer.env` and place in a local `./env` folder.

```
SFTP_HOSTNAME=1.2.3.4
SFTP_USERNAME=user
SFTP_PASSWORD=password 
SFTP_REMOTE_FILE=/share/testfolder/somefile.txt
SFTP_LOCAL_FILE=/tmp/somefile.txt
```

Run with:
```
podman run --mount=type=bind,source=./env,destination=/etc/transfer,relabel=shared quay.io/swinches/ubi-init-pythonscript:latest
```

