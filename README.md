# MIDialogue
Participate in a musical dialogue with an AI using your own MIDI synthesizers and serial connected sensors

## Setup
* Install Conda for Python 3
  * See [instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
* Install the latest distribution of Pure Data for your OS
  * http://puredata.info/downloads
* Install the comport, else and cyclone externals in pure data

In the root directory of your clone of this repo:

* Create a Conda env from `environment.yaml` and activate.
  *  `conda env create --name ENVNAME --file environment.yaml`
  *  `conda activate ENVNAME`
* Download the weights of the sequence prediction model and store them in `data/numpy/trained_models/transformerC_checkpoint.pth` with the following command:
  * `wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Si9mGzZdUUoXQcFYM7y2qCzkfyRvvWnr' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Si9mGzZdUUoXQcFYM7y2qCzkfyRvvWnr" -O data/numpy/trained_models/transformerC_checkpoint.pth && rm -rf /tmp/cookies.txt`
* Start the generation server with the following args:
  * `python3 generation_server.py --root $PWD`
* Open the Pure data patch PD/_MAIN.pd, and follow the instructions there
