import re
import string
import nltk
import json

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from html.entities import name2codepoint
from bs4 import BeautifulSoup

regex = re.compile('[%s]' % re.escape(string.punctuation))
wordnet = WordNetLemmatizer()

f = open("bagOfWords.json", 'r')
bag = json.loads(f.read())

# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return chr(int(text[3:-1], 16))
                else:
                    return chr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = chr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def cleanText(text):
    text = text.lower()
    soup = BeautifulSoup(unescape(text), "html.parser")
    text = soup.get_text()  # nltk.clean_html(unescape(text))

    tokens = word_tokenize(text)
    new_tokens = []
    for t in tokens:
        nt = regex.sub(u'', t)
        if not nt == u'' and nt not in stopwords.words('english'):
            new_tokens.append(wordnet.lemmatize(nt))

    return " ".join(new_tokens)

def main(userInput, maxLen=160):
    userInput = cleanText(userInput)
    inputTok = userInput.split()[:160]
    inputTok = [str(bag[t]) if t in bag else "0" for t in inputTok]
    return " ".join(inputTok)


if __name__ == "__main__":
    userInput = """Install amdgpu drivers on Ubuntu Server 16.04.3 LTS.  I have made it completely through the process of installing the AMDgpu drivers; yet at the end of the process when I run a package query, it finds no matching package.
     wget --referer http://support.amd.com \ > https://www2.ati.com/drivers/linux/ubuntu/amdgpu-pro-17.40-492261.tar.xz

tar xvf amdgpu-pro-17.40-492261.tar.xz

cd /amdgpu-pro-17.40-492261

./amdgpu-pro-install --compute"""
    print(main(userInput))
