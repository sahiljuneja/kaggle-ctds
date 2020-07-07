import pandas as pd
import numpy as np
from youtube_dl import YoutubeDL

def clean_data(file_path):

    episodes = pd.read_csv(file_path)

    episodes["youtube_url"][80] = "https://www.youtube.com/watch?v=2dpaSTWdhSk"
    episodes["youtube_url"][81] = "https://www.youtube.com/watch?v=iNZd_5T8tCI"
    episodes["youtube_url"][82] = "https://www.youtube.com/watch?v=VeM1T7UaYTk"
    episodes["youtube_url"][83] = "https://www.youtube.com/watch?v=aC9t9D7HpYE"
    episodes["youtube_url"][84] = "https://www.youtube.com/watch?v=tq_XcFubgKo"
    
    return episodes


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
    data_df = clean_data(data_file)
    if args["audio"]:
        download_audio_data(data_file, save_path)

