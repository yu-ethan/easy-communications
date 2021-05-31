import tkinter as tk, chat

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Easy Communications')
    root.geometry('525x350')
    chat = chat.Chat(root)
    root.protocol("WM_DELETE_WINDOW", chat.close_application)
    root.mainloop()