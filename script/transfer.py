import paramiko
import os

print(os.environ)

ssh_client =paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=os.getenv('SFTP_HOSTNAME'),username=os.getenv('SFTP_USERNAME'),password=os.getenv('SFTP_PASSWORD'))
# stdin,stdout,stderr=ssh_client.exec_command("ls")
# print(stdout.readlines())

ftp_client=ssh_client.open_sftp()
ftp_client.get(os.getenv('SFTP_REMOTE_FILE'),os.getenv('SFTP_LOCAL_FILE'))
ftp_client.close()

f = open(os.getenv('SFTP_LOCAL_FILE'))
print(f.read())