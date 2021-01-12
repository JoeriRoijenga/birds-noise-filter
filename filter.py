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
    
    duration = nframes/rate
    
    for i in range (0,nframes):
        fmt = fmt + 'h' 
        # fmt should contain 'h'for each samples in wave file: 'hhhhh...'

    if nchannels == 2:
        fmt = fmt + fmt

    # for 2 channels use hh instead of h and alternately data contains L and R datasample
    t = np.arange(0, nframes / rate, 1 / rate) # start,stop, step fill array    
    D = struct.unpack(fmt, data) # from binary to integer

    return nchannels, rate, sampwidth, nframes, t, D, duration

def writewav(nchannels, samplerate, samplewidth, duration, subDat):
    file = wave.open('filter1.wav','wb')
    file.setnchannels(nchannels)                      # mono 1, for stereo 2
    file.setsampwidth(samplewidth)
    file.setframerate(samplerate)

    N = round(duration * samplerate)                 # no of samples
    
    if (N % 2) != 0:
        N += 1
        
    # Pack data in wav file
    for i in range(N):
        value = round(subDat[i])                     # data should be integer
        data = struct.pack('<h', value)
        file.writeframesraw(data)

    file.close()

# Main
if __name__ == "__main__" :
    nchannels, samplerate, samplewidth, Nfrms, time, Data, duration = readwav('file1.wav')

    # Take subset of Data
    strt = 0
    step = len(Data)                              # Number of intervals
    stp = strt + step
    subDat = Data[strt:stp]

    a = np.array([-2.142717,1.857283])
    b = np.array([-2,2])
    #a = np.array([4.424034,-7.959264,3.616703])
    #b = np.array([4,-8,4])
    
    # a = np.array([1.000000000000000,-3.619724057745430,5.384488461116604,-4.088649657052628,1.579037255944415,-0.247487118545669]) # 3000
    # b = np.array([0.497480829700148,-2.487404148500741,4.974808297001482,-4.974808297001482,2.487404148500741,-0.497480829700148])

    for i in range(3):
        subDat= IIR_filter(subDat, a, b)

    writewav(nchannels, samplerate, samplewidth, duration, subDat)