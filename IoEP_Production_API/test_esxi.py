'''
Created on Apr 13, 2015

@author: tim.huang
¡­easy_install pysphere
or
pip install ¡VU pysphere
'''
from pysphere import VIServer

if __name__ == '__main__':
    server = VIServer()
    server.connect("10.90.1.16", "root", "xxxxxxx")
    vms = server.get_registered_vms()
    
    for serverpath in vms:
        print serverpath
        vm=server.get_vm_by_path(serverpath)
  
        vm.get_properties()
        vm.get_property("hostname")
    
    
    vm = server.get_vm_by_path(vms[0])
    print vm.get_property("mac_address")
    print vm.get_property("ip_address")
    print vm.get_property("name")
    print vm.get_resource_pool_name()
    #vm = server.get_vm_by_path("[datastore1] s1/s1.vmx")
    vm.power_on()