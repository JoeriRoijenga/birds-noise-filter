from pydub import AudioSegment

song = AudioSegment.from_wav("filter1.wav")

# reduce volume by 20 dB
song = song + 20

# save the output
song.export("louder1.wav", "wav")