from music21 import *

def write_to_pdf(stream, fp):
    '''
    Gets a music21 input stream and writes the output pdf file
    parsed by the MusicXML parser.
    '''

    out = stream.write('musicxml.pdf', fp=fp)
    print("PDF file is written!")

