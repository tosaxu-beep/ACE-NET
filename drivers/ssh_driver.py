from netmiko import ConnectHandler


def send_config(device, commands):

    with ConnectHandler(**device) as conn:
        output = conn.send_config_set(commands)
        return output


def get_port_status(device):

    with ConnectHandler(**device) as conn:

        output = conn.send_command("show interface status")

    ports = {}

    lines = output.splitlines()

    for line in lines:

        if "Gi" in line:

            parts = line.split()

            interface = parts[0]

            if "connected" in line:
                ports[interface] = "up"
            elif "notconnect" in line:
                ports[interface] = "down"
            else:
                ports[interface] = "unknown"

    return ports


# ==========================
# HEALER ENGINE
# ==========================
def analyze_ports(portmap):

    suggestions = []

    for port,status in portmap.items():

        if status == "down":
            suggestions.append(f"{port} → verificar cabo ou dispositivo")

        if status == "unknown":
            suggestions.append(f"{port} → verificar configuração ou VLAN")

    return suggestions
