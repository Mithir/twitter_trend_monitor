from trends_monitor import Application
from settings import Settings

if __name__ == '__main__':
    bucket_time = None
    keywords = input('Which keywords should we monitor?')

    """
    while True:
        try:
            bucket_time = int(input('How long should the bucket time be (in seconds)?'))
            if bucket_time <= 2:
                raise ValueError
            break
        except ValueError:
            print("you should enter a number higher than 2")
"""

    if bucket_time is None:
        bucket_time = Settings.DEFAULT_TREND_BUCKET_TIME_IN_SECONDS

    app = Application(keywords, bucket_time)
    app.start()
