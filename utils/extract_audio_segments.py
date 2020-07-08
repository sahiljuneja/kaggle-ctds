import re
import os
import argparse
import librosa
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pydub import AudioSegment
import time


def extract_data(input_path, save_path, data_path):
    
    path = os.listdir(input_path)
    for file in path:
        
        episode_num = int(file.split('.mp3')[0])
        
        # account for non-interview episodes and missing E4 subtitles
        if (episode_num > 45 and episode_num < 55) or episode_num == 4:
            continue
        elif episode_num > 54:
            episode_num = episode_num - 9
        episode_transcript = pd.read_csv(data_path + "E" + str(episode_num) + ".csv")
        print("Loaded Transcript for Episode {}".format(episode_num))
        episode_audio = AudioSegment.from_mp3(input_path + file)
        print("Loaded Audio for Episode {}".format(episode_num))
        for idx, time in enumerate(episode_transcript["Time"][:-1]):
            
            fig_save_path = save_path + str(episode_num) + "_" + str(idx) + ".jpeg"
            if not os.path.isfile(fig_save_path):

                start_minutes = int(episode_transcript.loc[idx, "Time"].split(":")[0])
                start_seconds = int(episode_transcript.loc[idx, "Time"].split(":")[1])

                stop_minutes = int(episode_transcript.loc[idx+1, "Time"].split(":")[0])
                stop_seconds = int(episode_transcript.loc[idx+1, "Time"].split(":")[1])

                start_time = (start_minutes*60 + start_seconds)*1000
                stop_time = (stop_minutes*60 + stop_seconds)*1000 

                clip = episode_audio[start_time:stop_time]

                samples = clip.get_array_of_samples()
                sample = np.array(samples).astype(np.float32)

                yt, _ = librosa.effects.trim(sample)
                y = yt
                sr=clip.frame_rate

                mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=100)
                mel_spect = librosa.power_to_db(mel_spect, ref=np.max)

                fig = librosa.display.specshow(mel_spect, fmax=20000)
            
                plt.savefig(fig_save_path, bbox_inches='tight', pad_inches=0.0)
                print("File saved to: {}".format(fig_save_path))


if __name__ == "__main__":
    
    # arguments parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str, help="path to existing audio files")
    ap.add_argument("-s", "--save", type=str, help="path to save files after slicing")
    ap.add_argument("-d", "--data", type=str, help="path to data file containing transcripts")
    args = vars(ap.parse_args())
    
    # sample call
    # python extract_audio_segments.py -p /notebooks/storage/ctds_data/audio_files/ -s /notebooks/storage/ctds_data/audio_files/audio_files_segments/
    # data path = "/notebooks/storage/ctds_data/Cleaned Subtitles/
    
    ip_path = args["path"]
    save_path = args["save"]
    data_path = args["data"]
    
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    
    time_start = time.time()
    extract_data(ip_path, save_path, data_path)
    print("Audio data segmented and saved as jpeg")
    print("Total time taken: ", time.time() - time_start)
    