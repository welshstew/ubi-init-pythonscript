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

Run on Openshift:

```
oc create secret generic script-config --from-file=./env/
```

Without Probes:

```
oc create -f - <<EOF
---
apiVersion: v1
kind: Pod
metadata:
  generateName: ftping-
  labels:
    script: python
    init: systemd
spec:
  containers:
  - name: pythonscript
    image: quay.io/swinches/ubi-init-pythonscript:latest
    volumeMounts:
    - mountPath: /etc/transfer
      name: script-config
  restartPolicy: Never
  volumes:
  - name: script-config
    secret:
      secretName: script-config
...
EOF
```

With Probes:
```
oc create -f - <<EOF
---
apiVersion: v1
kind: Pod
metadata:
  generateName: ftping-
  labels:
    script: python
    init: systemd
spec:
  containers:
  - name: pythonscript
    image: quay.io/swinches/ubi-init-pythonscript:latest
    volumeMounts:
    - mountPath: /etc/transfer
      name: script-config
    readinessProbe:
      exec:
        command:
        - /bin/sh
        - -c
        - /home/readiness.sh
      initialDelaySeconds: 10
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1  
    livenessProbe:
      exec:
        command:
        - /bin/sh
        - -c
        - /home/liveness.sh
      initialDelaySeconds: 10
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1  
  restartPolicy: Never
  volumes:
  - name: script-config
    secret:
      secretName: script-config
...
EOF
```



As a deployment...

```
oc create sa anyuid
oc adm policy add-scc-to-user anyuid -z anyuid

oc create -f - <<EOF
---
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    openshift.io/scc: anyuid
  labels:
    script: python
    init: systemd
  name: pythonscript
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  selector:
    matchLabels:
      app.component.name: pythonscript
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app.component.name: pythonscript
    spec:
      containers:
      - image: quay.io/swinches/ubi-init-pythonscript:latest
        imagePullPolicy: Always
        command: ["/sbin/init"]
        livenessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - /home/liveness.sh
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1  
        name: pythonscript
        volumeMounts:
        - mountPath: /etc/transfer
          name: script-config
        readinessProbe:
          exec:
            command:
            - /bin/sh
            - -c
            - /home/readiness.sh
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1  
        resources:
          limits:
            cpu: 500m
            memory: 256Mi
          requests:
            cpu: 200m
            memory: 128Mi
      dnsPolicy: ClusterFirst
      serviceAccountName: anyuid
      restartPolicy: Always
      volumes:
      - name: script-config
        secret:
          secretName: script-config
...
EOF
```