def detect_vendor(output: str) -> str:

    text = output.lower()

    if "cisco ios" in text or "catalyst" in text:
        return "cisco"

    if "huawei" in text or "vrp" in text:
        return "huawei"

    if "juniper" in text or "junos" in text:
        return "juniper"

    if "aruba" in text:
        return "aruba"

    if "mikrotik" in text or "routeros" in text:
        return "mikrotik"

    return "unknown"
