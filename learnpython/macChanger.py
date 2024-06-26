import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify an new mac, use --help for more info.")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                                          ifconfig_result.decode().strip("\n"))  # read
    # string , pattern is a form of string , learn more in pythex
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read Mac address")


option = get_arguments()

current_mac = get_current_mac(option.interface)
print("current MAC = " + str(current_mac))  # You can use str to modify none type to "None"

change_mac(option.interface, option.new_mac)

current_mac2 = get_current_mac(option.interface)
if current_mac != current_mac2:
    print("[+] MAC address was successfully changed to " + current_mac2)
else:
    print("[+] MAC address was not changed.")
