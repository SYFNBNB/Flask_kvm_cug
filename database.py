import pymongo


class DatabaseManager:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["vlan_management"]
        self.vlan_collection = self.db["vlans"]

    def add_vlan(self, vlan_id):
        self.vlan_collection.insert_one({"vlan_id": vlan_id})

    def delete_vlan(self, vlan_id):
        vlan = self.vlan_collection.find_one({"vlan_id": vlan_id})
        if vlan:
            vms = vlan.get("vms", [])
            if vms:
                return False
            else:
                self.vlan_collection.delete_one({"vlan_id": vlan_id})
                return True
        else:
            return False

    # def delete_vlan(self, vlan_id):
    #     self.vlan_collection.delete_one({"vlan_id": vlan_id})

    def delete_vm_vlan(self, vlan_id, vm_name):
        vlan = self.vlan_collection.find_one({"vlan_id": vlan_id})

        if vlan:
            vms = vlan.get("vms", [])
            if vm_name in vms:
                vms.remove(vm_name)
                self.vlan_collection.update_one({"vlan_id": vlan_id}, {"$set": {"vms": vms}})
                return True, f"VM '{vm_name}' deleted from VLAN '{vlan_id}'"
            else:
                return False, f"VM '{vm_name}' is not associated with VLAN '{vlan_id}'"
        else:
            return False, f"VLAN '{vlan_id}' not found"

    def add_vm_to_vlan(self, vlan_id, vm_name):
        self.vlan_collection.update_one({"vlan_id": vlan_id}, {"$push": {"vms": vm_name}})
        # self.vlan_collection.insert_one({"vlan_id": vlan_id})

    def get_all_vms(self):
        vms = set()
        for vlan in self.vlan_collection.find():
            vms.update(vlan.get("vms", []))
        return vms

    def get_all_vlans(self):
        vlans = []
        for vlan in self.vlan_collection.find():
            vlans.append({
                "vlan_id": vlan["vlan_id"],
                "vms": vlan.get("vms", "")  # 获取 VM 名称，如果不存在则为空字符串
            })
        return vlans

    def existjudge_delete_vm_vlan(self, vm_name):
        vm = self.vlan_collection.find_one({"vms": vm_name})
        if vm:
            vms = vm.get("vms", [])
            vlan_id = vm.get("vlan_id")
            if vm_name in vms:
                vms.remove(vm_name)
                self.vlan_collection.update_one({"vlan_id": vlan_id}, {"$set": {"vms": vms}})
                # return True, f"VM '{vm_name}' deleted from VLAN '{vlan_id}'"
