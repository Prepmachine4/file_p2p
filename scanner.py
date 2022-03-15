import netifaces
import socket
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

'''局域网扫描'''


class Scanner:

    @staticmethod
    def scan_tools_v1(host):
        port = 21
        sk = socket.socket()
        sk.settimeout(0.1)
        conn_result = sk.connect_ex((host, port))
        if conn_result == 0:
            print('服务器{}的{}端口已开放'.format(host, port))
        sk.close()

    @staticmethod
    def get_gateways():
        return netifaces.gateways()['default'][netifaces.AF_INET][0]

    @staticmethod
    def run():
        prefix = Scanner.get_gateways()
        hosts = [prefix[:-1] + str(host) for host in range(1, 255)]
        executor = ThreadPoolExecutor(max_workers=16)
        all_task = [executor.submit(Scanner.scan_tools_v1, (host)) for host in hosts]
        wait(all_task, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    Scanner.run()
