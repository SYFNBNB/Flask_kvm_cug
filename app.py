from flask import Flask, request, jsonify, render_template
import paramiko
from database import DatabaseManager
import subprocess

app = Flask(__name__)

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


# 添加 VLAN
@app.route("/api/add_vlan", methods=["POST"])
def add_vlan():
    data = request.json
    vlan_id = data.get("vlan_id")
    # bridge_name = data.get("name")
    if vlan_id:  # and bridge_name:
        db_manager.add_vlan(vlan_id)

        # # 在虚拟机上执行局域网划分命令
        # command = (
        #     f"sudo ovs-vsctl add-br {bridge_name} "
        #     f"sudo ovs-vsctl add-port {bridge_name} {bridge_name}.{vlan_id} tag={vlan_id}"
        # )
        # execute_command(command)

        return jsonify({"message": f"VLAN {vlan_id} 已被创建."}), 200
    else:
        return jsonify({"error": "VLAN ID and bridge name are required"}), 400


# 删除VM_VLAN
@app.route("/api/delete_vm_vlan", methods=["POST"])
def delete_vm_vlan():
    data = request.json
    vlan_id = data.get("vlan_id")
    # bridge_name = data.get("name")
    vm_name = data.get("vm_name")
    if vlan_id and vm_name:
        db_manager.delete_vm_vlan(vlan_id, vm_name)

        # 在虚拟机上执行删除局域网命令
        command = (
            # f"sudo ovs-vsctl del-port {bridge_name}.{vlan_id} && "
            f"sudo /usr/local/bin/ovs-vsctl clear Port {vm_name} tag "
        )
        execute_command(command)

        return jsonify({"message": f"VLAN {vlan_id} on 虚拟机 {vm_name} 已删除."}), 200
    else:
        return jsonify({"error": "VLAN ID and bridge name are required"}), 400


# 删除VLAN
@app.route("/api/delete_vlan", methods=["POST"])
def delete_vlan():
    data = request.json
    vlan_id = data.get("vlan_id")
    # bridge_name = data.get("name")
    # vm_name = data.get("vm_name")
    jury = db_manager.delete_vlan(vlan_id)
    if vlan_id and jury == True:
        db_manager.delete_vlan(vlan_id)
        return jsonify({"message": f"VLAN {vlan_id} 删除成功."}), 200
    else:
        return jsonify({"message": f"请先删除 {vlan_id} 下的KVM虚拟机再删除vlan_id."}), 200
        return jsonify({"error": "VLAN ID and bridge name are required"}), 400


# 将虚拟机接口添加到 VLAN
@app.route("/api/add_vm_to_vlan", methods=["POST"])
def add_vm_to_vlan():
    data = request.json
    vm_name = data.get("vm_name")
    vlan_id = data.get("vlan_id")
    if vlan_id and vm_name:
        db_manager.existjudge_delete_vm_vlan(vm_name)
        db_manager.add_vm_to_vlan(vlan_id, vm_name)
        command = (
            # f"sudo su\n"
            # f"150410\n"sudo /usr/local/bin/ovs-vsctl set Port 1 tag=1
            f"sudo /usr/local/bin/ovs-vsctl set Port {vm_name} tag={vlan_id}")
        # command = f"sudo ovs-vsctl set port {vm_name} tag={vlan_id}"\
        # subprocess.call(command, shell=True)
        execute_command(command)
        # 执行成功后返回成功消息
        return jsonify({"message": f"VM成功添加到了vlan:{vlan_id}中"}), 200
    else:
        return jsonify({"error": "VM name, interface name, VLAN ID, and bridge name are required"}), 400


# 查询所有 VLAN
@app.route("/api/get_all_vlans", methods=["GET"])
def get_all_vlans():
    vlans = db_manager.get_all_vlans()
    return jsonify(vlans), 200


# 获取端口状态
# def check_vm_status():
#     # output = subprocess.run(['ovs-vsctl', 'list-ports', 'br0'], capture_output=True, text=True)
#     # ports = output.stdout.split('\n')
#     # return ports
#     # 执行命令
#
#     return output


# 获取虚拟机状态
@app.route("/api/compared", methods=["POST"])
def compared():
    # data = request.json
    # command = "sudo /usr/local/bin/ovs-vsctl list-ports br0"
    # output = execute_command(command)
    # db_manager_vms = db_manager.get_all_vms()
    # # 获取当前连接到网桥的所有端口
    # bridge_ports = output
    # # 检查虚拟机状态
    # for vm_name in db_manager_vms:
    #     if vm_name not in bridge_ports:
    #         return jsonify({"message": f"虚拟机{vm_name}已掉线"}), 200
    data = request.json
    command = "sudo /usr/local/bin/ovs-vsctl list-ports br0"
    output = execute_command(command)
    db_manager_vms = db_manager.get_all_vms()
    # 获取当前连接到网桥的所有端口
    bridge_ports = output
    # 检查虚拟机状态
    offline_vms = []
    for vm_name in db_manager_vms:
        if vm_name not in bridge_ports:
            offline_vms.append(vm_name)
    if offline_vms:
        return jsonify({"offline_vms": offline_vms}), 200
    else:
        return jsonify({"message": "所有虚拟机正常连接"}), 200


# 渲染前端页面
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
