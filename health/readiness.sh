systemctl status transfer.service | awk 'NR==3' | grep running