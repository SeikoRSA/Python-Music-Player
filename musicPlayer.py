import tkinter as tk
from tkinter import filedialog
import os
import pygame
import time

# Initialize pygame mixer.
pygame.mixer.init()

# Create the main window
window = tk.Tk()
window.title("Reveal Music Player")
window.geometry("600x600")
window.configure(bg="#4f6c85")
window.iconbitmap("images\playerLogo.ico")

# Function to open the music folder and filter out non mp3 and wav files.
def openMusicFolder():
    directory = tk.filedialog.askdirectory()
    if directory:
        os.chdir(directory)
        songList.delete(0, tk.END)
        for filename in os.listdir(directory):
            if filename.endswith((".mp3", ".wav")):
                songList.insert(tk.END, filename)

paused = False

# Function to toggle pause/unpause.
def pause_music():
    global paused

    if not paused:
        pygame.mixer.music.pause()
        pause.config(text='Unpause')
        paused = True
    else:
        pygame.mixer.music.unpause()
        pause.config(text='Pause')
        paused = False

# Function to play the selected song.
def play_music():

    selected_song = songList.get(tk.ACTIVE)
    if selected_song:
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()

# Function to rewind the selected song.
def rewind_music():
    pygame.mixer.music.pause()  # Pause the music
    current_time = pygame.mixer.music.get_pos() // 1000  # Get current time in seconds
    new_time = max(0, current_time - 3)  # Rewind by 5 seconds, ensuring it doesn't go negative
    pygame.mixer.music.rewind()  # Rewind to the beginning of the track
    pygame.mixer.music.play(start=new_time)  # Resume playback from the new position

# Function to forward the selected song.
def forward_music():
    current_time = pygame.mixer.music.get_pos() // 1000  # Get current time in seconds
    new_time = current_time + 20  # Forward by 5 seconds
    pygame.mixer.music.set_pos(new_time)

# Function to stop the selected song.
def stop_music():
    pygame.mixer.music.stop()

# Function to change the selected song's volume.
def set_volume(value):
    pygame.mixer.music.set_volume(float(value) / 100)

# Function to change slider color
def on_enter(event):
    volume_slider.config(bg="#3b5164")
    volume_slider.config(foreground="white")

def on_leave(event):
    volume_slider.config(bg="#3b5164")
     
# Function to seek to a certain position in the song.
def seek_music(value):

    #Capture the song itself
    sound = pygame.mixer.Sound(songList.get(tk.ACTIVE))
    #How long that song is
    duration = sound.get_length()

    #The scale bar has values from 0 to 100, then convert's them to integer.
    scalePosition = int(value)

    newPosition = (scalePosition/100)*duration
    pygame.mixer.music.set_pos(newPosition)

    print(f"The duration of the sound is: {duration:.2f} seconds")
    print(f"Current scale bar position: {scalePosition}")

# Buttons and Listbox

#Button Frame
buttonFrame = tk.Frame(window, bg="#4f6c85")
buttonFrame.pack(side = tk.TOP)

#Find button
findButton = tk.Button(buttonFrame,font=("Helvetica",15), text="Find Music", command=openMusicFolder, bg="#2e4151", fg="#acb6bf")
findButton.pack(side = tk.TOP, pady=20)

#Creating Images for the buttons
playImage = tk.PhotoImage(file="images\Play.png")
play = tk.Button(buttonFrame, text="Play", command=play_music, image=playImage)
play.pack(side = tk.LEFT, padx=10)

stopImage = tk.PhotoImage(file="images\Stop.png")
stop = tk.Button(buttonFrame, text = "Stop", command = stop_music, image=stopImage)
stop.pack(side = tk.LEFT, padx=10)

pauseImage = tk.PhotoImage(file="images\Pause.png")
pause = tk.Button(buttonFrame, text="Pause", command = pause_music, image=pauseImage)
pause.pack(side = tk.LEFT, padx=10, pady=20)

#Creating section where the songs go
songFrame = tk.Frame(window, bg="#3b5164")
songFrame.pack()
songList = tk.Listbox(songFrame, background="blue", height=15, width=50,bg="#2c3c4a", fg="white", font=("Arial", 10))
songList.pack(padx=50,pady=20, side=tk.TOP)

#This is a seek component
musicScroll = tk.Scale(songFrame, from_=0,to=100, orient=tk.HORIZONTAL, command=seek_music, length=400, bg="#3b5164", troughcolor="#2e4151", highlightthickness=0)
musicScroll.pack(pady=5)


seekFrame = tk.Frame(window, background="#3b5164")
seekFrame.pack(pady=20)

#Creating Images for the buttons
rewindImage = tk.PhotoImage(file="images\REWIND.png")
rewind = tk.Button(seekFrame, text="Rewind 5s", command=rewind_music, image=rewindImage)
rewind.pack(side=tk.LEFT, padx=10)

forwardImage = tk.PhotoImage(file="images\Forward.png")
forward = tk.Button(seekFrame, text="Forward 5s", command=forward_music, image=forwardImage)
forward.pack(side=tk.LEFT)

#Creating Volume slider
volume_slider = tk.Scale(seekFrame, from_=100, to=0, orient="vertical", command=set_volume, bg="#3b5164", highlightthickness=0, troughcolor="#768fa5")
volume_slider.set(50)  # Set the initial volume to 50%

#Allowing more control on color of the slider using on_enter and on_leave
volume_slider.bind("<Enter>", on_enter)
volume_slider.bind("<Leave>", on_leave)

volume_slider.pack(side=tk.RIGHT)

#Add copyright text to the bottom section of the window.
copyrightTag = tk.Label(window, text="Copyright © 2023 Katleho Ribisi", background="#4f6c85", font=("Helvetica",13), foreground="white")
copyrightTag.pack(anchor="s", pady=80)


# Start the GUI event loop
window.mainloop()
