from textblob import TextBlob


def hello(name):
    output = f'Hello {name}'
    return output


def extract_sentiment(text):
    text = TextBlob(text)

    return text.sentiment.polarity


def text_contain_word(word: str, text: str):
    return word in text


def bubbleSort(array):
    n = len(array)

    swapped = False  # ADDED IMPROVEMENT (ALGORITHM MAY BE FINISHED EARLIER)

    for i in range(n-1):
        for j in range(0, n-i-1):
            if array[j] > array[j + 1]:
                swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]

    if not swapped:
        return
