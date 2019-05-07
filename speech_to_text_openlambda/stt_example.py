from deepspeech import Model
import sys
import librosa

audio,fs = librosa.load(sys.argv[1],sr=16000)
audio = (audio * 32767).astype("int16")

ds = Model("models/output_graph.pb",26,9,"models/alphabet.txt",500)
processed_data = ds.stt(audio,fs)

output_file_path = "/tmp/output_data.txt"
with open(output_file_path,"w") as f:
    f.write(processed_data)
    print(processed_data)
    print("Results written to " + output_file_path)
