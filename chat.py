import tkinter as tk, send_msg, receive_msg, threading

class Chat:
    def __init__(self, master):
        self.master = master
        self.send_route = tk.StringVar(self.master, '')
        self.receive_route = tk.StringVar(self.master, '')
        self.username = None
        self.send_thread = None
        self.receive_thread = None
        self.landing_page()
        self.textbox = None
    
    def chat_page(self):
        display_name_label = tk.Label(self.master, text='Display Name: {}'.format(self.username), font=('Courier', 20))
        display_name_label.grid(row=0,column=0, columnspan=3, sticky='W')
        send_label = tk.Label(self.master, text='Send Message')
        send_label.grid(row=2, sticky='W')
        self.msg_entry = tk.Entry(self.master)
        self.msg_entry.grid(row=2,column=1)
        self.msg_entry.bind('<Return>', func=lambda x:self.send_msg_clear_entry())
        send_button = tk.Button(self.master, text='Send', command=self.send_msg_clear_entry)
        send_button.grid(row=2,column=2, sticky='W')

        self.textbox = tk.Text(self.master, height=20,width=50)
        self.textbox.grid(row=1,column=0,columnspan=2)
        self.textbox.config(state=tk.DISABLED)
        scrollbar = tk.Scrollbar(self.master, command=self.textbox.yview)
        scrollbar.grid(row=1,column=3, sticky='NSW')
        self.textbox['yscrollcommand'] = scrollbar.set

        quit_button = tk.Button(self.master, text='QUIT', command=self.close_application, font=('Courier', 14))
        quit_button.grid(row=3,column=1)
        send_ch_label = tk.Label(self.master, text='Sending: {}'.format(self.send_route.get()), fg='#0f0')
        send_ch_label.grid(row=3,column=0,sticky='W')
        rec_ch_label = tk.Label(self.master, text='Receiving: {}'.format(self.receive_route.get()), fg='#0f0')
        rec_ch_label.grid(row=3,column=2)

        self.start_thread()
        send_msg.chat_connection(self.send_route.get(), self.username, True, self.textbox)

    def start_thread(self):
        self.receive_thread = threading.Thread(target=lambda: receive_msg.receive_msg(self.receive_route.get(), self.textbox, self.username))
        self.receive_thread.setDaemon(True)
        self.receive_thread.start()

    def send_msg_clear_entry(self):
        send_msg.send(self.send_route.get(), self.msg_entry.get(), self.textbox, self.username)
        self.msg_entry.delete(0, tk.END)
    
    def close_application(self):
        if self.textbox != None:
            send_msg.chat_connection(self.send_route.get(), self.username, False, self.textbox)
        self.master.quit()

    def landing_page(self):
        username_label = tk.Label(self.master, text='Display Name: ')
        username_label.grid(row=1, pady=(30,0))
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=1,column=1, pady=(30,0))
        send_label = tk.Label(self.master, text='Choose a Send Channel')
        send_label.grid(row=2,column=0,columnspan=3,pady=(20,10))
        receive_label = tk.Label(self.master, text='Choose a Receive Channel')
        receive_label.grid(row=4,column=0,columnspan=3,pady=(20,10))

        send_channel1 = tk.Radiobutton(self.master, text='Channel 1', variable=self.send_route, value='Channel 1')
        send_channel2 = tk.Radiobutton(self.master, text='Channel 2', variable=self.send_route, value='Channel 2')
        send_channel3 = tk.Radiobutton(self.master, text='Channel 3', variable=self.send_route, value='Channel 3')
        send_buttons = [send_channel1,send_channel2,send_channel3]
        
        receive_channel1 = tk.Radiobutton(self.master, text='Channel 1', variable=self.receive_route, value='Channel 1')
        receive_channel2 = tk.Radiobutton(self.master, text='Channel 2', variable=self.receive_route, value='Channel 2')
        receive_channel3 = tk.Radiobutton(self.master, text='Channel 3', variable=self.receive_route, value='Channel 3')
        receive_buttons = [receive_channel1,receive_channel2,receive_channel3]

        for i in range(3):
            send_buttons[i].grid(row=3,column=i)
            receive_buttons[i].grid(row=5,column=i)

        submit = tk.Button(self.master, text='Continue', command=self.proceed_to_chatpage)
        submit.grid(row=6,column=0,columnspan=3,pady=(30,10))

        self.error_label = tk.Label(self.master, text='', fg='#f00')
        self.error_label.grid(row=7,column=0, columnspan=3)

    def proceed_to_chatpage(self):
        if self.validate_username():
            return
        if self.display_channel_error():
            return
        self.clear()
        self.chat_page()
    
    def clear(self):
        slaves = self.master.grid_slaves()
        for x in slaves:
            x.destroy()
    
    def display_channel_error(self):
        error = False
        if self.send_route.get() == '' or self.receive_route.get() == '':
            self.error_label.config(text='Please select send/receive channels.')
            error = True
        return error
    
    def validate_username(self):
        error = False
        if self.username_entry.get() == '':
            self.error_label['text'] = 'Please enter a display name!'
            error = True
        elif self.username_entry.get() == 'You':
            self.error_label['text'] = 'Invalid display name. Please enter different display name.'
            error = True
        if not error:
            self.username = self.username_entry.get()
        return error