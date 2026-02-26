import os

from core.nlp_parser import parse_text_to_intent
from core.auto_brain import auto_generate


# ==========================
# SIMULADOR MULTI-VENDOR
# ==========================
def fake_show_version(opcao):

    if opcao == "1":
        return "Cisco IOS Software, Catalyst Switch Version 15.2"

    if opcao == "2":
        return "Huawei Versatile Routing Platform Software VRP"

    return "Cisco IOS Software"


# ==========================
# LIMPAR TELA
# ==========================
def clear():
    os.system("cls")


# ==========================
# HEADER
# ==========================
def header():
    print("\n===============================")
    print(" ACE NET • Network Copilot CLI ")
    print("===============================\n")


# ==========================
# MENU PRINCIPAL
# ==========================
def escolher_vendor():

    print("Escolha o Vendor (Simulação):")
    print("1 - Cisco")
    print("2 - Huawei")
    print("0 - Sair")

    opcao = input("\nDigite o número: ")

    return opcao


# ==========================
# LOOP PRINCIPAL
# ==========================
def main():

    while True:

        clear()
        header()

        opcao = escolher_vendor()

        if opcao == "0":
            print("\nEncerrando ACE NET...\n")
            break

        if opcao not in ["1", "2"]:
            print("\nOpção inválida.")
            input("ENTER para continuar...")
            continue

        version_output = fake_show_version(opcao)

        print("\nModo SIMULAÇÃO ATIVO.")
        print("Digite comando humano.")
        print("Ex: porta 10 vlan 30")
        print("Digite 'voltar' para menu.\n")

        while True:

            texto = input("ACE_NET> ")

            if texto.lower() == "voltar":
                break

            try:

                intent = parse_text_to_intent(texto)

                vendor, cmds = auto_generate(version_output, intent)

                print("\nFabricante detectado:", vendor)
                print("\nComandos gerados:\n")

                for c in cmds:
                    print(" ", c)

                print("\n[SIMULAÇÃO] Nenhum comando foi enviado.\n")

            except Exception as e:
                print("\nErro:", e, "\n")


# ==========================
# START
# ==========================
if __name__ == "__main__":
    main()
