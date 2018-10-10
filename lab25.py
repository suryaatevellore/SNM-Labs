import sys
import re
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException

class AdjacencyList:
    '''
        Class for creating Adjacency List

        Variables :
            Adj_device - List to store all elements

        Functions:
            add_devices - Takes an element object and appends it to Adj_device List

            show_devices - Show all devices along with neighbors
    '''
    def __init__(self):
        self.Adj_device = []

    def add_devices(self, device):
        self.Adj_device.append(device)

    def show_devices(self):
        for each_device in self.Adj_device:
            print("================================================")
            print(each_device.hostname)
            for each_neighbor_name, each_neighbor_params in each_device.neighbors.items():
                print(f"    Neighbor Name: {each_neighbor_name}")
                print(f"    Neighbor IP Address : {each_neighbor_params.get('IP address', None)}")
                print(f"    Neighbor Platform : {each_neighbor_params.get('Platform', None)}")
                print(f"    Neighbor Type : {each_neighbor_params.get('Capabilities', None)}")
                print(f"    Self Local Interface : {each_neighbor_params.get('Interface', None)}")
                print(f"    Local VLAN : {each_neighbor_params.get('Native VLAN', None)}")
                print(f"    Neighbor Local Interface : {each_neighbor_params.get('Port ID (outgoing port)', None)}")
                print(f"    Neighbor VLAN : {each_neighbor_params.get('Native VLAN', None)}")

                print("\n")


class Element:
    '''
        Class for defining each element of Adjacenct List
        This is basically the nodes that we will be logging in

        Variables:
            device_ip : Device IP of device
            hostname : Hostname of device
            neighbors = Dictionary of all neighbors of this device

        Functions:
            Login : Login into each of the devices
            calculate_neighbors : Output formatting for data gathered from each neighbor
            Outputs a structure neighbors : {Neighbor1: {Params}, Neighbor N : {Params}}

    '''
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.hostname = ""
        self.neighbors = {}

    def login(self, username, password, secret, device_ip):
        cisco_iou = {
            'device_type': 'cisco_ios',
            'ip' : device_ip,
            'username' : username,
            'password' : password,
            'secret' : secret,
            'verbose' : True
        }
        try:
            net_connect = ConnectHandler(**cisco_iou)
            net_connect.enable()
            net_connect.config_mode()
            #Checks if CDP is enabled
            print(f"Checking for cdp on {cisco_iou['ip']}")
            cdp_check = net_connect.send_command("do show cdp neighbors")
            if "CDP is not enabled" in cdp_check:
                net_connect.send_command("cdp run")
            else:
                print(f"CDP is enabled on this device {cisco_iou['ip']}")
                net_connect.exit_config_mode()
                output = net_connect.send_command("sh cdp neigh det | i (ID|IP add|Plat|Interface|Port ID|VLAN)")


            #Hostname
            find_hostname = net_connect.find_prompt()
            self.hostname = find_hostname.split("#")[0]

            return output


        except (EOFError, NetMikoTimeoutException):
            print('SSH is not enabled for this device.')
            sys.exit()

    def calculate_neighbors(self, output):
        temp = output.split("\n")
        device_data = re.findall("(Device ID: [A-Za-z0-9.]+)\n(\s\sIP address: [\d.]+\n)?(Platform: [a-zA-Z\s]+,)\s\s(Capabilities: [a-zA-Z\s]+\n)(Interface: [A-Za-z0-9\/]+,)\s\s(Port ID .*: [a-zA-Z0-9\/]+)\n(Native VLAN: [\d]+)?", output)

        for device in device_data:
            device_hostname = device[0].split(":")[1]
            self.neighbors[device_hostname] = {}
            for item in device[1:]:
                if item:
                    self.neighbors[device_hostname][item.split(":")[0].strip()] = item.split(":")[1].strip()
            # print(self.neighbors)

def main():
    username = "cisco"
    password = "cisco"
    secret = "cisco"
    # device_ip = [
    #     "192.168.130.251",
    #     "192.168.130.252",
    #     "192.168.130.253"
    # ]

    data = input("Enter all device IPs seperated by space > ")
    if data:
       device_ip = data.strip().split()
    else:
        print("Data format incorrect. You probably pressed enter by mistake")

    Adj_list = AdjacencyList()

    for each_item in device_ip:
        device = Element(each_item)
        neighbor_data = device.login(username, password, secret, each_item)
        device.calculate_neighbors(neighbor_data)
        Adj_list.add_devices(device)

    #Show all devices
    Adj_list.show_devices()

if __name__ == "__main__":
    main()
