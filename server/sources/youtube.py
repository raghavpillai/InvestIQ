import os
from apiclient.discovery import build
from flair.models import TextClassifier
classifier = TextClassifier.load("en-sentiment")
from flair.data import Sentence

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class Message:
    def __init__(self, perception, popularity, platform):
        self.perception = perception
        self.popularity = popularity
        self.platform = platform


class Youtube:
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    def get_messages(self, topic):
        messages = list()
        title_request = self.youtube.search().list(
            q=topic,
            part="snippet",
            type="video",
            publishedAfter="2021-11-07T00:00:00Z",
            maxResults=100,
        )
        res1 = title_request.execute()
        ids = ""
        titles = list()
        for item in res1["items"]:
            titles.append(item["snippet"]["title"])
            ids = ids + str(item["id"]["videoId"]) + ","
        ids = ids[:-1]
        statistics_request = self.youtube.videos().list(
            id=ids, part="statistics", maxResults=100
        )
        res2 = statistics_request.execute()
        index = 0
        for item in res2["items"]:
            title = titles[index]
            sentence = Sentence(title)
            classifier.predict(sentence)
            if sentence.labels[0].score < 0.8:
                perception = 0
            elif sentence.labels[0].value == "POSITIVE":
                perception = 1
            else:
                perception = -1
            print(item["statistics"])

            views = int(item["statistics"]["viewCount"])
            if "likeCount" in item["statistics"]:
                likes = int(item["statistics"]["likeCount"])
                dislikes = (
                    likes * 0.3
                )  # Temp solution, b4 int(item['statistics']['dislikeCount'])
                if dislikes == 0:
                    likeDislikeRatio = 1
                else:
                    likeDislikeRatio = likes / (dislikes + likes)
            else:
                likeDislikeRatio = 1
            perception *= likeDislikeRatio
            message = Message(perception, views, "Youtube")
            messages.append(message)
            index += 1
        return messages