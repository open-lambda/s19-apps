import requests
import scipy.io.wavfile as wav
import json

#r = requests.post("http://localhost:8080/runLambda/hello",data='{"name":"Bucky"}')
#print(r.status_code)
#print(r.text)
#print("")

fs, audio = wav.read("example.wav")
s = json.dumps(audio.tolist())
data = {"wav_data":s,"sample_rate":fs}
#r = requests.post("http://localhost:8080/runLambda/sttf",data=json.dumps(data))
r = requests.post("http://c220g5-111206.wisc.cloudlab.us:8080/runLambda/sttf",data=json.dumps(data))
print(r.status_code)
print(r.text)
