import pandas as pd
import numpy as np
from youtube_dl import YoutubeDL


def download_audio_data(dataframe, save_path):
    
    for idx, url in enumerate(dataframe["youtube_url"][1:]):

        file_path = save_path + str(idx+1)
        def my_hook(d):
            if d['status'] == 'finished':
                print('Done downloading {}, now converting ...'.format(str(idx+1) + ".mp3"))

        if not os.path.isfile(save_path + ".mp3"):
            ydl_opts = {
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'outtmpl': save_path + ".%(ext)s"} # ".%(ext)s" is necessary, otherwise downloaded file has no audio 

            ydl = YoutubeDL(ydl_opts)
            ydl.download([url])

            

if __name__ == "__main__":
    
    # arguments parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", type=str, help="path to data file containing URLs")
    ap.add_argument("-s", "--save", type=str, help="path to save data")
    ap.add_argument("-a", "--audio", type=str, help="to save audio data", action="store_true")
    ap.add_argument("-v", "--video", type=str, help="to save video data", action="store_true")
    args = vars(ap.parse_args())
    
    # data_file = "/notebooks/storage/ctds_data/Episodes.csv"
    data_file = args["path"]
    
    # save_path = '/notebooks/storage/ctds_data/audio_files/'
    save_path = args["save"]    
    
    # clean urls if needed
    data_df = pd.read_csv(file_path)
    if args["audio"]:
        download_audio_data(data_df, save_path)

