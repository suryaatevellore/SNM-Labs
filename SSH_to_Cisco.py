from netmiko import ConnectHandler
import re

def does_all_work():
    """Performs the primary function in the file
    Input variables :
        device_ip : IP of the device that we should login to
        username/password : device username/password
    Program variables :
        interfaces = stores the configuration for "show interface"
        ip = stores the configuration for the command "show ip interface brief"
        IP_EXPRESSIONS = regex for extracting information from interfaces
        Expression = regex for extracting information from ip
        choice = choice of the user to pick interface parameters

    Output variables : None , print to stdout

    Flow :
        Ask for device ip -> Login -> Obtain information by making a connection to the router and passing commands -> populate the dictionaries -> Obtain information from the dictionaries according to user choice


    """
    ip_dict = {}
    interfaces_dict = {}
    username = 'cisco'
    password = 'cisco'

    device_ip = raw_input("Provide device IP> ")
    print "Username/password is assumed to be cisco/cisco. Change in username/password will be added later"

    cisco_iou = {
        'device_type': 'cisco_ios',
        'ip' : device_ip,
        'username' : username,
        'password' : password
    }

    net_connect = ConnectHandler(**cisco_iou)
    print("Connection Established")
    print("Sending commands to box")
    interfaces = net_connect.send_command("show interface")
    ip = net_connect.send_command("show ip int br")
    IP_EXPRESSIONS = r"((Gigabit)?Ethernet\d(\/\d)?)\s{1,30}([a-zA-Z0-9.]*)"
    r2 = re.findall(IP_EXPRESSIONS, ip)

    for item in r2:
        ip_dict[item[0]] = item[3]



    EXPRESSION = r"((Gigabit)?Ethernet)(\d(\/\d)?)\s(.*\n)\s\sHardware\sis\s([a-zA-Z0-9\s]*),\saddress\sis\s([a-zA-Z0-9.]*)"
    r1 = re.findall(EXPRESSION,interfaces)


    mac_dict = {}
    type_dict = {}
    for each_interface in r1:
        type_dict[each_interface[0]+each_interface[2]] = each_interface[5]
        mac_dict[each_interface[0]+each_interface[2]] = each_interface[6]
        # interfaces_dict[each_interface[0]+each_interface[2]] = [(each_interface[5],each_interface[6])]

    print ("Data Structures populated")

    #########################################################################
             ## Actual Processing
    #########################################################################

    print("Now, do you wish to search interfaces by \n1.IP\n2.MAC\n3.TYPE. Please Enter your choice")
    choice = int(input(">"))


    if (choice==1):
        ip_address = raw_input("Enter the IP Address of the Interface> ")
        print ip_dict
        try:
            interface_for_ip = ip_dict.keys()[ip_dict.values().index(ip_address)]
            print ("#############################")
            print "Here is the interface" ,interface_for_ip
            print "Other Details..TYPE :" + type_dict[interface_for_ip] + " ....MAC :" + mac_dict[interface_for_ip]
        except ValueError:
            print ("#############################")
            print "The IP does not exist on the box"


    elif (choice==2):
        mac = raw_input("Enter the mac of the interface> ")
        try:
            interface_for_mac = mac_dict.keys()[mac_dict.values().index(mac)]
            print ("#############################")
            print "Here is the interface", interface_for_mac
            print "Other Details..TYPE: " + type_dict[interface_for_mac] + ".......IP: " + ip_dict[interface_for_mac]

        except ValueError:
            print "This mac does not exist on the box"

    elif (choice==3):
        type_interface = raw_input("Enter the type of the interface> ")
        try:
            for k,v in type_dict.items():
                if v==type_interface:
                    print "Interface" + k, "  IP of Interface :" + ip_dict[k], "   MAC for Interface: " + mac_dict[k]
                else:
                    raise ValueError()
        except ValueError:
            print "This interface does not exist on the box"
    else:
        print ("You are a rebel!. But since I am an amateur, could you please pick a value that is stated above ? Thank you!")

    return None


if __name__ == "__main__":

    """Just if the code is called through another program or an app"""
    does_all_work()
