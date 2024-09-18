import time
import math


def _ativar(placa):
    f = open("placas_ativadas.txt", "a")
    ts = int(float(time.time()))
    f.write("{} {}\n".format(placa, ts))
    f.close()


def _consultar(placa):
    placas = {}
    with open("placas_ativadas.txt", "r") as arquivo:
        linhas = arquivo.read().split("\n")
    for linha in linhas:
        if linha:
            plc = linha.split(" ")[0]
            timestamp = linha.split(" ")[1]
            placas[plc] = int(float(timestamp))

    if placa not in placas:
        return (placa, False, None)

    tempo = math.floor((time.time() - placas[placa]) / 60)

    if tempo > 60:
        return (placa, False, tempo - 60)

    return (placa, True, 60 - tempo)


def _verificando_conexao(nome):
    saida = (
        "\033[32m"
        + "\nOlá "
        + nome
        + ", você está conectado ao servidor!\n"
        + "\033[0;0m"
    )
    return saida
