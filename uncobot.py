@author: gnaneswari
"""
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
uncobot1 = ChatBot('GGBot',trainer='chatterbot.trainers.ListTrainer')
#,storage_adapter="chatterbot.storage.SQLStorageAdapter")
import speech_recognition as s
import threading
import pyttsx3 as pp
engine = pp.init()
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1].id)
#call speak from ask_from_bot function
def speak(words):
    engine.say(words)
    engine.runAndWait()

# create the dialog file
conversation=open('ggsamplebot.csv','r').readlines()
#set the trainer
print('Training the bot . . .  ')
#train
uncobot1.train(conversation)
#UI
#=============================================================================
main = Tk()
main.geometry("600x650")
#Unusually amazing person
main.title("GG Unco bot")
img = PhotoImage(file="bot.png")
photoL = Label(main,image=img)
photoL.pack(pady=5)
#=============================================================================
#take query : it takes audio as input from user and convert it to string..
def takeQuery():
    sr = s.Recognizer()
    sr.pause_threshold = 1
    print("Uncobot is listening . . . ")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            #print(query)
            textF.delete(0, END)
            textF.insert(0, query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print("not recognized")
def ask_from_bot():
    query = textF.get()
    answer_from_bot = uncobot1.get_response(query)
    msgs.insert(END, "You : " + query)
    print(type(answer_from_bot))
    msgs.insert(END, "GG bot : " + str(answer_from_bot))
    speak(answer_from_bot)
    textF.delete(0, END)
    #makes it vertically scrollable
    msgs.yview(END)
frame = Frame(main)
sc = Scrollbar(frame)
msgs = Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10)
frame.pack()

# creating text field
textF = Entry(main, font=("Courier", 12))
textF.pack(fill=X, pady=10)
btn = Button(main, text=" bot", font=(
    "Courier", 10),bg='red', command=ask_from_bot)
btn.pack()

# creating a function
def enter_function(event):
    btn.invoke()

# going to bind main window with enter key...
main.bind('<Return>', enter_function)

def repeatL():
    while True:
        takeQuery()

t=threading.Thread(target=repeatL)
t.start()
        
main.mainloop()