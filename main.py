import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk #ttk= themed tkinter
from ttkthemes import themed_tk as tk


root= tk.ThemedTk()
root.get_themes()                 # Returns a list of all themes that can be set
root.set_theme("radiance")         # Sets an available theme

# Fonts - Arial (corresponds to Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys,
# MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), and Verdana
#
# Styles - normal, bold, roman, italic, underline, and overstrike


statusbar = ttk.Label(root, text="Welcome to Musically", relief=SUNKEN, anchor=W, font=("Times 10 italic"))
statusbar.pack(side=BOTTOM,fill=X)

leftFrame = Frame(root)
leftFrame.pack(side=LEFT,padx=30)

rightFrame = Frame(root)
rightFrame.pack()

topFrame = Frame(rightFrame)
topFrame.pack()

btnFrame= Frame(rightFrame)
btnFrame.pack(padx=30,pady=30)

btnFrame2 =Frame(rightFrame)
btnFrame2.pack()

playListbox = Listbox(leftFrame)
playListbox.pack()
    


#Creating a menu
menuBar = Menu(root)
root.config(menu=menuBar)

playlist= [] #contains full path and it requires to play music loaded in playlist

def browseFile():
    global filename_path
    filename_path= filedialog.askopenfilename()
    addPlaylist(filename_path)

def addPlaylist(filename):
    filename= os.path.basename(filename)
    index = 0
    playListbox.insert(index,filename)
    playlist.insert(index, filename_path)
    index +=1
    

#Creating a sub menu

subMenu = Menu(menuBar, tearoff=0) #tearoff removes starting dooted line in submenu of file
menuBar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open", command=browseFile)
subMenu.add_command(label="Exit", command= root.destroy)

def aboutUs():
    tkinter.messagebox.showinfo("About Us", "This is the first version of Musically, created by Pritam")

subMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us", command=aboutUs)

mixer.init()  # initializing the mixer
root.title("Musically")
root.iconbitmap("images/musically.ico")

#fileLabel=Label(root,text="This is media player")
#fileLabel.pack()

lengthLabel=Label(topFrame,text="Total Length - 00:00",fg="red")
lengthLabel.pack(pady=6)

currentLabel=Label(topFrame,text="Current Time - 00:00", relief=GROOVE,fg="red")
currentLabel.pack(pady=6)





def showDetails(playSong):
    #fileLabel['text'] = "Playing"+ " "+ os.path.basename(filename_path)

    fileData = os.path.splitext(playSong)

    if fileData[1] == ".mp3":
        audio = MP3(playSong)
        totalLength = audio.info.length
    else:
        a=mixer.Sound(playSong)
        totalLength = a.get_length()
        
    mins,secs= divmod(totalLength,60) #store quotient in mins and remainder in secs
    mins=round(mins)
    secs=round(secs)
    timeFormat ="%d:%d"%(mins,secs)
    lengthLabel['text'] = "Total length -"+ " "+ timeFormat

    t1= threading.Thread(target=startCount,args=(totalLength,))
    t1.start()
    

def startCount(length):
    global paused
    currentTime=0
    #mixer.music.get_busy returns false when music stops
    while currentTime<=length and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs= divmod(currentTime,60) 
            mins=round(mins)
            secs=round(secs)
            timeFormat ="%d:%d"%(mins,secs)
        
            currentLabel['text'] = "Current time -"+ " "+ timeFormat
            time.sleep(1) #1secs
            currentTime+=1


paused= FALSE

def playMusic():
    global paused
    if paused:
         mixer.music.unpause()
         statusbar['text'] = os.path.basename(filename_path)+" "+"resume"
         paused = FALSE
    else:
        try:
            stopMusic()
            time.sleep(1)
            selectedSong= playListbox.curselection()
            selectedSong=int(selectedSong[0])
            playIt = playlist[selectedSong]
            mixer.music.load(playIt)
            mixer.music.play()
            statusbar['text'] = "Playing"+ " "+ os.path.basename(playIt)
            showDetails(playIt)
        except:
            tkinter.messagebox.showerror("Error","File not found!!!")
    
       
        


def pauseMusic():
    global paused
    paused=TRUE
    mixer.music.pause()
    statusbar['text'] = os.path.basename(filename_path)+" "+"paused"
    
def stopMusic():
    mixer.music.stop()
    statusbar['text'] = "Stop"

def rewindMusic():
    playMusic()
    statusbar['text'] = os.path.basename(filename_path)+" "+"rewind"

def setVolume(val):
    volume= float(val)/100
    mixer.music.set_volume(volume)# set_volume takes value from 0 to 1

def delSong():
    selectedSong= playListbox.curselection()
    selectedSong=int(selectedSong[0])
    playListbox.delete(selectedSong)
    playlist.pop(selectedSong)
    

muted = FALSE

def muteMusic():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted=TRUE

  
    
playPhoto=PhotoImage(file="images/play.png")
#photolabel= Label(root, image= photo).pack()
playBtn = ttk.Button(btnFrame, image= playPhoto, command=playMusic)
playBtn.grid(row=0,column=0,padx=10)

pausePhoto= PhotoImage(file="images/pause.png")
pauseBtn = ttk.Button(btnFrame, image=pausePhoto, command=pauseMusic)
pauseBtn.grid(row=0,column=1,padx=10)

stopPhoto=PhotoImage(file="images/stop.png")
stopBtn = ttk.Button(btnFrame, image= stopPhoto, command=stopMusic)
stopBtn.grid(row=0,column=2,padx=10)



rewindPhoto=PhotoImage(file="images/rewind.png")
rewindBtn= ttk.Button(btnFrame2, image=rewindPhoto, command=rewindMusic)
rewindBtn.grid(row=0,column=0,padx=10)

mutePhoto=PhotoImage(file="images/mute.png")
volumePhoto=PhotoImage(file="images/volume.png")
volumeBtn= ttk.Button(btnFrame2, image=volumePhoto, command=muteMusic)
volumeBtn.grid(row=0,column=1,padx=10)

addBtn = ttk.Button(leftFrame, text="+ Add", command=browseFile)
addBtn.pack(side=LEFT)

delBtn = ttk.Button(leftFrame, text="- Delete",command=delSong)
delBtn.pack(side=LEFT)

scale = ttk.Scale(btnFrame2,from_=0,to=100, orient=HORIZONTAL, command= setVolume)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,padx=10)

def onClosing():
    stopMusic()
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW",onClosing) #over-riding close button
#root.geometry("300x300")
root.mainloop()
