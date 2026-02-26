from vendors.base_vendor import BaseVendor


class CiscoVendor(BaseVendor):

    def __init__(self, prefix="Gi1/0/"):
        self.prefix = prefix

    def build_interfaces(self, interfaces):

        return [f"{self.prefix}{i}" for i in interfaces]

    def access_port(self, interfaces, vlan):

        cmds = []

        portas = self.build_interfaces(interfaces)

        if len(portas) > 1:
            portas_str = ",".join(portas)
            cmds.append(f"interface range {portas_str}")
        else:
            cmds.append(f"interface {portas[0]}")

        cmds.extend([
            "switchport mode access",
            f"switchport access vlan {vlan}",
            "exit"
        ])

        return cmds
