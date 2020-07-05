import re
import os
import argparse
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def modify_data(input_path, save_path, dir_dict):
    
    path = os.listdir(input_path)
    for folders in path:
        
        folders = os.path.sep.join([input_path, folders])
        
        for file in os.listdir(folders):
            
            num = re.findall('\d+', file)
            emotion = dir_dict[num[2]]
            
            file_save_path = save_path + str(emotion)
            if not os.path.isdir(file_save_path):
                os.makedirs(file_save_path)

            load_file_path = '{0}/{1}'.format(folders, file)
            
            file_name = "/{}.jpeg".format(file[:-4])
            if not os.path.isfile(file_save_path + file_name):
            
                y, sr = librosa.load(load_file_path)
                yt, _ = librosa.effects.trim(y)
                y = yt

                mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=100)
                mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

                librosa.display.specshow(mel_spect, y_axis='mel', fmax=20000, x_axis='time');


                plt.savefig(file_save_path + file_name)

                #print("File saved to: {}".format(file_save_path + file_name))


if __name__ == "__main__":

    # sample call
    # python modify_ravdess.py -p /notebooks/storage/ravdess/ -s /notebooks/storage/ravdess_mod/
    
    # arguments parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str, help="path to raw data")
    ap.add_argument("-s", "--save", type=str, help="path to save data after processing")
    args = vars(ap.parse_args())
    
    # directory structure dict
    dir_dict = {'01' : 'neutral', '02' : 'calm', '03' : 'happy', '04' : 'sad', 
                '05' : 'angry', '06' : 'fearful', '07' : 'disgust', '08' : 'surprised'}
    
    ip_path = args["path"]
    save_path = args["save"]
    
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    
    modify_data(ip_path, save_path, dir_dict)
    print("Data converted from .wav to .jpeg")
    