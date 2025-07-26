# import paramiko
#
# from database import DatabaseManager
# import subprocess
#
# # 初始化数据库管理器
# db_manager = DatabaseManager()
#
# # SSH 连接信息
# hostname = '192.168.199.129'
# username = 'hadoop'
# password = '150410'
#
# # 创建 SSH 客户端连接
# ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname, username=username, password=password)
#
#
# # 获取端口状态
# # def check_vm_status():
# #     output = subprocess.run(["sudo", "/usr/local/bin/ovs-vsctl", "list-ports", "br0"], capture_output=True, text=True)
# #     ports = output.stdout.split('\n')
# #     return ports
# bridge_ports1 = output = subprocess.run(["sudo", "/usr/local/bin/ovs-vsctl", "list-ports", "br0"], capture_output=True, text=True)
# print(bridge_ports1)
#
# # db_manager_vms1 = db_manager.get_all_vms()
# # print(db_manager_vms1)
# # def execute_command():
# #     try:
# #         result = subprocess.run(["sudo", "/usr/local/bin/ovs-vsctl", "list-ports", "br0"], capture_output=True,
# #                                 text=True)
# #         if result.returncode == 0:
# #             return result.stdout.strip()  # 返回输出结果
# #         else:
# #             return f"Command execution failed with return code {result.returncode}"
# #     except Exception as e:
# #         return f"Error executing command: {str(e)}"
# #
# #
# # # 例子：获取ovs-vsctl list-ports br0的输出
# # output = execute_command()
# # print(output)
import paramiko

# SSH连接参数
hostname = '192.168.199.129'
port = 22
username = 'hadoop'
password = '150410'

# 创建SSH客户端
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # 连接到虚拟机
    client.connect(hostname=hostname, port=port, username=username, password=password)

    # 执行命令
    command = "sudo /usr/local/bin/ovs-vsctl list-ports br0"
    stdin, stdout, stderr = client.exec_command(command)

    # 读取命令输出
    output = stdout.read().decode().strip()

    # 输出命令输出
    print(output)

except Exception as e:
    print("Error executing command:", e)

finally:
    # 关闭SSH连接
    client.close()
