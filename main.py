"""
Just something to make my life easier :)
PS. This is my attempt at trying to make code as unreadable as possible
"""
import netifaces as ni
from colorama import Fore, Style
from pwn import *

type_of_payloads = ['Reverse Shell', 'Shellcode']
def main():
    choose_payload()

def rev_payload(ip: str, port: int):
    print()

"""

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
    # Only call the function if the reverse shell payload is selected
    choose_interface() if chosen_type_of_payload == 0 else ""

"""This function only generates like a shell payload, I understand very very very little about shellcode and thought this would be a good reason to learn
"""
# def shellcode():
#     context(arch="amd64", os="linux")
#     code = b''
#     code += asm(shellcraft.sh())
if __name__ == "__main__":
    main()