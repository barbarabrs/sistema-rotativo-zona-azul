import pika
import time
import math

def on_message_received(ch, method, properties, body):
    print(f"received new message: {body}")
    print("-" * 20)
    print("Bem vindo ao sistema de estacionamento rotativo!")
    nome = input("Digite seu nome, e tecle enter:")
    conectando(nome)

    while True:
        menu()
        opcao = input()

        if opcao == "1":
            ativar()
            if outra_operacao():
                continue
            break
        elif opcao == "2":
            consultar()
            if outra_operacao():
                continue
            break
        elif opcao == "3":
            print("\033[32m" + "\nTchau!\n" + "\033[0;0m")
            break
        else:
            print("\033[31m" + "\nOpção inválida.\n" + "\033[0;0m")
            continue
def conectando(nome):
    print("conectando ...")
    time.sleep(3)
    print(
        "\033[32m"
        + "\nOlá "
        + nome
        + ", você está conectado ao servidor!\n"
        + "\033[0;0m"
    )
    print("carregando ...")
    time.sleep(3)


def menu():
    print("-" * 20)
    print("O que deseja fazer?")
    print("Digite 1 para ativar uma placa.")
    print("Digite 2 para consultar uma placa.")
    print("Digite 3 para sair do programa.")
    print("Depois tecle Enter.")


def _ativar(placa):
    f = open("placas_ativadas.txt", "a")
    ts = int(float(time.time()))
    f.write("{} {}\n".format(placa, ts))
    f.close()


def ativar():
    print("-" * 20)
    print("ATIVAR PLACA")
    placa = input("Digite a placa:")
    _ativar(placa)


def _consultar(placa):
    placas = {}
    with open("placas_ativadas.txt", "r") as arquivo:
        linhas = arquivo.read().split("\n")
    for linha in linhas:
        if linha:
            plc = linha.split(" ")[0]
            timestamp = linha.split(" ")[1]
            placas[plc] = int(float(timestamp))

    if not placas[placa]:
        return (placa, False, None)

    tempo = math.floor((time.time() - placas[placa]) / 60)

    if tempo > 60:
        return (placa, False, tempo - 60)

    return (placa, True, 60 - tempo)


def consultar():
    print("-" * 20)
    print("CONSULTAR PLACA")
    placa = input("Digite a placa:")
    consulta = _consultar(placa)
    if not consulta[1] and not consulta[2]:
        print("\033[31m" + "\nA placa não está ativada!\n" + "\033[0;0m")
    elif not consulta[1] and consulta[2]:
        print(
            "\033[33m"
            + "\nO tiket foi expirado a "
            + str(consulta[2])
            + " minutos.\n"
            + "\033[0;0m"
        )
    elif consulta[1]:
        print(
            "\033[32m"
            + "\nO tiket está ativado. Faltam "
            + str(consulta[2])
            + " minutos.\n"
            + "\033[0;0m"
        )


def outra_operacao():
    resposta = input("\nDeseja fazer outra operação? (S/n)\n")
    return not resposta == "n"


connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue = 'letterbox')
channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=on_message_received)

print("Start Consuming")

channel.start_consuming()







