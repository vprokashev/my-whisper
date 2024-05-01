import os
import pyaudio
import wave
import signal


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 44100
CHUNK = 1024

recording = False


def signal_handler(sig, frame):
    global recording
    if recording:
        print("Finishing recording...")
        recording = False


signal.signal(signal.SIGINT, signal_handler)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


print("Recording... (Press Ctrl+C to stop)")

wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)

recording = True

while recording:
    data = stream.read(CHUNK)
    wf.writeframes(data)

print("Finished recording.")
stream.stop_stream()
stream.close()

wf.close()

p.terminate()
