import customtkinter #pip install customtkinter
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
import google.generativeai as genai  #pip install google-generativeai

# GUI Theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Gemini API
genai.configure(api_key="")
# Gemini Settings
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048,}
# Gemini Filters
safety_settings = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]
# Gemini Model
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings,
)

gui = customtkinter.CTk() # Start
gui.geometry("850x500") # APP Size
gui.title("Gemini") # APP name

# Change Theme Function
mode = "dark"
def change():
    global mode
    if mode == "dark":
        customtkinter.set_appearance_mode("light")
        mode = "light"
    else:
        customtkinter.set_appearance_mode("dark")
        mode = "dark"

# Save File Function
def save_conversation():
    global chat_history
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text files", "*.txt")]
    )
    if filename:
        with open(filename, "w") as f:
            f.write(chat_history.get(1.0, END))
        gui.destroy()

# Exit APP function
def exitgui():
    answer = messagebox.askquestion("Exit", "Do you want to save the conversation?") #
    if answer == "yes":
        save_conversation()
    elif answer == "no":
        gui.destroy()
    else:
        pass

# Change GUI Theme Function
colorbutton = customtkinter.CTkButton(gui, text="Change Theme",height=25, width=75, font=("Helvetica", 15),command=change)
colorbutton.pack(side=TOP, anchor=NW, padx=8, pady=5)

# Exit Button
exitbutton = customtkinter.CTkButton(gui, text="Exit",height=25, width=75, font=("Helvetica", 13), command= exitgui)
exitbutton.pack(side=TOP, anchor=NW, pady=1, padx=8)

# User Input Box 
inputbox = customtkinter.CTkEntry(gui,width=600, height=50,font=("Helvetica", 17), placeholder_text="    Start a conversation...")
inputbox.pack(side=BOTTOM, pady=10, anchor="center")
inputbox.bind("<Return>", lambda event: send_message()) # Bind "enter" to send user input

# Conversation Box
chat_history = customtkinter.CTkTextbox(gui, width=700, height=750, state="disabled")
chat_history.pack(padx=10, pady=10)

# send user input to gemini and print response in chat_history box
def send_message():
    convo = model.start_chat(history=[])
    user_input = inputbox.get()
    inputbox.delete(0,END)
    convo.send_message(user_input)
    response = convo.last.text
    chat_history.configure(state="normal")
    chat_history.insert(END, f"User:  {user_input}\n")  #print user chat in chat box
    chat_history.insert(END, f"Gemini:  {response}\n")  #print gemini response in chat box
    chat_history.see(END)  #scrolls to the end of the box
    chat_history.configure(state="disabled")

gui.mainloop()