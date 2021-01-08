import numpy as np
import wave, struct

# General IIR filter
def IIR_filter(x, a, b):
    Nsamples = len(x)
    y = [0] * Nsamples
    Na = len(a)
    Nb = len(b)
    
    for i in range(Nb, Nsamples):
        sumbx = 0
        
        for j in range(0, Nb):
            if i - j >= 0:
                sumbx += b[j] * x[i-j]
        
        sumay = 0

        for k in range(1, Na):
            if i - k >= 0:
                sumay += a[k] * y [i - k]
        y[i] = (sumbx - sumay) / a[0]

    return(y) 


# Read wav file
def readwav(file):
    wav = wave.open(file)
    rate = wav.getframerate()
    nchannels = wav.getnchannels()
    sampwidth = wav.getsampwidth()
    nframes = wav.getnframes()
    data = wav.readframes(nframes)
    wav.close()
    fmt=''

    for i in range (0,nframes):
        fmt = fmt + 'h' 
        # fmt should contain 'h'for each samples in wave file: 'hhhhh...'

    if nchannels == 2:
        fmt = fmt + fmt

    # for 2 channels use hh instead of h and alternately data contains L and R datasample
    t = np.arange(0, nframes / rate, 1 / rate) # start,stop, step fill array    
    D = struct.unpack(fmt, data) # from binary to integer

    return nchannels, rate, sampwidth, nframes, t, D


# Main
if __name__ == "__main__" :
    nchannels, samplerate, samplewidth, Nfrms, time, Data = readwav('file2.wav')
    Ts = 1 / samplerate
    t = np.arange(Nfrms) * Ts

    # Take subset of Data
    strt = 0
    step = len(Data)                              # Number of intervals
    stp = strt + step
    intervals = stp - strt
    subDat = Data[strt:stp]

    a = np.array([-2.014248,1.985752])            # High pass filter values
    b = np.array([-2,2])
    
    subDat = None
    
    for i in range(3):
        subDat= IIR_filter(subDat, a, b)

    # Take DFT and scale results
    freq = np.fft.fftfreq(Nfrms, Ts)

    sp = abs(2 / intervals * np.fft.fft(subDat))    # z, y=i, for log scale
    k = int(np.trunc(len(sp) / 2))                  # only first half <Fs/2 contains valid data
    sp = sp[0:k]
    freq = np.fft.fftfreq(intervals, Ts)
    freq = freq[0:k]
    t = np.arange(step) * Ts
    Data = subDat

    # Save file settings
    sampleRate = 44100.0                        # hertz
    duration = 30                               # seconds
    
    obj = wave.open('test2.wav','wb')
    obj.setnchannels(2)                         # mono 1, for stereo 2
    obj.setsampwidth(2)
    obj.setframerate(sampleRate)

    N = round(duration * sampleRate)                # no of samples
    Ts = 1 / sampleRate                             # sample time in s
    
    if (N % 2) != 0:
        N += 1

    maxint = 32767 - 1

    for i in range(N):
        value = round(Data[i])                  # data should be integer
        data = struct.pack('<h', value)         # Pack data in wav file
        obj.writeframesraw(data)

    obj.close()