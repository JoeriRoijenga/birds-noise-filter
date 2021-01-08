import noisereduce as nr
# load data
rate, data = wavfile.read("mywav.wav")
# select section of data that is noise
noisy_part = data[10000:15000]
# perform noise reduction
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)
