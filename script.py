#!/usr/bin/env python
#
# A script that formats samples to wavetables for an Arduino drum machine I made.
#
# Shortens .wav files to mono, 2048 samples long and 
# uses ffmpeg (https://ffmpeg.org/) to format them to signed 8-bit .raw.
# char2mozzi.py from the mozzi library (https://github.com/sensorium/Mozzi/tree/master/extras/python) 
# is used (with small changes) to generate the wavetables from .raw files with samplerate of 16384.

import glob
import os
import wave
from tkinter import filedialog
from tkinter import *
from pydub import AudioSegment
import char2mozzi as c2m

sample_count = 2048

ffmpeg_exe = "C:/ffmpeg/bin/ffmpeg.exe" # Where ffmpeAg is installed

def to_wavetable(file):
    file = file.split(".")[0]
    ffmpeg = ffmpeg_exe + " -y -i " + file + ".wav -f s8 -acodec pcm_s8 " + file + ".raw"
    os.system(ffmpeg)
    c2m.char2mozzi(f"{file}.raw", f"{file}.h", file, 16384)

def format(file):
    with wave.open(file, "r") as read:
        frames = read.getnframes()
        sampwidth = read.getsampwidth()
        framerate = read.getframerate()
        channels = read.getnchannels()

        if frames > sample_count:   # if wav files sample count is > 2048: read and write the first 2048 samples, else write all of them
            data = read.readframes(sample_count)
        else:
            data = read.readframes(frames)
    
    with wave.open(file, "w") as write:
        write.setnchannels(channels)
        write.setsampwidth(sampwidth)
        write.setframerate(framerate)
        write.writeframes(data)

    to_wavetable(file)

if __name__ == "__main__": 
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="Select Folder With .wav Samples")
    for file in glob.glob(path + "/" + "*.wav"): # Searches folder for all .wav files
        sound = AudioSegment.from_wav(file)
        sound = sound.set_channels(1) # Downsamples file to mono
        sound.export(file, format="wav")
        format(file)  
