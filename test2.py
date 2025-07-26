from flask import Flask, request, jsonify, render_template
import paramiko
from database import DatabaseManager
import subprocess
# 初始化数据库管理器
db_manager = DatabaseManager()
# SSH 连接信息
hostname = '192.168.199.129'
username = 'hadoop'
password = '150410'

# 创建 SSH 客户端连接
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname, username=username, password=password)


# 执行切换到 root 用户的命令

# 执行命令函数
def execute_command(command):
    # stdin, stdout, stderr = ssh_client.exec_command(f'sudo su\n')
    # stdin.write(f'150410\n')  # 输入 root 用户的密码
    # stdin.flush()
    # stdin.write(f'150410\n')  # 输入 root 用户的密码
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if error:
        print(f"Error: {error}")
    return output


# def check_vm_status():
#     # output = subprocess.run(['ovs-vsctl', 'list-ports', 'br0'], capture_output=True, text=True)
#     # ports = output.stdout.split('\n')
#     # return ports
#     # 执行命令
command = "sudo /usr/local/bin/ovs-vsctl list-ports br0"

output = execute_command(command)

out=output
print(out)
db_manager_vms1 = db_manager.get_all_vms()
print(db_manager_vms1)

# 检查虚拟机状态
for vm_name in db_manager_vms1:
    if vm_name not in out:
        print("虚拟机已掉线")
