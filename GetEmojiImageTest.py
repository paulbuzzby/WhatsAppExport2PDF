import requests
import re
import pickle

class EmojiConverter:
    def __init__(self):
        
        #self.data = requests.get('https://unicode.org/emoji/charts/full-emoji-list.html').text

        
        # with open("emojidata.pkl", "wb") as file:
        #     pickle.dump(self.data, file)
        with open("emojidata.pkl", "rb") as file:
            self.data = pickle.load(file)
    def to_base64_png(self, emoji, version=0):
        """For different versions, you can set version = 0 for , """
        html_search_string = r"""<img alt='{}' class='imga' src='data:image/png;base64,([^']+)'>""" #'

        matchlist = re.findall(html_search_string.format(emoji), self.data)
        return matchlist[version]

e = EmojiConverter()
b64 = e.to_base64_png("&#x1F600;")

print("Start")
print(b64)
print("END")


'''
# Save data to a binary file
with open("text_data.pkl", "wb") as file:
    pickle.dump(text, file)

# Load data from the binary file
with open("text_data.pkl", "rb") as file:
    loaded_text = pickle.load(file)

'''