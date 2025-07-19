import sounddevice as sd
import vosk
import queue
import json
import tkinter as tk
import threading

# === Queue for audio input ===
q = queue.Queue()

# === Callback for microphone input ===
def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    q.put(bytes(indata))

# === Speech recognition thread ===
def recognize():
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            final_text = result.get("text", "")
            update_text(final_text)
        else:
            partial = json.loads(rec.PartialResult())
            update_text(partial.get("partial", ""))

# === GUI: update text label ===
def update_text(new_text):
    text_var.set(new_text)

# === Setup GUI ===
root = tk.Tk()
root.configure(bg="black")
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e: root.destroy())  # Exit fullscreen with Esc

text_var = tk.StringVar()
label = tk.Label(root, textvariable=text_var,
                 font=("Helvetica", 48),
                 fg="white", bg="black",
                 wraplength=root.winfo_screenwidth(),
                 justify="center")

# Top-align the label with padding from the top
label.pack(side="top", fill="x", pady=40)

# === Load Vosk model ===
model = vosk.Model(r"vosk-model-small-en-us-0.15")  # Change this to the folder of the model
samplerate = 16000
device = None
rec = vosk.KaldiRecognizer(model, samplerate)

# === Start microphone stream ===
stream = sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype='int16', channels=1, callback=callback)
stream.start()

# === Start recognition in separate thread ===
threading.Thread(target=recognize, daemon=True).start()

# === Run GUI loop ===
root.mainloop()

# https://alphacephei.com/vosk/models