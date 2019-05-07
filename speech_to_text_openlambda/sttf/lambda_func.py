import numpy as np
import json
from deepspeech import Model
import ds_data
import pkg_resources
import scipy.io.wavfile as wav
import sys
import os

def handler(event):
    try:
        #get data
        wav_data = event["wav_data"]
        wav_data = np.asarray(json.loads(wav_data),dtype="float32")
        sample_rate = int(event["sample_rate"])
        
        #downsample
        import scipy.signal as sps
        new_rate = 16000

        number_of_samples = int(round(len(wav_data) * float(new_rate) / sample_rate))
        audio = sps.resample(wav_data, number_of_samples)

        audio = (audio * 32767).astype("int16")

        #predict
        alphabet = pkg_resources.resource_filename("ds_data","alph.txt")
        model = pkg_resources.resource_filename("ds_data","gph.pb")

        ds = Model(model,26,9,alphabet,500)
    
        text = ds.stt(audio,new_rate)

        return text
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return {'error': str(e) + ":" + str(exc_type) + " " + str(fname) + " " + str(exc_tb.tb_lineno)}
