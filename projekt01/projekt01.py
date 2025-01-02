import re
from collections import Counter
from ascii_graph import Pyasciigraph
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='nazwa pliku wejściowego')
parser.add_argument('--top_words', '-tw', type=int, default=10, help='ilość słów pokazanych w histogramie')
parser.add_argument('--character_minimum', '-cm', type=int, default=0,
                    help='minimalna ilość liter w rozważanych słowach')
args = parser.parse_args()


def count_word_frequencies(filename, top_words=10, min_len=0):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
            text = re.findall(r'\w+', text)  # magia ktora usuwa wszystkie znaki niepotrzebne
            text = [item for item in text if len(item) >= min_len]
            words_counts = Counter(text)
            most_common_words = words_counts.most_common(top_words)  # o moj boze to lista krotek

        return most_common_words
    except FileNotFoundError:
        print(f"Błąd: Plik '{filename}' nie został znaleziony")
        return 0


data = count_word_frequencies(args.filename, args.top_words, args.character_minimum)

graph = Pyasciigraph()
for line in graph.graph('Histogram częstotliwości występowania słów:', data):
    print(line)
