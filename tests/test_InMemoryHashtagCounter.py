from unittest import TestCase
from domain import InMemoryHashtagCounter


class TestInMemoryHashTagCounter(TestCase):
    def test_add_single(self):
        # given
        hashtag_counter = InMemoryHashtagCounter()
        hashtag = 'hashtag'
        hashtag_counter.add(hashtag)

        # when
        most_common = hashtag_counter.get_most_common(1)

        # then
        assert most_common[0][0] == hashtag
        assert most_common[0][1] == 1

    def test_add_multiple(self):
        # given
        hashtag_counter = InMemoryHashtagCounter()
        hashtag1 = 'hashtag1'
        hashtag2 = 'hashtag2'
        amount1 = 5
        amount2 = 3

        for i in range(amount1):
            hashtag_counter.add(hashtag1)

        for i in range(amount2):
            hashtag_counter.add(hashtag2)

        # when
        most_common = hashtag_counter.get_most_common(2)

        # then
        assert most_common[0][0] == hashtag1
        assert most_common[0][1] == amount1

        assert most_common[1][0] == hashtag2
        assert most_common[1][1] == amount2

