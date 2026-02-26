from vendors.cisco import CiscoVendor
from vendors.huawei import HuaweiVendor


def get_vendor(vendor_name, prefix):

    if vendor_name == "cisco":
        return CiscoVendor(prefix)

    if vendor_name == "huawei":
        return HuaweiVendor()

    raise Exception(f"Vendor não suportado: {vendor_name}")


def generate_commands(vendor_name, intent, prefix):

    vendor = get_vendor(vendor_name, prefix)

    if intent["action"] == "access_port":

        return vendor.access_port(
            intent["interfaces"],
            intent["vlan"]
        )

    raise Exception("Ação não suportada")
