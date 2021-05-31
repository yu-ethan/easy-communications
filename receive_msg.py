import pika, tkinter as tk

def receive_msg(route, textbox, username):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(route, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=route, queue=queue_name)

    def callback(ch, method, properties, body):
        message = body.decode('utf-8')
        if message[:message.find(':')] != username:
            textbox.config(state=tk.NORMAL)
            textbox.insert(tk.END, message)
            textbox.see(tk.END)
            textbox.config(state=tk.DISABLED)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    channel.start_consuming()
