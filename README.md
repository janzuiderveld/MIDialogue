# MIDialogue
Participate in a musical dialogue with an AI using your own MIDI instruments and/or serial connected sensors

## Setup
* Install Conda for Python 3
  * See [instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
* Install the latest distribution of Pure Data for your OS
  * http://puredata.info/downloads

In the root directory of your clone of this repo:

* Create a Conda env from `environment.yaml`.
  *  `conda env create --name ENVNAME --file environment.yaml`
* Download the weights of the sequence prediction model and store them in `data/numpy/trained_models/MusicTransformerKeyC.pth`.
  * `wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Si9mGzZdUUoXQcFYM7y2qCzkfyRvvWnr' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Si9mGzZdUUoXQcFYM7y2qCzkfyRvvWnr" -O data/numpy/trained_models/MusicTransformerKeyC.pth && rm -rf /tmp/cookies.txt`
* Start the generation server with the following args:
  * python3 generation_server.py --root $PWD 
* Open the Pure data patch PD/_MAIN.pd 

In the patch, 
