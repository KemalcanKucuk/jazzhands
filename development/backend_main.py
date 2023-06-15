from basic_pitch.inference import predict_and_save
import music21

import speech_recognition as sr

import numpy as np
import pandas as pd

import pyaudio
import wave

import librosa as lr
import soundfile as sf

import random

import os
import time
import sys
from playsound import playsound # for mp3s

# instancing and initialization

# function tests
TEST_WAV = "/Users/kemalcankucuk/Music/Logic/Bounces/drum_loop_for_trans"
TEST_MP3 = "/Users/kemalcankucuk/Music/Logic/Bounces/sax jam"
TEST_SR = "/Users/kemalcankucuk/jazzhands/jazzhands/test_audios/speech_recognition_bm.wav"

def create_temp_wav(file, temp_name):

    '''
    Create a temporary .wav file if reading any other file type is necessary.
    '''

    temp_path = temp_name + '.wav'
    y, sr = lr.load(file)
    sf.write(temp_path, y, sr)
    return temp_path

def record_sound(seconds, file, p):

    '''
    Record audio file for the specified amount of duration
    '''

    file_id = random.randint(1, 5000)
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100 
    filename = "output.wav"

    #p = pyaudio.PyAudio() 

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    #return file_id

def play_file(file, p):
    #print("Playing the file: ", file)
    file_s = os.path.splitext(file)
    if file_s[1] == ".mp3" or file_s[1] == ".wav":
        playsound(file)
    print("Ended playing the file")
    '''        
    elif file_s[1] == ".wav":
        wf = wave.open(file, 'rb')
        stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # Read data in chunks
        data = wf.readframes(chunk)

        # Play the sound by writing the audio data to the stream
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
            if data == b'':
                break
        # Close and terminate the stream
        stream.close()
        p.terminate()
        '''
    
def command_recognition(rec_type, file, r):

    '''
    Recognize command using speech_recognition library and Google Web API.
    rec_type=1: passing the recording ti PyAudio
    rec_type=0: native recording using SR
    '''

    out = ''
    if rec_type:
        # processing a file
        command_file = sr.AudioFile(file)
        with command_file as source:
            try:
                print("started loading file")
                audio = r.record(source)
                out = r.recognize_google(audio)
            except sr.exceptions.UnknownValueError:
                print("failed due to noise")
    else:
        mic = sr.Microphone()
        with mic as source:
            #r.adjust_for_ambient_noise(source)
            try:
                print("started recording")
                audio = r.listen(source)
                out = r.recognize_google(audio)
            except sr.exceptions.UnknownValueError:
                print("recording failed due to noise")
    #print(out)
    return out

def transcribe(recording, fp):
    predict_and_save(audio_path_list=[recording],
                    output_directory=fp,
                    save_midi=True, 
                    sonify_midi=True,
                    save_model_outputs=False,
                    save_notes=False)

def write_to_pdf(midi_file, fp):

    '''
    Gets a music21 input stream and writes the output pdf file
    parsed by the MusicXML (MuseScore in this implementation) parser.
    '''
    
    stream = music21.converter.parse(midi_file)
    print("Received MIDI File!")
    out = stream.write('musicxml.pdf', fp=fp)
    print("PDF file is written!")

if '__name__' == '__main__':
    
    p = pyaudio.PyAudio() # portaudio instance
    r = sr.Recognizer() # speech recognition instance

    #play_file(test_wav, p)
    #record_sound(5, p)
    #command_recognition(0, None, r)
    #command_recognition(1, test_sr, r)


