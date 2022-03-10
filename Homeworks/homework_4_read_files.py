import re


def get_index_by_word(look_for: str, list_:list[tuple])->int:
	"""
	Get tuple index from list
	:param look_for: String key that we are looking for
	:param list_: List of tuples
	:return: index { int }
	"""
	for item in list_:
		if look_for == item[0]:
			return list_.index(item)
	return -1


def merge_words(words_1: list[tuple], words_2: list[tuple]):
	"""
	Merge two word lists 
	:param words_1: List with matched words and times used
	:param words_2: List with matched words and times used
	:return: Merged list
	"""
	merged = []
	words_only_1 = [i[0] for i in words_1]
	words_only_2 = [i[0] for i in words_2]

	# match words from file 1 against file 2
	for word in words_1:
		if word[0] in words_only_2:
			index = get_index_by_word(word[0], words_2)

			if index != -1:
				merged.append((word[0], word[1], words_2[index][1]))
		else:
			merged.append((word[0], word[1], 0))

	# match words from file 2 against file 1
	for word in words_1:
		if word[0] in words_only_2:
			index = get_index_by_word(word[0], words_2)

			if index != -1:
				if (word[0], word[1], words_2[index][1]) not in merged:
					merged.append((word[0], word[1], words_2[index][1]))
		else:
			if (word[0], word[1], 0) not in merged:
				merged.append((word[0], word[1], 0))

	return merged


def read_file(file: str, filter_pattern: str=r'\W+'):
	"""
	Filter given file and return key words + count
	:param file: File name if in same dir. If not full path
	:param filter_pattern: Regex filter pattern
	:return: list with matched keywords and times used
	"""
	all_words = {}
	with open(file, mode="rt", encoding="utf-8") as f:
		for line in f:
			words = line.strip().split("#")[0]
			words = re.split(filter_pattern, words.strip())
			for word in words:
				if word != "":
					all_words[word] = all_words.get(word, 0) + 1

	wc_items: list[tuple[str, int]] = list(all_words.items())
	wc_items.sort(key=lambda t: t[1], reverse=True)
	return wc_items


def calc_difference(list_: list[tuple])->int:
	"""
	Calculate the difference between the two files
	:param list_: List with tuples ( word, times in file-1, times in file-2 )
	:return: int
	"""
	total_items = len(list_)
	test = []
	for item in list_:
		current = item[1] - item[2]
		if current < 0:
			current *= -1
		test.append(current)

	print(test)
	return 0

if __name__ == '__main__':
	file_1_words = read_file("file_to_read_1.py")
	file_2_words = read_file("file_to_read_2.py")
	# TODO change the way we sort the lists
	#	Calc the difference
	merged = merge_words(file_1_words, file_2_words)
	calc_difference(merged)
	# print(calc_difference(merged))

	print()
