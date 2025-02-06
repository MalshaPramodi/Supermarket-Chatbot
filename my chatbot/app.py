from tkinter import *
from tkinter import messagebox 
from main import get_response, bot
import pyttsx3 as pp

engine = pp.init()
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1].id)

shelves_requested = {}

#Make chatbot speak
def speak(word):
    engine.say(word)
    engine.runAndWait()
    
def repeat():
    pass

#Set UI 
BG_GRAY = "#EAEAEA"
BG_COLOR = "#2C3E50"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#1ABC9C"
ENTRY_COLOR = "#34495E"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()        
        
    def _setup_main_window(self):
        self.window.title("Supermarket Chatbot")
        self.window.iconbitmap('grocery_Cart.ico')  # Set the icon here
        self.window.resizable(width =False, height = False)
        self.window.configure(width=600, height = 700, bg = BG_COLOR)
        
        #Head Label
        head_label = Label(self.window, bg = BG_COLOR, fg = TEXT_COLOR, text = "Welcome to Supermarket\nType 'quit' to end the conversation.", font = FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow",state=DISABLED)
        
        #Scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        #bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry =Entry(bottom_label, bg=ENTRY_COLOR, fg = TEXT_COLOR, font =FONT)
        self.msg_entry.place(relwidth=0.74,relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        #send button
        send_button = Button(bottom_label, text="Enter", font=FONT_BOLD, width=20, bg=BUTTON_COLOR, fg=TEXT_COLOR, command=lambda:self._on_enter_pressed(None))    
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        
        init_response = "Hello, I'm your Chatbot. I'm happy to help you. \nI can tell the shelf numbers of the goods you need to buy. \nPlease enter them one by one"
        msg_init = f"{bot}:{init_response}\n\n"
       
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg_init)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
        
        self.window.after(1000, lambda: speak(init_response))
        
        # Send message when enter key is pressed
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
        if msg.lower() == 'quit':
            self._end_chat()
        else:
            response = get_response(msg)
            self._insert_message(response, bot)
            speak(response)

            # Track goods and their associated shelves
            if "Shelf number" in response:
                shelf_number = response.split("Shelf number ")[-1].split(".")[0].strip()
                goods = ", ".join(msg.split())  # Assuming msg contains goods
                if shelf_number not in shelves_requested:
                    shelves_requested[shelf_number] = []
                shelves_requested[shelf_number].append(goods)

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
    def _end_chat(self):
        # Generate document with shelves and associated goods
        if shelves_requested:
            self._generate_document(shelves_requested)
        else:
            messagebox.showinfo("Chatbot", "No shelves were requested.")

        self.window.quit()

    def _generate_document(self, shelves):
        # Create a text file with shelves and associated goods
        doc_filename = "requested_shelves.txt"
        with open(doc_filename, 'w') as f:
            f.write("Requested Shelves and Goods:\n")
            for idx, (shelf_number, goods_list) in enumerate(shelves.items(), 1):
                goods_str = ", ".join(goods_list)
                f.write(f"{idx}. Shelf number {shelf_number}: {goods_str}\n")

        messagebox.showinfo("Chatbot", f"Document saved: {doc_filename}")


if __name__ == "__main__":
    app = ChatApplication()
    app.run()
