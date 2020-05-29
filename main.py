#allow python to make https call out to nltk's site to download word data 
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context

import math
#use natural language toolkit for set of all words
import nltk
nltk.download('words')
from nltk.corpus import words

setOfAllWords = set(words.words())
combosCache = {}

#use a second dictionary source for validation (TODO: eventually use Oxford online API to check since Words with Friends uses that)
from PyDictionary import PyDictionary
dictionary=PyDictionary()

def isRealWord(myWord):
  isWord = myWord in setOfAllWords
  return isWord
  
def findPossibleCombos(letters):
  inCache = combosCache.get(letters)
  if inCache != None:
    # print('Found %s in cache' % letters)
    return list(inCache)
  combos=[]
  if len(letters) == 1:
    return letters
  else:
    for i in range(0, len(letters)):
      # Removing char at position i
      otherLetters = letters[:i] + letters[i+1:]
      for element in findPossibleCombos(otherLetters):
        # if len(element) > 1:
        #   if element not in combos:
        combos.append(element)
        combos.append(letters[i] + element)
    #cache the combos for this group of letters
    combosCache.update({letters: tuple(combos)})
    return combos

def findValidWords(words):
  validWords = []
  for word in words:
    if len(word) > 1:
      if word not in validWords:
        if isRealWord(word):
          validWords.append(word)
    # else:
      # print('%s is not a real word' % word)
  if len(validWords) > 2:
    validWords.sort(key=len, reverse=True)
  return validWords

def checkMeaning(words):
  print('Peforming lookups for meanings...')
  # double-check another dictionary for validity (TODO: use Oxford API)
  validAndCrossCheckedWords = []
  for validWord in validWords:
    meaning = dictionary.meaning(validWord)
    if meaning != None:
      validAndCrossCheckedWords.append(validWord)
      # print('Meaning of %s:' % validWord)
      # for k, v in meaning.items():
      #   print('{}: {}'.format(k, str(v)))
    # else:
    #   print('Could not find meaning of %s.' % validWord)
  print('Out of {} valid words, {} actually have meanings.'.format(len(words), len(validAndCrossCheckedWords)))
  if len(validAndCrossCheckedWords) > 0:
    print(validAndCrossCheckedWords)

def showProcessingStats(words):
  n = len(words)
  factorial = math.factorial(n-1)
  iterations = n * factorial * (2**(n-1))
  print('\'{}\' contains {} letters, which will require {} searches...'.format(words, n, iterations))

def prompt():
  myWord = input('Find me all words from (max of 8 letters): ')
  if myWord is None:
    print('Gotta enter something, bro.')
    return prompt()
  if len(myWord) > 8:
    print('Too many characters. Try with 8 or less.')
    return prompt()
  if len(myWord) < 2:
    print('Must at least enter 2 characters.')
    return prompt()
  return myWord

def filterBySubstring(words):
  subString = input('Filter valid words for particular letter sequence (max 7): ')
  if len(subString) < 1:
    print('Filtered nothing.')
    return words
  if len(subString) > 7:
    print('Too many characters. Try with 7 or less.')
    return filterBySubstring(words)
  return [match for match in words if subString in match]

while True:
  myWord = prompt()
  showProcessingStats(myWord)
  combos = findPossibleCombos(myWord)
  print('%i possible combinations found.' % len(combos))
  # print(combos)
  validWords = findValidWords(combos)
  print('Out of that, %i valid word(s) found:' % len(validWords))
  if len(validWords) > 0:
    for validWord in validWords:
      print(validWord, end = ", ")
    print('\n')
    # checkMeaning(validWords)
    filteredWords = filterBySubstring(validWords)
    if len(filteredWords) > 0:
      print('Found word(s) that contain your letters:')
      for filteredWord in filteredWords:
        print(filteredWord, end = ", ")
      print('\n')
    else:
      print('Did not find valid word(s) that contain your letters.')




