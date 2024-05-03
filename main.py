import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import pyaudio
import wave
import signal
from faster_whisper import WhisperModel


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 44100
CHUNK = 102400  # 1024

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

model_size = "medium.en"
model = WhisperModel(
    model_size,
    device="cuda",
    compute_type="float16",
    download_root=os.path.join(os.path.dirname(__file__), "./models/download")
)



print("Recording... (Press Ctrl+C to stop)")

recording = True

while recording:
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    data = stream.read(CHUNK)
    wf.writeframes(data)
    segments, info = model.transcribe("./output.wav", beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    print(transcription)
    wf.close()

print("Finished recording.")
stream.stop_stream()
stream.close()

p.terminate()
