import re
import uuid
import nltk
import spacy
from functools import partial
from nltk.corpus import wordnet
from nltk.metrics import edit_distance

import emot
import enchant
from textacy import preprocessing
from deepmultilingualpunctuation import PunctuationModel



knowledge_base = """
Hello,
My name is Jonathan Smith from ExGen Enterprises I recently spoke to your customer service agent Emily and she was quite helpful however I still have some questions about the product I was looking at earlier the product in question is the new espresso machine

I'm really intersted in this product, but I noticed some discrepances between the specifications on the page and what Emily mentioned. Could you clarify if the water tank capacity is 1.5 litres or 1.6 liters? Also, how long does the delivery take? I'm planning a vacation soon and want to make sure it arrives on time. Last time I ordered a similar product, it was delivered to my neighbour's flat instead of mine while I was haway.

Please respond at your earliest convenience as I'm keen to make a purchase soon. You can reach me on 12345678910 or via email at jonathan.smith@example.com, better still, you can reach out to me on Twitter with @JonathanSmith_78.

Thank you.
"""

class SpellCorrector:
    def __init__(self, lang='en_US', domain_wordlist_path=None, max_dist=2):
        if domain_wordlist_path:
            self.d = enchant.DictWithPWL(lang, domain_wordlist_path)
        else:
            self.d = enchant.Dict(lang)

        self.max_dist = max_dist

    def correct(self, token):
        if not self.d.check(token):
            suggestions = self.d.suggest(token)
            if suggestions and edit_distance(token, suggestions[0]) <= self.max_dist:
                return suggestions[0]
            

# Correcting spelling errors 

# Initialize SpellCorrector class
sc = SpellCorrector()

# Create a spacy document
nlp = spacy.load('en_core_web_sm')
doc = nlp(knowledge_base) # convert knowledge base into processed text which contans information
                          # about the tokens, their linguistic featues and relationships. 

# Extract words: Code iterates through the token in the doc and extracts the words that are alphabetic, ignoring punctuation and numbers.
words = [token.text for token in doc if token.is_alpha]

# Get proposed word corrections 
corrections = {}
for word in words:
    correction = sc.correct(word)
    if correction:
        corrections[word] = correction

# Show and validate suggested corrections 
for word, correction in corrections.items():
    print(f'{word} -> {correction}')

# Commit corrections
for word, correction in corrections.items():
  knowledge_base = re.sub(fr'\b({word})\b', correction, knowledge_base)

  