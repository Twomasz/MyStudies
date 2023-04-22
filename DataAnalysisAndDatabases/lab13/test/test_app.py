from app import hello, extract_sentiment, text_contain_word, bubbleSort
import pytest


def test_hello():
    got = hello("Aleksandra")
    want = "Hello Aleksandra"

    assert got == want


testdata1 = ["I think today will be a great day"]


@pytest.mark.parametrize('sample', testdata1)
def test_extract_sentiment(sample):

    sentiment = extract_sentiment(sample)

    assert sentiment > 0


testdata2 = [('There is a duck in this text', 'duck', True),
             ('There is nothing here', 'duck', False)]


@pytest.mark.parametrize('sample, word, expected_output', testdata2)
def test_text_contain_word(sample, word, expected_output):

    assert text_contain_word(word, sample) == expected_output


testdata3 = [[64, 34, 25, 12, 22, 11, 90]]


@pytest.mark.parametrize('sample', testdata3)
def test_bubbleSort(sample):
    actual = bubbleSort(sample)
    expected = sample.sort()

    assert actual == expected
