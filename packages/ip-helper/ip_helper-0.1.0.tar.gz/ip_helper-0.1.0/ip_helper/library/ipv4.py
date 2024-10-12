class IPV4:
    def __init__(self, ip: str, submask_len: int) -> None:
        """Take ip and submask_len as input"""
        self.length = 32
        self.ip = ip
        self.submask_len = submask_len

    def get_ip(self) -> str:
        return self.ip

    def get_ip_available(self) -> int:
        """This function take the submask_len as input, return the amonut of aviailable IPs"""
        return 2 ** (32 - int(self.submask_len))

    def get_ip_usable(self) -> int:
        """This fucntion take the submask_len as input, return the amount of usable IPs"""
        # Corner case is when submask len is 32, no negative will return
        return 0 if self.submask_len == 32 else (2 ** (32 - int(self.submask_len)) - 2)

    def get_submask_in_ip(self) -> str:
        """This function take the submask_len as intput, return submask in IP format"""
        submask_in_binary = "1" * self.submask_len + "0" * (
            self.length - self.submask_len
        )
        first_octlet = int(submask_in_binary[0:8], 2)
        second_octlet = int(submask_in_binary[8:16], 2)
        third_octlet = int(submask_in_binary[16:24], 2)
        fourth_octlet = int(submask_in_binary[24:32], 2)
        return f"{first_octlet}.{second_octlet}.{third_octlet}.{fourth_octlet}"

    def get_submask_in_binary(self) -> str:
        return self.convert_ip_to_binary(self.get_submask_in_ip())

    def get_wildcard_mask_in_ip(self) -> str:
        """This function take the submask_len as input, return wildcard mask in IP format"""
        submask_in_binary = "0" * self.submask_len + "1" * (
            self.length - self.submask_len
        )
        first_octlet = int(submask_in_binary[0:8], 2)
        second_octlet = int(submask_in_binary[8:16], 2)
        third_octlet = int(submask_in_binary[16:24], 2)
        fourth_octlet = int(submask_in_binary[24:32], 2)
        return f"{first_octlet}.{second_octlet}.{third_octlet}.{fourth_octlet}"

    def convert_ip_to_binary(self, ip_in_int: str) -> str:
        """Convert IP address from int format to binary format"""
        ip_divided_by_octlet = ip_in_int.split(".")
        output = []
        for octlet in ip_divided_by_octlet:
            all_zero_octlet = ["0"] * 8
            octlet_in_binary = str(bin(int(octlet))[2:])
            for i in range(len(octlet_in_binary)):
                if octlet_in_binary[i] == "1":
                    all_zero_octlet[8 - len(octlet_in_binary) + i] = "1"
            output.append("".join(all_zero_octlet))

        return ".".join(output)

    def convert_binary_to_ip(self, ip_in_binary: str) -> str:
        """Convert IP address from binary format to int format"""
        ip_divided_by_octlet = ip_in_binary.split(".")
        output = []
        for octlet in ip_divided_by_octlet:
            octlet_in_int = int(octlet, 2)
            output.append(str(octlet_in_int))
        return ".".join(output)

    def get_ip_network_address(self) -> str:
        """Do bitwise AND operation on ip and submask to get the network address of the subnet"""
        ip_divided_by_octlet = self.convert_ip_to_binary(self.ip).split(".")
        submask_divided_by_octlet = self.convert_ip_to_binary(
            self.get_submask_in_ip()
        ).split(".")
        output = []
        for i in range(4):
            bitwise_and = int(ip_divided_by_octlet[i], 2) & int(
                submask_divided_by_octlet[i], 2
            )
            output.append(str(bitwise_and))
        return ".".join(output)

    def get_ip_broadcast_address(self) -> str:
        """Do bitwise OR operation on ip and wildcard mask to get the broadcast address of the subnet"""
        ip_divided_by_octlet = self.convert_ip_to_binary(self.ip).split(".")
        submask_divided_by_octlet = self.convert_ip_to_binary(
            self.get_wildcard_mask_in_ip()
        ).split(".")
        # print(ip_divided_by_octlet) # uncomment for debugging
        # print(submask_divided_by_octlet) # uncomment for debugging
        output = []
        for i in range(4):
            bitwise_and = int(ip_divided_by_octlet[i], 2) | int(
                submask_divided_by_octlet[i], 2
            )
            output.append(str(bitwise_and))
        return ".".join(output)

    def get_ip_range(self) -> str:
        """Calculate usable ip range"""
        # Corner case, when submask length is 31 or 32, no usable IP
        if self.submask_len == 31 or self.submask_len == 32:
            return "NA"
        # first ip is the network address + 1
        ip_divided_by_octlet = self.get_ip_network_address().split(".")
        ip_divided_by_octlet[3] = str(int(ip_divided_by_octlet[3]) + 1)
        first_ip = ".".join(ip_divided_by_octlet)
        # last ip is the broadcast address - 1
        ip_divided_by_octlet = self.get_ip_broadcast_address().split(".")
        ip_divided_by_octlet[3] = str(int(ip_divided_by_octlet[3]) - 1)
        last_ip = ".".join(ip_divided_by_octlet)
        return f"{first_ip} ~ {last_ip}"

    def get_ip_type(self) -> str:
        """Check if ip is public or private"""
        # Private IP range
        # 10.0.0.0 to 10.255.255.255
        # 172.16.0.0 to 172.31.255.255
        # 192.168.0.0 to 192.168.255.255
        return (
            "Private"
            if self.check_if_ip_in_subnet(self.ip, "10.0.0.0/8")
            or self.check_if_ip_in_subnet(self.ip, "172.16.0.0/12")
            or self.check_if_ip_in_subnet(self.ip, "192.168.0.0/16")
            else "Public"
        )

    def check_if_ip_in_subnet(self, ip, subnet) -> bool:
        """To check if the ip in a subnet or not, return a boolen value"""
        subnet_ip = subnet.split("/")[0]
        subnet_submask = int(subnet.split("/")[1])
        ip_network_address_in_binary = self.convert_ip_to_binary(ip).replace(".", "")[
            0:subnet_submask
        ]
        subnet_network_address_in_binary = self.convert_ip_to_binary(subnet_ip).replace(
            ".", ""
        )[0:subnet_submask]

        return ip_network_address_in_binary == subnet_network_address_in_binary
