from twitter_client import TwitterProvider
from threading import Thread
from twitter_client import TwitterStreamListener
from domain import InMemoryHashtagCounter, SimpleTimerHashtagSubstracter, BufferedHashtagSubstracter
from plot_client import PlotProvider
from handlers import HashtagHandler


class Application:
    """
    Bootstrap and run the application
    """
    def __init__(self, keywords, bucket_time):
        self._bucket_time = bucket_time
        self._keywords = keywords

    def start(self):
        # this ins
        hashtag_counter = InMemoryHashtagCounter()

        # I left may naive timer implementation commented out but it can work just as well if replacing the commented lines
        #hashtag_subtracter = SimpleTimerHashtagSubstracter(hashtag_counter, self._bucket_time)

        hashtag_subtracter = BufferedHashtagSubstracter(hashtag_counter, self._bucket_time)
        hashtag_handler = HashtagHandler(hashtag_counter, hashtag_subtracter)
        stream_listener = TwitterStreamListener(hashtag_handler)
        provider = TwitterProvider(self._keywords, stream_listener)
        plot_provider = PlotProvider(hashtag_counter)

        thread = Thread(target=provider.start)
        thread.start()

        plot_provider.start()
