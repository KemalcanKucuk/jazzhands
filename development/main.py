import speech_recognition as sr
import pyaudio

import os
import time
import sys

import backend_main as bm
from view_screen import *

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk

import random

test_recording = "/Users/kemalcankucuk/jazzhands/jazzhands/development/midi/drum_loop_for_trans"

midi_path = "/Users/kemalcankucuk/jazzhands/jazzhands/development/midi/"
sheet_path = "/Users/kemalcankucuk/jazzhands/jazzhands/development/sheet/"
sheet_output = sheet_path + "output.pdf"

recording = "/Users/kemalcankucuk/jazzhands/jazzhands/development/midi/pya_record"
recording_file = recording + ".wav"

playback_file = recording + '_basic_pitch.wav'
midi_file = recording + '_basic_pitch.mid'


def main():

    working_state = True
    p = pyaudio.PyAudio() # portaudio instance
    r = sr.Recognizer() # speech recognition instance
    root = ThemedTk(theme="arc") # root Tk instance
    app = ViewScreen(root)
    ids = []
    while working_state:
        
        print("User is prompted")
        command = command_recognition(rec_type=0, file=TEST_SR, r=r)

        #recording = test_recording
        
        if "record" in command.split():
            record_sound(seconds=10, file=recording_file, p=p) # 10s is what'ive gathered from user study
            transcribe(recording_file, midi_path)
        
        elif "play" in command.split():
            play_file(playback_file, p)
            write_to_pdf(midi_file, sheet_output)   
            app.open_file(sheet_output)
            
        elif "stop" in command.split():
            app.terminate_session()
            working_state = False
        
        root.mainloop()


if '__name__' == '__main__':
    main()


