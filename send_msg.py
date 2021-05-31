import pika, tkinter as tk

def send(route, message, textbox, username):
    if not message:
        return
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(route,exchange_type='fanout')
    send_message='{}: {}\n'.format(username, message)
    channel.basic_publish(exchange=route, routing_key='', body=send_message)
    textbox.config(state=tk.NORMAL)
    textbox.insert(tk.END, 'You: {}\n'.format(message))
    textbox.see(tk.END)
    textbox.config(state=tk.DISABLED)

    connection.close()

def chat_connection(route, username, joining, textbox):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(route,exchange_type='fanout')
    if joining:
        send_message = '{} has joined the chat.\n'.format(username)
    else:
        send_message = '{} has left the chat.\n'.format(username)
    channel.basic_publish(exchange=route, routing_key='', body=send_message)
    textbox.config(state=tk.NORMAL)
    textbox.insert(tk.END, send_message)
    textbox.see(tk.END)
    textbox.config(state=tk.DISABLED)
    connection.close()