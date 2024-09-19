import pika
import time

def _ativar(placa):
    f = open("placas_ativadas.txt", "a")
    ts = int(float(time.time()))
    f.write("{} {}\n".format(placa, ts))
    f.close()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='ativacao', durable=True)
print(' [*] Esperando placas para ativação. To exit press CTRL+C')


def callback(ch, method, properties, body):
    placa = body.decode()
    print(f" [x] Recebendo placa: {placa}")
    _ativar(placa)
    print(f" [x] A placa {placa} foi ativada")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='ativacao', on_message_callback=callback)

channel.start_consuming()