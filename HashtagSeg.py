import re
import pickle
import sys

st = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
class Segmenter:
	
	def __words(self, text):
		return re.findall('[a-z]+', text.lower()) 
	
	def __wordProb(self, word):
		return self.dictionary.get(word, 0) / self.total
	
	def __init__(self, dictionary):
		"""dictionary is a map of terms and frequency values (a dict file, serialized with pickle).
		It can be generated from a generic text, and it is used for segmentation."""
		#dictionary=open(os.path.join(RESOURCE_PATH, '1gramsGoogle'),'r')
		self.dictionary = pickle.load(open(dictionary))
		self.maxWordLength = max(map(len, self.dictionary))
		self.total = float(sum(self.dictionary.values()))

	def sample(self, text):
		rep = set()
		for ch in st:
			if ch*2 in text:
				rep.add(ch)
		dic_pro = {}
		dic_pro[text] = self.__wordProb(text)
		for ch in rep:
			count = text.count(ch)
			for i in range(2, count + 1):
				temp = text
				while True:
					temp = temp.replace(ch*i, ch*(i - 1))
					if temp.count(ch) <= i - 1:
						break
				prob = self.__wordProb(temp)
				dic_pro[temp] = prob
		sort = sorted(dic_pro.items(), key = lambda d:d[1], reverse = True)
		print sort[0][0]

	def get(self, text):
		"""Segment the hashtag text"""
		text=text.lower()
		if text[0] == '#':
			text = text[1:]
		probs, lasts = [1.0], [0]
		for i in range(1, len(text) + 1):
			prob_k, k = max((probs[j] * self.__wordProb(text[j:i]), j) for j in range(max(0, i - self.maxWordLength), i))
			probs.append(prob_k)
			lasts.append(k)
		words = []
		i = len(text)
		while 0 < i:
			words.append(text[lasts[i]:i])
			i = lasts[i]
		words.reverse()
		str = ''
		for word in words:
			str += word + " "
		return str
		#return words, probs[-1]

		
se = Segmenter('./normal_word.pkl')

#se.sample('fuuuuck')
# def get_hashtags(file):
	# fp = open(file,"r")
	# hashtags = []
	# for line in fp.readlines():
		# terms = line.strip('\r\n ').split(' ')
		# for term in terms:
			# if len(term) >= 1 and term[0] == '#':
				# hashtags.append(term)
	# fp.close()
	# return hashtags

# if __name__ == '__main__':
	# # if len(sys.argv) < 2:
		# # print 'Usage: dictPath files'
		# # sys.exit(0)
	# #se = Segmenter(sys.argv[1])
	# se = Segmenter('dict.pkl')
	# fp = open('subtaske_trial_data_updated_20141001.txt',"r")
	# new_word = []
	# for line in fp.readlines():
		# line = line.strip()
		# line = line.split("\t")[0]
		# if len(line) <= 1 or line[0] != '#':
			# new_word.append(line)
		# #print files
		# #hashtags = get_hashtags(files[0])
		# #fw = open(files[1],'wb')
		# # for hashtag in hashtags:
			# # fw.write(hashtag + '\t' + se.get(hashtag) + '\n')
			# # print se.get(hashtag)
		# # fw.close()
		# new_word.append(se.get(line))
	# print new_word
	
	
