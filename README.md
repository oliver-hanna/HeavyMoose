#Heavy Moose

The app will recieve inputted text, parse it to a list of each individual strings.
Next, iterate through the list and check:
1: If each word is part of a pre-made text file of flagged common words that don't need to be parsed (e.g. "the", "it", etc.)
2: Query the word into a thesaurus api, if it is an adjective then add the first synonym to a dictionary like this:
{"key = index in list":"value = synonym of original word"}

Finally copy the original list and replace the indicies in the list with the words that correspond to the matching keys of the dictionary. The final list contains the final output.
