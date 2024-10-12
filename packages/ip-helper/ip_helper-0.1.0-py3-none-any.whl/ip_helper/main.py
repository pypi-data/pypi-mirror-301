# usr/bin/python
""" IP helper take ip/submask as the input and give detail for that subnet """
from ip_helper.library.ipv4 import IPV4
from ip_helper.library.ipv6 import IPV6
from ip_helper.library.ip_schema import IPAddressModel
import argparse
import configparser


def main():
    parser = argparse.ArgumentParser(
        prog="IP Helper", description="Calculate subnet details"
    )
    parser.add_argument("subnet", type=str, help="Enter subnet in format IP/submask")
    args = parser.parse_args()
    valid_input = IPAddressModel(address=args.subnet)
    # Need validate the subnet argument format
    ip = str(valid_input.address.ip)
    submask = str(valid_input.address.network.prefixlen)

    ip = IPV4(ip=ip, submask_len=int(submask))
    print(f"IP Address: {ip.get_ip()}")
    print(f"Network Address: {ip.get_ip_network_address()}")
    print(f"Usable Host IP Range: {ip.get_ip_range()}")
    print(f"Broadcast Address: {ip.get_ip_broadcast_address()}")
    print(f"Total Number of Hosts: {ip.get_ip_available()}")
    print(f"Number of Usable Hosts {ip.get_ip_usable()}")
    print(f"Subnet Mask: {ip.get_submask_in_ip()}")
    print(f"Wildcard Mask: {ip.get_wildcard_mask_in_ip()}")
    print(f"Binary Subnet Mask: {ip.get_submask_in_binary()}")
    print(f"CIDR Notation: /{submask}")
    print(f"IP Type: {ip.get_ip_type()}")


if __name__ == "__main__":
    main()
