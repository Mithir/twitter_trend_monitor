class HashtagHandler:
    """
    The listener should call this handler with new statuses.
    when handling a new status it will extract the hashtags and call the hashtag_counter and hashtag subtracter
    """
    def __init__(self, hashtag_counter, hashtag_subtracter):
        self._hashtagCounter = hashtag_counter
        self._hashtagSubtracter = hashtag_subtracter

    def handle(self, status):
        if hasattr(status, 'retweeted_status'):  # not interested in retweets
            return

        hashtag_metadatas = status.entities.get('hashtags')
        if len(hashtag_metadatas) == 0:  # only interested in tweets with hashtags
            return

        hashtags = []
        for hashtagMetadata in hashtag_metadatas:
            curr_hashtag = hashtagMetadata['text']  # consider filtering if hashtag equals the keyword
            hashtags.append(curr_hashtag)
            self._hashtagCounter.add(curr_hashtag)

        self._hashtagCounter.print_most_common(5)
        self._hashtagSubtracter.subtract(hashtags)
