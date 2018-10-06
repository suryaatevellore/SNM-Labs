from netmiko import ConnectHandler


#Use this for threading
username = "cisco"
password = "cisco"
secret = "cisco"
device_ip = [
    "192.168.130.250",
    "192.168.130.251",
    "192.168.130.252"
]

devices_cdp_output = {}
for item in device_ip:
    cisco_iou = {
            'device_type': 'cisco_ios',
            'ip' : item,
            'username' : username,
            'password' : password,
            'secret' : secret,
            'verbose' : True
        }

    #Need to add error handling here but otherwise the code works and configures cdp
    net_connect = ConnectHandler(**cisco_iou)
    # print("Check prompt at login")
    # print(net_connect.find_prompt())
    net_connect.enable()
    net_connect.config_mode()
    cdp_flag = net_connect.send_command("do show cdp neighbors")
    if "CDP is not enabled" in cdp_flag:
        net_connect.send_command("cdp run")
        print(net_connect.find_prompt())

    else:
        print("CDP seems to be already enabled")

    net_connect.exit_config_mode()
    output = net_connect.send_command("sh cdp ne d | inc (ID|IP add|Plat|Interface|Port ID)")

    print(output.split("\n"))
    #Perform processing on output



    # devices_cdp_output[item] = output.split("\n")[4:]
    net_connect.disconnect()

# print(devices_cdp_output)

#paramiko.ssh_exception.AuthenticationException: Authentication timeout.
