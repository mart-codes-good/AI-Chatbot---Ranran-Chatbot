from ranbotapi import get_llm_response
from tkinter import *
from PIL import Image, ImageSequence, ImageTk

window = Tk()

def typing_sfx(label, text, index=0):
    if index < len(text):
        label.config(text=text[:index+1])
        window.after(100, typing_sfx, label, text, index+1)

def chat():
    usr_message = usr_txt.get() # this is the prompt
    response = get_llm_response(usr_message)
    typing_sfx(ran_res, response)
    print(response)
    usr_txt.delete(0, END)

def endchat():
    typing_sfx(ran_res, "Laterr, beeeswwaax!")
    window.after(5000, window.quit)

window.title("RanRan ChatBot")
icon = PhotoImage(file="images/rrbicon.png")
window.wm_iconphoto(True, icon)
window.geometry("600x500")
window.config(background="#E6E6FA")

idle = Image.open("gifs/idlerrb.gif")
new_size = (200,200)
frames = [ImageTk.PhotoImage(frame.convert("RGBA").resize(new_size, Image.Resampling.LANCZOS)) 
          for frame in ImageSequence.Iterator(idle)]


idle_lbl = Label(window, bg="white", image=frames[0])
idle_lbl = Label(window, bg="crimson")
idle_lbl.place(x=200,y=50)

def update_gif(frame_index):
    idle_lbl.configure(image=frames[frame_index])
    window.after(100, update_gif, (frame_index + 1) % len(frames))

update_gif(0)

usr_lbl = Label(window, text="You:")
usr_lbl.config(font=('Ink Free', 15))
usr_lbl.place(x=100,y=430)

usr_txt = Entry()
usr_txt.place(x=150,y=430)
usr_txt.config(font=('Ink Free', 15))
usr_txt.config(fg='#372e30')
usr_txt.config(bg='#f9f9f9')

send = Button(window,text="send",command=chat)
send.config(font=('Ink Free', 15))
send.place(x=400,y=430)

bye = Button(window, text="Bye!", command=endchat)
bye.config(font=('Ink Free', 15))
bye.place(x=460,y=430)

ran_lbl = Label(window, text="RanRan Bot:")
ran_lbl.config(font=('Ink Free', 15))
ran_lbl.place(x=20,y=270)

ran_res = Label(window, wraplength=380, justify="left")
ran_res.config(font=('Ink Free', 14))
ran_res.config(bg='white')
ran_res.place(x=140,y=270)
typing_sfx(ran_res, "Hello, I'm RanRan, wassup?")

window.mainloop()