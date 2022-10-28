from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.factory import get_crossover, get_mutation, get_sampling
import io
import sys
import requests
import numpy as np
from pprint import pprint
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
requests.packages.urllib3.disable_warnings()

YOUTUBE_API_KEY = "AIzaSyB4jvB4FZR0VkZfD08lzDhCE33o_9WMDXc"

global datasetv, datasetl
datasetv = {}
datasetl = {}
satisfaction = {}


youtube_channel_id = "UCXOBLGJdYA1mfhOrDwQESTg"


class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        """取得頻道上傳影片清單的ID"""
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='contentDetails', max_results=30):
        """取得影片清單ID中的影片"""
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults=30'
        data = self.get_html_to_json(path)
        if not data:
            return []

        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids

    def get_video1(self, video_id, part='snippet,statistics'):
        """取得影片點閱數"""
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]

        info = int(data_item['statistics']['viewCount'])
        return info

    def get_video2(self, video_id, part='snippet,statistics'):
        """取得影片按讚數"""
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]

        info = int(data_item['statistics']['likeCount'])
        return info

    def get_video3(self, video_id, part='snippet,statistics'):
        """取得影片標題"""
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        data_item = data['items'][0]

        info = data_item['snippet']['title']
        return info


youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)

video_ids = youtube_spider.get_playlist(uploads_id, max_results=5)

for video_id in video_ids:
    print("----------------------")
    video_view = youtube_spider.get_video1(video_id)
    video_like = youtube_spider.get_video2(video_id)
    video_title = youtube_spider.get_video3(video_id)
    datasetv[video_id] = youtube_spider.get_video1(video_id)
    datasetl[video_id] = youtube_spider.get_video2(video_id)
    satisfaction[video_id] = datasetl[video_id] / datasetv[video_id]
    print(video_title)
    print("點閱數: %s" % video_view)
    print("按讚數: %s" % video_like)
    print(satisfaction[video_id])


global PopulationSize, NGEN, CXPB, MUTPB

PopulationSize, NGEN, CXPB, MUTPB, = 10, 50, 0.9, 0.01

sampling = get_sampling("bin_random")

crossover = get_crossover("real_one_point",  prob=CXPB)

mutation = get_mutation("bin_bitflip", prob=MUTPB)

algorithm = GA(
    pop_size=PopulationSize,
    sampling=sampling,
    crossover=crossover,
    mutation=mutation,
    eliminate_duplicates=True
)


class trade_problem(Problem):
    def __init__(self):
        super().__init__(n_var=20)

    def _evaluate(self, x, out, *args, **kwargs):
        population = x.astype(int)
        fvalue_list = []
        for individual in population:
            views = 0
            likes = 0
            for i, g in enumerate(individual):
                if (g == 1):
                    views += datasetv[video_ids[i]]
                    likes += datasetl[video_ids[i]]
            if (likes == 0):
                fvalue = 0
            else:
                fvalue = -(likes/views)
            fvalue_list.append(fvalue)
        out["F"] = np.column_stack([fvalue_list])


problem = trade_problem()

res = minimize(problem,
               algorithm,
               ('n_gen', NGEN),
               verbose=False
               )

print("最佳影片: %s" % res.X.astype(int))
print("分數: %s" % -res.F)
