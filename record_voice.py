import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import sys
import keyboard
import csv

def read_csv_file(filename):
    with open(filename, encoding = "utf8", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='|')
        previous_line_count = read_number_from_file("previous_line.txt")
        line_count = 0
        for row in csv_reader: 
            if previous_line_count < line_count:

                record_audio(row[0], row[2])
                write_number_to_file("previous_line.txt", line_count)
                
            line_count += 1
    return line_count

q = queue.Queue()  # Define q as a global variable

def write_number_to_file(filename, number):
    with open(filename, 'w') as file:
        file.write(str(number))

def read_number_from_file(filename):
    with open(filename, 'r') as file:
        number = int(file.read())
    return number

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    global q
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def clear_queue(q):
    while not q.empty():
        q.get()

def record_audio(filename, text):
    # Parameters for recording audio
    duration = 10   # seconds
    fs = 44100      # sampling frequency
    channels = 1    # mono

    global q        # Queue to store recorded audio

    # Start recording audio
    print("Press 's' to start recording, text to read: \n" + "\033[32m" + text + "\033[0m")
    keyboard.wait('s') 
    clear_queue(q)
    with sd.InputStream(channels=channels, samplerate=fs, callback=callback):
        print("Recording audio... Press 's' to stop.")
        keyboard.wait('s')  # Wait for 's' key press to stop recording

    # Save recorded audio to file
    audio_data = np.concatenate(list(q.queue))
    wavname = "wavs/" + filename + ".wav"
    sf.write(wavname, audio_data, fs)
    print(f"Audio recorded and saved as {wavname}.")

if __name__ == "__main__":
    csv_data = read_csv_file("metadata.csv")