import time
import pika
from servidor.funcoes_do_servidor import _verificando_conexao

# from servidor.funcoes_do_servidor import _ativar
from servidor.funcoes_do_servidor import _consultar


def conectando(nome):
    print("conectando ...")
    time.sleep(3)
    print(_verificando_conexao(nome))
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
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()
        channel.queue_declare(queue="ativacao", durable=True)
        channel.basic_publish(
            exchange="",
            routing_key="ativacao",
            body=placa,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        print(f" Placa {placa} está sendo ativada.")
        connection.close()
    except:
        print("Não foi possível conectar, tente mais tarde.")


def ativar():
    print("-" * 20)
    print("ATIVAR PLACA")
    placa = input("Digite a placa:")
    _ativar(placa)


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


# print("-" * 20)
# print("Bem vindo ao sistema de estacionamento rotativo!")
# nome = input("Digite seu nome, e tecle enter:")
# conectando(nome)

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
        print("\033[32m" + "\nTchal!\n" + "\033[0;0m")
        break
    else:
        print("\033[31m" + "\nOpção inválida.\n" + "\033[0;0m")
        continue
