from typing import List
from spellchecker import SpellChecker
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords as nltk_stopwords
from nltk import pos_tag
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize , sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import inflect
import re
import contractions
from typing import Dict
from collections import defaultdict
from datetime import datetime
import pycountry
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def custom_preprocessor(text):

    lowercase_text = _lowercase_tokens(text)
    expanded_text = expand_contractions(lowercase_text)
    cleaned_text = remove_html_and_links(expanded_text)

    return cleaned_text

#==================================================================#

def custom_tokenizer(text,online=False):
    
    tokens, ddate = _get_tokenz(text)
    
    cleaned_tokens = _remove_punctuations(tokens)

    # apply Spell Checker for online query 
    if online:
        corrected_token = spell_checker(cleaned_tokens)
    else:
        corrected_token = cleaned_tokens

    stop_words_removed = _stop_words(corrected_token)
    
    dateNormalization = normalize_dates(ddate)
    
    tokenWithoutCountry, countryNormalization = _normalize_country_names(stop_words_removed)
    
    lemma_tokens = _lemma_tokens(tokenWithoutCountry)
    
    return lemma_tokens + dateNormalization + countryNormalization

#==================================================================#
def _lowercase_tokens(text:list) -> str:
    lowercase_words = text.lower()
    #print("lowercase_text",lowercase_words)
    return lowercase_words 

#==================================================================#
def expand_contractions(text):

    expanded_text = contractions.fix(text)
    #print("expanded_text",expanded_text)
    return expanded_text
    
#==================================================================#
def remove_html_and_links(text):
    # Remove html tags
    clean_text = re.sub(r'<.*?>', '', text)
    # Remove URLs
    clean_text = re.sub(r'http\S+', '', clean_text)
    #print("cleaned_text",clean_text)
    return clean_text
    
#==================================================================#
def _get_tokenz(text: str) -> list:
    
    date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|'\
                r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})|'\
                r'(\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{2,4})|' \
                r'((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},\s+\d{2,4})|' \
                r'(\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{2,4})|' \
                r'((january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{2,4})'

    matches = re.findall(date_pattern, text)
    #print("---------------------",matches)
    dates=[]
    for match in matches:
        date = next(item for item in match if item) 
        dates.append(date)
        text = text.replace(date,"")

    tokens = word_tokenize(text)
    
    # print("tokens",tokens)
    # print("date",dates)

    return tokens , dates 

#==================================================================#
def _remove_punctuations(tokens: list) -> list:


    tokenizer = RegexpTokenizer(r'\w+')
    cleaned_token = tokenizer.tokenize(' '.join(tokens))
    
    #print("_remove_punctuations",cleaned_token)
    return cleaned_token

#==================================================================#
def _stop_words(tokens:list) -> list:
    stopwords = nltk_stopwords.words("english")
    filtered_tokens = [token for token in tokens if token not in stopwords]
    #print("**************stop words**************")
    #print("_stop_words",filtered_tokens)
    return filtered_tokens

#==================================================================#
def get_wordnet_pos(tag_parameter):

    tag = tag_parameter[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    
    return tag_dict.get(tag, wordnet.NOUN)

def _lemma_tokens(tokens:list) -> list:
    tagged_tokens = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in tagged_tokens]
    #print("_lemma_tokens",lemmatized_words)
    
    return lemmatized_words

#==================================================================#
def normalize_dates(tokens:list) -> list:
    date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|' \
                    r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})|' \
                    r'(\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{2,4})|' \
                    r'((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},\s+\d{2,4})|' \
                    r'(\d{1,2}\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{2,4})|' \
                    r'((january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{2,4})'

    format_strings = ['%d-%m-%Y', '%d/%m/%Y', '%d.%m.%Y', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%d %b %Y', '%b %d, %Y',
                        '%d %B %Y', '%B %d, %Y', '%m/%d/%Y', '%m-%d-%Y', '%m.%d.%Y', '%d-%m-%y', '%d/%m/%y', '%d.%m.%y',
                        '%y-%m-%d', '%y/%m/%d', '%y.%m.%d', '%d %b %y', '%b %d, %y',
                        '%d %B %y', '%B %d, %y', '%m/%d/%y', '%m-%d-%y', '%m.%d.%y']

    # Loop through each token and replace valid date strings with normalized date strings
    for token in tokens:
        #print("BEFORE if matches",token," == ")
        matches = re.findall(date_pattern, token)
        #print("test if matches",matches)
        if matches:
            # this is to get the first item that has value in tuple
            match = next(item for item in matches[0] if item)
            #print("the match is ",match)
            for fmt in format_strings:
                try:
                    date_obj = datetime.strptime(match, fmt)
                    break  # Stop trying format strings when one succeeds
                except ValueError:
                    pass
            else:
                continue  
            normalized_date = date_obj.strftime('%Y-%m-%d')
            position = tokens.index(token)
            tokens[position]=token.replace(match, normalized_date)
            
    #print("normalize_dates",tokens)
    return tokens

    
#==================================================================#
def _normalize_country_names(tokens:list) -> list:
    
    country_codes = set(country.alpha_3 for country in pycountry.countries)
    countryName=[]
    for token in tokens.copy():
        if token.upper() in country_codes:
            try:
                country = pycountry.countries.lookup(token.upper())
                tokens.remove(token)
                countryName.append(country.name)
            except LookupError:
                pass
                

    # print("_normalize_country_names",countryName)
    # print("token without country",third_list)

    return tokens,countryName
#==================================================================#
def normalize_number(tokens:list):
    p = inflect.engine()
    converted_words = [p.number_to_words(word) if word.isdigit() else word for word in tokens]
    return converted_words
    
#==================================================================#
def is_english_word(tokens:list):
    english_words = [token for token in tokens if bool(wordnet.synsets(token))]
    #print("english_words",english_words)
    return english_words
#==================================================================#
def spell_checker(tokens:list) -> list:
    spell = SpellChecker()
    misspelled = spell.unknown(tokens)
    # print("--------",misspelled)
    for i, token in enumerate(tokens):
        if token in misspelled:
            suggestions = spell.candidates(token)
            #print("hello",suggestions)
            if suggestions:
                corrected = spell.correction(token)
                if corrected is not None:
                    tokens[i] = corrected
    return tokens