#!/usr/bin/env python

import sys
import re

# Define the list of stopwords
stopwords = ['the', 'and', 'is', 'in', 'it', 'to', 'of', 'a']  # Add more stopwords as needed

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation and non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove leading and trailing whitespaces
    text = text.strip()

   
    text = ' '.join(text)

    return text

# Read input from standard input
for line in sys.stdin:
    # Remove leading/trailing whitespaces and split by tab
    line = line.strip().split('\t')

    # Ensure the line contains both text and sentiment
    if len(line) == 2:
        text, sentiment = line

        # Preprocess the text
        preprocessed_text = preprocess_text(text)

        # Emit the preprocessed text and sentiment as key-value pairs
        print(f"{preprocessed_text}\t{sentiment}")
