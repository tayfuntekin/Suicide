#!/usr/bin/env python

import sys

# Read input from standard input
for line in sys.stdin:
    # Remove leading/trailing whitespaces and split by tab
    line = line.strip().split('\t')

    # Ensure the line contains both preprocessed text and sentiment
    if len(line) == 2:
        preprocessed_text, sentiment = line

        # Encode sentiment as 0 or 1
        encoded_sentiment = 0 if sentiment == 'negative' else 1

        # Emit the preprocessed text and encoded sentiment as output
        print(f"{preprocessed_text}\t{encoded_sentiment}")
