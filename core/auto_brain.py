from core.device_detector import detect_vendor
from core.executor import generate_commands


# ==========================
# DETECTA PREFIXO REAL
# ==========================
def detect_prefix(show_version_output, vendor):

    text = show_version_output.lower()

    if vendor == "cisco":

        # exemplos reais possíveis
        if "catalyst" in text:
            return "Gi1/0/"
        if "2960" in text:
            return "Fa0/"
        if "9300" in text:
            return "Gi1/0/"
        if "9500" in text:
            return "Te1/0/"

        return "Gi1/0/"

    if vendor == "huawei":

        if "vrp" in text:
            return "GigabitEthernet0/0/"

        return "GigabitEthernet0/0/"

    return ""


# ==========================
# AUTO GENERATE
# ==========================
def auto_generate(show_version_output, intent):

    vendor = detect_vendor(show_version_output)

    if vendor == "unknown":
        raise Exception("Fabricante não identificado")

    prefix = detect_prefix(show_version_output, vendor)

    commands = generate_commands(vendor, intent, prefix)

    return vendor, commands
