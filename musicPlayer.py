import tkinter as tk
from tkinter import filedialog
import os
import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()

# Create the main window
window = tk.Tk()
window.title("Reveal Music Player")
window.geometry("600x600")
window.configure(bg="#6F97BA")
window.iconbitmap("playerLogo.ico")

# Function to open the music folder
def openMusicFolder():
    directory = tk.filedialog.askdirectory()
    if directory:
        os.chdir(directory)
        songList.delete(0, tk.END)
        for filename in os.listdir(directory):
            if filename.endswith((".wav", ".mp3")):
                songList.insert(tk.END, filename)

paused = False

# Function to toggle pause/unpause
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

# Function to play the selected song
def play_music():
    selected_song = songList.get(tk.ACTIVE)
    if selected_song:
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()

def rewind_music():
    current_time = pygame.mixer.music.get_pos() // 1000  # Get current time in seconds
    new_time = max(0, current_time - 5)  # Rewind by 5 seconds, ensuring it doesn't go negative
    pygame.mixer.music.rewind()
    pygame.mixer.music.play(start=new_time)

def forward_music():
    current_time = pygame.mixer.music.get_pos() // 1000  # Get current time in seconds
    new_time = current_time + 20  # Forward by 5 seconds
    pygame.mixer.music.set_pos(new_time)

def stop_music():
    pygame.mixer.music.stop()

def set_volume(value):
    pygame.mixer.music.set_volume(float(value) / 100)
# Buttons and Listbox

#Button Frame
buttonFrame = tk.Frame(window, bg="#6F97BA")
buttonFrame.pack(side = tk.TOP)

#My main buttons
findButton = tk.Button(buttonFrame, text="Find Music", command=openMusicFolder)
findButton.pack(side = tk.TOP, pady=20)

playImage = tk.PhotoImage(file="Play.png")
play = tk.Button(buttonFrame, text="Play", command=play_music, image=playImage)
play.pack(side = tk.LEFT, padx=10)

stopImage = tk.PhotoImage(file="Stop.png")
stop = tk.Button(buttonFrame, text = "Stop", command = stop_music, image=stopImage)
stop.pack(side = tk.LEFT, padx=10)

pauseImage = tk.PhotoImage(file="Pause.png")
pause = tk.Button(buttonFrame, text="Pause", command = pause_music, image=pauseImage)
pause.pack(side = tk.LEFT, padx=10)

songFrame = tk.Frame(window, bg="Red")
songFrame.pack()
songList = tk.Listbox(songFrame, background="blue", height=15, width=50, fg="white", font=("Arial", 10))
songList.pack(padx=50, pady=50)

seekFrame = tk.Frame(window)
seekFrame.pack(side = tk.BOTTOM, pady=40)

rewindImage = tk.PhotoImage(file="REWIND.png")
rewind = tk.Button(seekFrame, text="Rewind 5s", command=rewind_music, image=rewindImage)
rewind.pack(side=tk.LEFT)

forwardImage = tk.PhotoImage(file="Forward.png")
forward = tk.Button(seekFrame, text="Forward 5s", command=forward_music, image=forwardImage)
forward.pack(side=tk.LEFT)

volume_slider = tk.Scale(songFrame, from_=0, to=100, orient="vertical", command=set_volume)
volume_slider.set(50)  # Set the initial volume to 50%
volume_slider.pack(side=tk.RIGHT)

# Start the GUI event loop
window.mainloop()
