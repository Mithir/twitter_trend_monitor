from unittest import TestCase
from domain import BufferedHashtagSubstracter, InMemoryHashtagCounter
import time


class TestBufferedHashtagSubstracter(TestCase):
    def test_act_on_buffer(self):
        # given
        hashtag_counter = InMemoryHashtagCounter()
        buffered_hashtag_subtracter = BufferedHashtagSubstracter(hashtag_counter, 1, 100, 1)
        hashtag = 'hashtag'
        hashtag_counter.add(hashtag)
        hashtag_counter.add(hashtag)

        most_common = hashtag_counter.get_most_common(1)
        assert most_common[0][0] == hashtag
        assert most_common[0][1] == 2

        # when
        buffered_hashtag_subtracter.subtract([hashtag])
        time.sleep(3)
        buffered_hashtag_subtracter.stop_timer()

        # then
        most_common = hashtag_counter.get_most_common(1)
        assert most_common[0][0] == hashtag
        assert most_common[0][1] == 1
