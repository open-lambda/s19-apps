git clone https://github.com/open-lambda/open-lambda.git
cd open-lambda

sudo ./quickstart/deps.sh
sudo make

clustername=my-cluster
sudo ./bin/admin new -cluster $clustername

lambdadir=sttf
sudo cp -r ../$lambdadir $clustername/registry/

if [ ! -d "../models" ]; then
	cd ..
	wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz
	tar xvfz deepspeech-0.4.1-models.tar.gz
	cd open-lambda
fi

#install function data files and packages
mkdir ../ds_data
touch ../ds_data/__init__.py
sudo cp ../models/output_graph.pb ../ds_data/gph.pb
sudo cp ../models/alphabet.txt ../ds_data/alph.txt
sudo mv ../ds_data $clustername/packages/

sudo pip install numpy --target=$clustername/packages
sudo pip install deepspeech --target=$clustername/packages

sudo cp -r ./quickstart/handlers/hello ./my-cluster/registry/hello

#sudo ./bin/admin workers -cluster=$clustername
#sudo ./bin/admin status -cluster=$clustername
#curl -X POST localhost:8080/runLambda/hello -d '{"name": "Bucky"}'
