# EASY COMMUNICATIONS

A communications application built in Python using RabbitMQ as the main backbone for message sending and delivering. 
Each instance of the application is both a consumer and producer which is achieved through multithreading. Chatrooms are also supported through the selection of channels as users are subscribed to a receive channel and all messages in that channel are received.
Currently, only local connections are supported for chatting.
The inspiration behind this application was to build a simple yet powerful chat application using RabbitMQ in which the send/receive code can be ported into different applications which require messaging between components/users with relative ease.

## HOW TO USE

Ensure that you have installed the required packages listed in the requirements document.
Run `python main.py`.