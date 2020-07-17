import re
import json
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from rap_songs import list_of_rap_songs
from country_songs import list_of_country_songs

class HotSongs:
    def __init__(self, filename, genre, singer, title, year):
        self.filename = filename
        self.genre = genre
        self.singer = singer
        self.title = title
        self.year = year
        self.text = self.load_file()
        self.words = self.clean_text()
        self.count = self.word_count()
        self.stopword_filter = self.remove_stopwords()
        self.word_length = self.avg_word_length()
        self.stemmed_words = self.stemming()
        self.word_frequency = self.word_freqs()
        self.sorted_word_frequency = self.sort_word_dict()
        self.lexical_div = self.lexical_diversity()

    def load_file(self):
        try:
            file = open(self.filename, "r")
            text = file.read()
            file.close()
            return text
        except:
            print("ERROR: Could not open file " + self.filename)
            return None

    def clean_text(self):
        """Removes all characters that are not alphabets or spaces"""
        words = re.split(r"\W+", self.text.lower())
        words = [word for word in words if len(word) > 0]
        return words

    def word_count(self):
        """Calculates the number of words in lyrics"""
        count = 0
        for word in self.words:
            count += 1
        return count

    def remove_stopwords(self):
        """Filter out stop words using stopwords from nltk library"""
        stop_words = set(stopwords.words("english"))
        stopword_filter = [w for w in self.words if not w in stop_words]
        return stopword_filter

    def avg_word_length(self):
        """Calculates the average word length within lyrics"""
        word_length = 0
        for word in self.words:
            word_length += len(word)
        word_length /= self.count
        return word_length

    def stemming(self):
        """Simplifies the word into its root word"""
        porter = PorterStemmer()
        stemmed_words = [porter.stem(word) for word in self.words]
        return stemmed_words

    def word_freqs(self):
        """Determines how frequent a word appears within lyrics"""
        word_frequency = {}
        for word in self.words:
            if word in word_frequency:
                word_frequency[word] += 1
            else:
                word_frequency[word] = 1
        return word_frequency

    def sort_word_dict(self):
        """Sorting the word_frequency dictionary in descending order"""
        sorted_word_frequency = {
            k: v
            for k, v in sorted(
                self.word_frequency.items(), key=lambda item: item[1], reverse=True
            )
        }
        return sorted_word_frequency

    def lexical_diversity(self):
        "Calculates the lexical diversity of the lyric"
        lexical_div = len(list(self.sorted_word_frequency.items())) / sum(
            self.sorted_word_frequency.values()
        )
        return lexical_div

def process_songs(list_of_songs):
    """ Take in a dict of songs, return a list of song objects"""
    songs = []
    for name, info in list_of_songs.items():
        # Step 1: Make your object
        song = HotSongs(
            info["filename"],
            info["genre"],
            info["singer"],
            info["title"],
            info["year"],
        )
        songs.append(song)
    return songs


if __name__ == "__main__":

    rap_songs = process_songs(list_of_rap_songs)
    country_songs = process_songs(list_of_country_songs)

    print("\n\t Rap Songs")
    for song in rap_songs:
        print(song.title, song.count)
    print("\n\t Country Songs")
    for song in country_songs:
        print(song.title, song.count)




