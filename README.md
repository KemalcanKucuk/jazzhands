# Jazz Hands

## Project Descriptions
Jazz Hands is an end-to-end automatic music transcription interface. Its main purpose is to enable musicians to transcribe their playing into sheet music without learning any additional skills for transcription software.

The intended use is for a musician to open the interface, pick up their instrument and say "record" to start transcribing. Later, the musician can listen to what they transcribed and see the sheet music on the screen. 

What I mean by "end-to-end" is that there aren't many tools that combine each tool that JH is utilizing for the end-user, such as combining transcription/pitch estimation models with MIDI conversions and musical engraving.

The project has a proof-of-concept nature as each of the challenges that I'll describe in the following section have intricate and exhausting solutions that I couldn't fully reach. 


## What were the challenges?
Technical challenges, user-study challenges, etc.

### Technical Challenges

The main 4 technical challenges involved are: 

<ol>
  <li>Audio to Note Transcription</li>
  <li>MIDI Conversion</li>
  <li>Musical Engraving</li>
  <li>Voice Recognition</li>
</ol> 

#### Audio-to-Note Transcription

This part is where most of the development time was spent. There are different ways for musical transcription but most of the state-of-the-art models are focused on "pitch detection estimation". These models perform well but in my case, they require long inference times and they are not suitable for using them in a pipeline since most of the models output a list of possible frequencies with their corresponding time occurrence in the given signal. This creates the need for many conversion layers to transform the transcription into a MIDI file, or conversion to a mainstream music library (music21 in my case) by converting each note to a note object in the relevant library. And this process also includes a conversion for rhythmic value, which is an area of study by itself. Also, some of the models were not compatible with (or performed sub-par) certain instruments and I wanted to keep the variety high.

After testing many different models (and in hindsight delving too much and wasting time), I decided to settle with Spotify's "Basic Pitch" API since it was much faster than what I tested and their pipeline had a built-in MIDI conversion and also an audio file for the transcribed MIDI file, which is great since we would need it for playback anyway. Basic Pitch is also almost instrument-agnostic, meaning I could transcribe a variety of instruments. Another advantage of it is that it can transcribe polyphonic music (more than one sound being played simultaneously) which is great for rhythm section players.

A drawback of Basic Pitch is that it was meant to use in music production as MIDI outputs. Normally, any glitch or artifact caused by the inference can be easily deleted by the musician by inspecting the MIDI notes on a piano roll. But this is not possible in our case since we can't differentiate between the relevant notes and artifacts. That's why when the MIDI file is converted into a piece of sheet music it will have some artifacts.

#### MIDI Conversion

By using Basic Pitch, this problem was solved by itself but a MIDI file was necessary regardless of the implementation I went with because the transcribed notes will be converted to audio again for playback and also engraving gets quite easier when using MIDIs.

#### Musical Engraving

Musical Engraving is what I call the conversion from the transcribed values into sheet music. This is one of the parts I put more than the necessary hours upon because initially, I tried to develop a musical representation backend from scratch. But of course, this didn't work well and I couldn't connect with any of the existing APIs for engraving. Initially, I decided that a more interactive interface would be best for making changes and tried to connect LilyPond (a common open-source engraving software) into the pipeline but again that complicated things way more than it was necessary and I changed the interface to be a simple PDF viewer. 

I used music21 for dealing with MusicXML files and used MuseScore to parse and process the MIDI file into a piece of sheet music, which was converted into a PDF file and shown in the interface after the transcription was finished.

Voice Recognition is quite involved with the user-study challenge so I'll discuss it in the following section.


### User-Study Challenges

I conducted a user study with 10 participants (that were down to 6 by the end of the semester) with intermediate to advanced players who are mostly beginners at reading and writing sheet music. 

This part goes hand-in-hand with the user-study challenge because I changed my initial plan with a lot of user feedback. My initial plan was to enable users to change any note in the sheet music by using voice commands like "change the 4th note in bar 2 to a C#" but my first test for this felt very cumbersome to the players. For the voice recognition I used Google Web API and although it was performing well for broad commands (record, play, stop) it wasn't enough for specific modification.

Following this I changed the command to go to a specific bar, then record on top of the existing recording; but this didn't yield the result I wanted and most of the users didn't even bother fixing any mistakes. None of the users chose to transcribe longer audios (like a full song ~3 mins. long) but instead, they chose to transcribe licks and parts they've been wanting to save to somewhere. Since the recording was 15-20 seconds maximum, they didn't want to interact with the voice command to go to a specific bar and they chose to record from scratch.

I still believe recording on top of a failed section is the better way to interact with this but most likely my implementation fell short (music21 also behaves strangely when modifying an existing file, there would be many engraving errors), and in the final interface I've only kept re-recording from scratch.


## What have you learned?
Academic, technical, personal, etc.

I was really excited to work on this project and it was a great experience for me. Thinking about how I could make an interaction more natural was quite eye-opening and I started to inspect my daily relationship with technology from this perspective. 

I've found out that I need to work on GUIs a bit more because it took me a long time to connect the backend of the project with the front end because of UI loops. 

And from a meta-academic perspective, I wish I had kept the scope smaller when I first started. I could make something a lot more polished but I tried to do so much and I should've let go of some things that I've been working on forever by that point. Also, my health wasn't the best from a few weeks into the semester and I should've scaled down at that point to make the best of my functional time. Overall, it was a very informative, fun, and sometimes a bit too stressful experience for me. 

## Suggestions to contributors

I didn't include any of my experimentations with other models and kept the final code quite simple for easier modification but I could provide them guidance on what would work best for a project like this. They can start with a better implementation of the rerecording section of the interface because the ability to recover from mistakes is quite impaired now, especially when working with a longer piece.
