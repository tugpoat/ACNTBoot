#system control helpers.
#requires provisions to be made in sudo/wheel config.

import os

def remount_root_rw():
	os.system("sudo mount -o remount,rw /")

def remount_root_ro():
	os.system("sudo mount -o remount,ro /")

def set_ifconfig(iface, ip, mask):
	os.system("sudo ifconfig ? ? netmask ?", [iface, ip, mask])

def disable_sshd():
	os.system("sudo service ssh stop")
	os.system("sudo service ssh disable")

def enable_sshd():
	os.system("sudo service ssh enable")
	os.system("sudo service ssh start")

def disable_dnsmasq():
	os.system("sudo service dnsmasq disable")
	os.system("sudo service dnsmasq stop")

def enable_dnsmasq():
	os.system("sudo service dnsmasq enable")
	os.system("sudo service dnsmasq start")

def disable_hostapd():
	os.system("sudo service dnsmasq disable")
	os.system("sudo service dnsmasq stop")

def enable_hostapd():
	os.system("sudo service hostapd enable")
	os.system("sudo service hostapd start")

def write_ifconfig(prefs):
	with open("/etc/network/interfaces.default") as defaultconf:
	data=defaultconf.readlines()
	defaultconf.close()

	data.append("#-----Managed by CANTBoot, don't touch")
	data.append("auto lo")
	data.append("iface lo inet loopback")


	with open ("/etc/network/interfaces", "rw") as outfile:

	data.append("auto eth0")
	if prefs.get('Network', 'eth0_mode') == 'static':
		data.append("iface eth0 inet static")
		data.append("address ?", [prefs.get('Network', 'eth0_ip')])
		data.append("netmask ?", [prefs.get('Network', 'eth0_netmask')])

		#TODO: do bitwise operations to figure out the network and bcast from ip and mask.
		#data.append("network ?", [])
		data.append("network ?", [prefs.get('Network', 'eth0_network')])
		data.append("broadcast ?", [prefs.get('Network', 'eth0_bcast')])

	data.append("allow-hotplug wlan0")
	if prefs.get('Network', 'wlan0_ip') == 'dhcp' || prefs.get('Network', 'wlan0_subnet') == 'dhcp':
		#DHCP setting
	else:
		data.append("iface wlan0 inet static")
		data.append("address ?", [prefs.get('Network', 'wlan0_ip')])
		data.append("netmask ?", [prefs.get('Network', 'wlan0_netmask')])
		data.append("network ?", [prefs.get('Network', 'wlan0_network')])
		data.append("broadcast ?", [prefs.get('Network', 'wlan0_bcast')])

	outfile.writelines(data)
	outfile.close()
