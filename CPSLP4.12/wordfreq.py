def get_word_frequencies(filename):
    # Empty dictionary for word frequencies
    freqs = {}

    # Read in the file
    with open(filename, 'r') as f:
	    for line in f:
	        for word in line.split():
	            if word in freqs:
	                freqs[word] += 1
	            else:
	                freqs[word] = 1
    return freqs