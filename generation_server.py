
import os
from melody_generation.numpy_encode import *
from melody_generation.utils.file_processing import process_all, process_file
from melody_generation.config import *
from melody_generation.music_transformer import *
import fastai.text.models.transformer
import traceback
from midiutil import MIDIFile
import mido
from mido import MidiFile
from audiolazy import lazy_midi
import select
import socket
import sys
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num_buffers', type=int, default=6)
parser.add_argument('--root', type=str, default="/Users/janzuiderveld/Documents/GitHub/SSI")
parser.add_argument('--model_name', type=str, default="MusicTransformerKeyC.pth")
args = parser.parse_args()


data_path = Path(f'{args.root}/data/numpy')
data = MusicDataBunch.empty(data_path)
vocab = data.vocab

model_path = str(data_path) + '/trained_models/MusicTransformerKeyC.pth'
model = music_model_learner(data, pretrained_path=model_path)

os.makedirs(f"{args.root}/PD/init_midis", exist_ok=True)
os.makedirs(f"{args.root}/PD/generated_sequences", exist_ok=True)

def empty_socket(sock):
    """remove the data present on the socket"""
    input = [sock]
    while 1:
        inputready, o, e = select.select(input,[],[], 0.0)
        if len(inputready)==0: break
        for s in inputready: s.recv(1)

def filter_notes_from_midi(fn=""):
    notes = []
    mid = MidiFile(f"{args.root}/PD/generated_sequences/{fn}.mid")
    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            if not msg.is_meta:
                print(str(msg).split()[2].split("=")[-1])
                notes.append(str(msg).split()[2].split("=")[-1])

    notes = list(set(notes)) 
    notes.remove("0")
    startindex = random.randint(0, max(len(notes)-4, 1))
    notes = notes[startindex:startindex+4]
    notes = sorted(list(set(notes)))
    return notes

def play_midi(fn:""):
    # get your midi device with mido.get_output_names()
    outport = mido.open_output("monologue SOUND")
    for msg in MidiFile(f"{args.root}/PD/generated_sequences/{fn}.mid").play():
        if not msg.is_meta:
            if str(msg).split()[2].split("=")[0] =="note":
                outport.send(msg)

def filter_notes_from_musicitem(musicitem):
    notes = []
    chords = []
    for i in musicitem.to_stream():
        if "stream" in str(i):
            for j in i:
                # print(j)
                if "Note" in str(j):
                    # print(str(j).replace("-", "b")[:-1].split()[1:])
                    notes.extend(str(j).replace("-", "b")[:-1].split()[1:])
                if "Chord" in str(j):
                    # print(str(j)[:-1].split()[1:])
                    chords.extend(str(j)[:-1].split()[1:])

    notes = sorted(list(set(notes)))
    notes = [str(lazy_midi.str2midi(note+"3")) for note in notes]
    return notes


def generate_midi(input_f="", output_f="", ntokens=60, note_t=2.0, rhythm_t=0.1, top_k=50, top_p=1):
    prime = MusicItem.from_file(f"{args.root}/PD/{input_f}", data.vocab)
    generated, full = model.predict(prime, n_words=ntokens, temperatures=(note_t,rhythm_t), min_bars=12, top_k=top_k, top_p=top_p)
    generated.stream.write('midi', fp=f"{args.root}/PD/generated_sequences/{output_f}")
    # return generated

def recipe_update_lasers(note_t, rhythm_t, top_k, top_p, lasers=args.num_buffers, input_filename="generated_sequences/generation.mid", ntokens=50):
    note_lines = []
    for i in range(lasers):
        generate_midi(input_f=input_filename, output_f=f"laser_update_{i}.mid", ntokens=ntokens, note_t=note_t, rhythm_t=rhythm_t, top_k=top_k, top_p=top_p)
        notes = filter_notes_from_midi(f"laser_update_{i}")
        notes = " ".join(notes)
        print(f"laser {i}:", notes)
        note_lines.append(f"0 {notes}")
        # play_midi(f"laser_update_{i}")

    with open(f"{args.root}/PD/generated_sequences/sorted_notes.txt", "w") as f:
        f.write(",".join(note_lines))

def recipe_generate_answer(note_t, rhythm_t, top_k, top_p, ntokens=100, filename="generation.mid"):
    generate_midi(input_f="played_sequences/seq.mid", output_f=filename, ntokens=ntokens, note_t=note_t, rhythm_t=rhythm_t, top_k=top_k, top_p=top_p)
    # play_midi(filename)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 13001)
print(f'starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)
sock.listen(1)

empty_socket(sock)
data_snd = b"ready;";

melody_t = 1.5
rhythm_t = 1
topk = 50

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data_recv = connection.recv(16)
            data_recv = data_recv.decode("utf-8")
            data_recv = data_recv.replace('\n', '').replace('\t','').replace('\r','').replace(';','')
            print(f'received {data_recv}')
            if str(data_recv) == "1":
                
                recipe_generate_answer(melody_t, rhythm_t, topk, 0.3, ntokens=90)
                recipe_update_lasers(1.5, 2, 50, 0.3, ntokens=40)

                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                clientSocket.connect(("localhost",13002));
                clientSocket.send(data_snd)

                play_midi("generation")
                print(f"melody_temp: {melody_t}, rhythm_t: {rhythm_t}, topk: {topk}")

                melody_t -= 0.1
                rhythm_t += 0.1
                # topk -= 5

            if str(data_recv) == "2" or topk < 10:
                # reset_generation_vars
                melody_t, rhythm_t, topk = 1.5, 1, 50
            
            if melody_t < 0.25:
                melody_t = 1.5
                rhythm_t = 1
                topk = 50


            empty_socket(sock)
            if not data_recv:
                break
    except Exception as e:
        print(traceback.format_exc())
        connection.close()
    finally:
        connection.close()
    
