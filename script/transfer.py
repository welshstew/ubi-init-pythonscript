from time import sleep
import paramiko
import os

print(os.environ)

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Opening Connection to {}".format(os.getenv('SFTP_HOSTNAME')) )
ssh_client.connect(hostname=os.getenv('SFTP_HOSTNAME'),username=os.getenv('SFTP_USERNAME'),password=os.getenv('SFTP_PASSWORD'))
# stdin,stdout,stderr=ssh_client.exec_command("ls")
# print(stdout.readlines())

print("Transferring remote file: {} to local file: {}".format(os.getenv('SFTP_REMOTE_FILE'), os.getenv('SFTP_LOCAL_FILE')) )
ftp_client=ssh_client.open_sftp()
ftp_client.get(os.getenv('SFTP_REMOTE_FILE'),os.getenv('SFTP_LOCAL_FILE'))
ftp_client.close()

f = open(os.getenv('SFTP_LOCAL_FILE'))
content = f.read()

for i in range(10):
    print("Printing File {} {}".format(i, content))
    sleep(10)
