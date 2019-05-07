import numpy as np
import json
#from deepspeech import Model
#import boto3
import speech_recognition as sr
import scipy.io.wavfile as wav

def lambda_handler(event, context):

    try:
        data = event["wav_data"]
        sample_rate = int(event["sample_rate"])
        audio = np.asarray(json.loads(data),dtype="int16")
        username = event["username"] if "username" in event else None
    except Exception as e:
        return {"statusCode":500, "body": str(e)}

    #first use speech recognition package
    try:
        AUDIO_FILE_PATH = "/tmp/output.wav"
        wav.write(AUDIO_FILE_PATH,sample_rate,audio)

        # use the audio file as the audio source
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE_PATH) as source:
            audio = r.record(source)  # read the entire audio file

        # recognize speech using Google Speech Recognition
        transcription = r.recognize_google(audio)

        return {"statusCode":200, "body":json.dumps({"transcription":transcription,"username":username})}
    except Exception as e:
        print("Failed to translate using speech recognition package")
        return {"statusCode":500, "body": str(e)}

    #otherwise try old approach
    # try:
    #     #BEAM_WIDTH = 500

    #     #same parameters as trained model
    #     N_FEATURES = 26 # Number of MFCC features to use
    #     N_CONTEXT = 9 # Size of the context window used for producing timesteps in the input vector
    #     BUCKET_NAME = "838speechtotext"
        
    #     s3 = boto3.resource("s3")
    #     s3.Bucket(BUCKET_NAME).download_file("alphabet.txt","/tmp/alphabet.txt")
    #     s3.Bucket(BUCKET_NAME).download_file("output_graph.pbmm","/tmp/output_graph.pbmm")

    #     ds = Model("/tmp/output_graph.pbmm",N_FEATURES,N_CONTEXT,"/tmp/alphabet.txt",500)
    #     transcription = ds.stt(audio,sample_rate)

    #     return {"statusCode":200, "body":json.dumps({"transcription":transcription,"username":username})}
    
    # except Exception as e:
    #     return {"statusCode":500, "body": str(e)}