from unittest import TestCase
from handlers import HashtagHandler
from unittest.mock import patch


class TestHashtagHandler(TestCase):
    @patch('domain.InMemoryHashtagCounter')
    @patch('domain.SimpleTimerHashtagSubstracter')
    def test_handle_retweet(self, mock_counter, mock_subtracter):
        # given
        handler = HashtagHandler(mock_counter, mock_subtracter)
        status = Object()
        status.retweeted_status = 'something'

        # when
        handler.handle(status)

        # then
        assert not mock_counter.add.called
        assert not mock_subtracter.subtract.called

    @patch('domain.InMemoryHashtagCounter')
    @patch('domain.SimpleTimerHashtagSubstracter')
    def test_handle_tweet_with_hashtags(self, mock_counter, mock_subtracter):
        # given
        hashtag1 = "hashtag1"
        hashtag2 = "hashtag2"
        handler = HashtagHandler(mock_counter, mock_subtracter)
        status = Object()
        status.entities = {"hashtags": [{'text': hashtag1}, {'text': hashtag2}]}
        # when
        handler.handle(status)

        # then
        mock_counter.add.assert_any_call(hashtag2)
        mock_counter.add.assert_any_call(hashtag1)
        assert mock_counter.add.call_count == 2

        assert mock_subtracter.subtract.call_count == 1

    @patch('domain.InMemoryHashtagCounter')
    @patch('domain.SimpleTimerHashtagSubstracter')
    def test_handle_no_hashtags(self, mock_counter, mock_subtracter):
        # given
        handler = HashtagHandler(mock_counter, mock_subtracter)
        status = Object()
        status.entities = {"hashtags": []}

        # when
        handler.handle(status)

        # then
        assert not mock_counter.add.called
        assert not mock_subtracter.subtract.called


class Object:  # help with mocking
    pass
