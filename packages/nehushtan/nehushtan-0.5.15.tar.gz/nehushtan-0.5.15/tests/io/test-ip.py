import socket

import psutil


def get_local_ip():
    addresses = psutil.net_if_addrs()

    for interface, addr_list in addresses.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
                if ip_address != '127.0.0.1':
                    return ip_address

    return '127.0.0.1'


if __name__ == '__main__':
    print(get_local_ip())