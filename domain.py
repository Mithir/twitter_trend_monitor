from threading import Timer
from collections import Counter


class BufferedHashtagSubstracter:
    """
    This class is responsible of keeping the hashtag counter in line with the desired bucket(which is given in seconds)
    it buffers the hashtags for a calculated amount of time (delay_in_seconds) and then subtracts it from the counter
    this way we can promise we won't get more than divide_factor(100) threads running in the same time
    """
    def __init__(self, hashtag_counter, bucket_time_in_seconds, divide_factor=100, minimal_buffer_time=2):
        self._hashtag_counter_to_subtract = Counter()
        self._hashtag_counter = hashtag_counter

        self._bucket_time_in_seconds = bucket_time_in_seconds
        buffer_time = self._bucket_time_in_seconds / divide_factor  # this determines how many hanging threads we will have

        if buffer_time < minimal_buffer_time:
            self._delay_in_seconds = minimal_buffer_time
        else:
            self._delay_in_seconds = buffer_time

        self._repeated_timer = None
        self.start_buffer_timer()

    def subtract(self, hashtags):
        for hashtag in hashtags:
            self._hashtag_counter_to_subtract[hashtag] += 1
        print('To Subtract:')
        print(self._hashtag_counter_to_subtract.most_common(5))

    def start_buffer_timer(self):
        self._repeated_timer = RepeatedTimer(self._delay_in_seconds, self.act_on_buffer)

    def act_on_buffer(self):
        if len(self._hashtag_counter_to_subtract) == 0:
            print("no hashtags to subtract")
            return

        t = Timer(self._bucket_time_in_seconds, self._hashtag_counter.subtract_counter, [self._hashtag_counter_to_subtract])
        t.start()
        self._hashtag_counter_to_subtract = Counter()  # clean the buffer

    def stop_timer(self):
        self._repeated_timer.stop()


class InMemoryHashtagCounter:
    """
    This class is a simple wrapper on top of the Counter class.
    """
    def __init__(self):
        self._hashtagsCounter = Counter()

    def add(self, hashtag):
        self._hashtagsCounter[hashtag] += 1

    def subtract_hashtag(self, hashtags):
        for hashtag in hashtags:
            if self._hashtagsCounter[hashtag] <= 1:
                del self._hashtagsCounter[hashtag]
            else:
                self._hashtagsCounter[hashtag] -= 1

    def get_most_common(self, amount):
        return self._hashtagsCounter.most_common(amount)

    def subtract_counter(self, hashtag_counter_to_subtract):
        print("subtracted")
        print(hashtag_counter_to_subtract)
        print("subtracted")
        self._hashtagsCounter.subtract(hashtag_counter_to_subtract)

    def print_most_common(self, amount):  # for tests
        print(self._hashtagsCounter.most_common(amount))


class SimpleTimerHashtagSubstracter:
    """
    This class is responsible of keeping the hashtag counter in line with the desired bucket(which is given in seconds)
    this is a simple approach, every new list of hashtag we get, we set a time for the bucket_time to subtract them
    it is of course not going to work well when the bucket is big and or when there are lots of hashtags added
    """
    def __init__(self, hashtag_counter, delay_in_seconds):
        self._delay_in_seconds = delay_in_seconds
        self._hashtag_counter = hashtag_counter

    def subtract(self, hashtags):
        t = Timer(self._delay_in_seconds, self._hashtag_counter.subtract_hashtag, [hashtags])
        t.start()


class RepeatedTimer(object):
    """
    taken from https://stackoverflow.com/questions/2398661/schedule-a-repeating-event-in-python-3
    """
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
