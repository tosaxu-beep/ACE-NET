import re


def parse_ports(texto):

    # portas 1-5
    intervalo = re.search(r"portas?\s+(\d+)\s*-\s*(\d+)", texto)
    if intervalo:
        inicio = int(intervalo.group(1))
        fim = int(intervalo.group(2))
        return list(range(inicio, fim + 1))

    # portas 1,2,3
    lista = re.search(r"portas?\s+([\d,]+)", texto)
    if lista:
        portas = lista.group(1).split(",")
        return [int(p) for p in portas]

    # porta única
    unica = re.search(r"porta\s+(\d+)", texto)
    if unica:
        return [int(unica.group(1))]

    raise Exception("Não encontrei porta válida")


def parse_text_to_intent(text: str):

    text = text.lower()

    portas = parse_ports(text)

    vlan_match = re.search(r"vlan\s+(\d+)", text)

    if not vlan_match:
        raise Exception("VLAN não encontrada")

    vlan = int(vlan_match.group(1))

    intent = {
        "action": "access_port",
        "interfaces": portas,
        "vlan": vlan
    }

    return intent
