from vendors.base_vendor import BaseVendor


class HuaweiVendor(BaseVendor):

    def __init__(self):
        # Prefixo padrão Huawei
        self.prefix = "GigabitEthernet0/0/"

    def build_interfaces(self, interfaces):

        return [f"{self.prefix}{i}" for i in interfaces]

    def access_port(self, interfaces, vlan):

        cmds = []

        portas = self.build_interfaces(interfaces)

        if len(portas) > 1:
            portas_str = " ".join(portas)
            cmds.append(f"interface range {portas_str}")
        else:
            cmds.append(f"interface {portas[0]}")

        cmds.extend([
            "port link-type access",
            f"port default vlan {vlan}",
            "quit"
        ])

        return cmds
