# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 14:56:59 2023

@author: Akhilesh
"""
#!pip install pyenchant

import enchant
import tqdm
from nltk.stem.snowball import SnowballStemmer
import re

def read_file(filename = "BERT-vocab.txt"):
    with open(filename, encoding="utf8") as txt:
        f = txt.readlines()
    return f
    

def trim_vocab(f):
    word_list = f
    
    print("Initial Vocabulary list - length = %d"%len(word_list))
    print("-"*100)    
    print("Replace new line '\n' with a null character...")
    print("*"*50)
    print("""CODE - word_list = [word.replace('\n', '') for word in word_list]
          """)
    print("*"*50)
    # 1. Replace new line '\n' with a null character
    word_list = [word.replace('\n', '') for word in word_list]
    print("Done.")
    print("Vocabulary list length = %d"%len(word_list))
    print("-"*100)
    
    # 2. Remove words enclosed in [..]
    print("Removing words enclosed in []")
    print("*"*50)
    print("""CODE - word_list = [word for word in word_list if not re.match(r'\[.*\]', word)]
          """)
    word_list = [word for word in word_list if not re.match(r'\[.*\]', word)]
    print("*"*50)
    print("Done.")
    print("Vocabulary list length = %d"%len(word_list))
    print("-"*100)
    
    

    print("Remove words containing a mixture of numeric characters and special characters")
    print("*"*50)
    print("""CODE - pattern = re.compile("^[A-Za-z]+$")
          """)
    # 3. Remove words containing a mixture of numeric characters and special characters
    # Define a regular expression pattern to match words with only letters
    pattern = re.compile("^[A-Za-z]+$")
    
    # Filter out words that match the pattern
    word_list = [word for word in word_list if pattern.match(word)]
    print("*"*50)
    print("Done.")
    print("Vocabulary list length = %d"%len(word_list))
    print("-"*100)
       
    print("Removing words with a lenght of 1]")
    print("*"*50)
    print("""CODE - word_list = [word for word in word_list if len(word) > 1]
          """)
    # 4. Remove single-character tokens.
    word_list = [word for word in word_list if len(word) > 1]
    print("*"*50)
    print("Done.")
    print("Vocabulary list length = %d"%len(word_list))
    print("-"*100)
    
    return word_list

def apply_pyenchant_spell(word_list):
    li = []
    d = enchant.Dict("en_US")
    print("Applying Spell!")
    for i in tqdm.tqdm(word_list):
        word = i.replace("\n", "")
        if d.check(word):
            li.append(word)
    print("Done!")
    print("Vocabulary list length = %d"%len(li))
    print("-"*100)
    return li

def apply_porter_stemmer(li):
    print("Trimming out sub words")
    stemmer = SnowballStemmer("english")
    stemmed_words = []
    for word in li:
        stemmed_words.append(stemmer.stem(word))
    
    stemmed_words_set = sorted(list(set(stemmed_words)))
    print("Done!")
    print("Vocabulary list length = %d"%len(stemmed_words_set))
    print("-"*100)
    return stemmed_words_set
    
def main(filename = "BERT-vocab.txt"):
    f = read_file(filename)
    word_list = trim_vocab(f)    
    enchanted_li = apply_pyenchant_spell(word_list)
    final_li = apply_porter_stemmer(enchanted_li)
    print("Final Vocabulary Length = %d"%len(final_li))
    
if __name__ == '__main__' :
    main()        