import os

class Hinter:
	'''
	load a dictionary and obtain some suggestions
	regarding the next possible letters or compatible words.
	'''
	def __init__(self, words):
		self.words = words

	@staticmethod
	def load_english_dict():
		
		ENGLISH_FILENAME = "dict" + os.sep + "english.txt"
		words = [i.replace("\n","") for i in open(ENGLISH_FILENAME)]
		return Hinter(words)

	def compatible_words(self, word, limit = 10):

		output = []
		word_count = 0
		#Cycle through all the words to find the ones that starts with "word"
		for i in self.words:
			if i.startswith(word):
				output.append(i)
				word_count+=1
			if word_count>=limit: #If limit is reached, exit
				break
		return output

	def next_letters(self, word):
		words = self.compatible_words(word, 100)
		letters = []
		for i in words:
			if len(i)>len(word): #if the "word" is longer than a compatible word, skip
				letter = i[len(word):len(word)+1] #Get the following letter
				if not letter in letters: #Avoid duplicates
					letters.append(letter)
		return letters

	def does_word_exists(self, word):
		if word in self.words:
			return True
		else:
			return False

	def most_probable_letter(self, clf, classes, linearized_sample, word):
		if word=="":
			return None
		
		probabilities = clf.predict_log_proba(linearized_sample)
		ordered = sorted(classes)
		values = {}
		for i in range(len(probabilities[0])):
			values[round(probabilities[0,i], 5)] = classes[ordered[i]]
		ordered = sorted(values, reverse=True)
		possible_letters = self.next_letters(word)
		for i in ordered:
			if values[i] in possible_letters:
				return values[i]
		return None

