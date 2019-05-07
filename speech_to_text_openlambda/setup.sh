sudo apt-get update
sudo apt-get install python-pip
pip install scipy
pip install numpy
pip install librosa #just for the stt_example, not open lambda

#setup virtual env
#sudo pip3 install virtualenv
#virtualenv -p python3 deepspeech-env
#source deepspeech-env/bin/activate

pip install deepspeech

#https://pysoundfile.readthedocs.io/en/0.9.0/
#sudo apt-get install libsndfile1
#pip3 install pysoundfile

#download pre-trained model - 1.83 GB
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz
tar xvfz deepspeech-0.4.1-models.tar.gz

#download example audio
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/audio-0.4.1.tar.gz
tar xvfz audio-0.4.1.tar.gz
cp audio/2830-3980-0043.wav example.wav

echo "Run an example with: python stt_example.py example.wav"
