import sys
import random
from multiprocessing.dummy import Pool as ThreadPool  # threads used to get confs
import threading
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

dico = []
dico_size = 0
ptr = {}

def debug(str):
	if False:
		print(str)
		
def load_data(f):
	global dico 
	global dico_size
	global ptr
	with open(f, encoding="latin-1") as fdico:
		for line in fdico.readlines():
			word = line.rstrip()
			if len(word) <=1:
				continue
			dico.append(word)
			if word[0] not in ptr:
				ptr[word[0]] = dico_size
			if word[0:2] not in ptr:
				ptr[word[0:2]] = dico_size 
			dico_size += 1	

def supprime_accent(self, ligne):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'] }
        for (char, accented_chars) in accents.iteritems():
            for accented_char in accented_chars:
                ligne = ligne.replace(accented_char, char)
        return ligne
        
        
def get_random_word():
	return dico[random.randint(0, dico_size-1)]

def get_lookup_zone(str):
	if len(str) >= 2 and str[0:2] in ptr:
		debug("Found shortcut for %s" % str[0:2])
		return ptr[str[0:2]]
	elif  str[0] in ptr:
		debug("Found shortcut for %s" % str[0])
		return ptr[str[0]]	
	
	return None

def longest_word(list, word):
	clean_list = []
	for x in list:
		if x not in word:
			clean_list.append(x)
		
	if len(clean_list) == 0:
		return ""
		
	return clean_list[random.randint(0,len(clean_list))-1]
	
	
	choice = ""
	for w in list:
		if len(w) > len(choice):
			choice = w
	return choice

def print_final_answer(final_answer):
	mishmash = final_answer[0]
	for w in final_answer[1:]:
		for x in range(0, len(w) -1):
			if w[:x] == mishmash[-x:]:
				mishmash += w[x:]
				break
		
		
	return mishmash

def research_words(word):
	max_next_word_len = len(word) - 2
	next_words = []
	finished = False
	final_answer = []
	final_answer.append(word)
	while not finished:
		for x in range(2, max_next_word_len):
			debug("Trying to find a word beginning with %s" % word[-x:])
			lookup_start = get_lookup_zone(word[-x:])
			if lookup_start is None:
				break
			while(True):
				if dico[lookup_start][:x] == word[-x:]:
					next_words.append(dico[lookup_start])
					#print("next word %s" % dico[lookup_start])
				lookup_start += 1
						
				if len(dico) == lookup_start or len(dico[lookup_start]) == 0 or dico[lookup_start][0] != word[-x]:
					#debug("Broke because %s vs %s" % (dico[lookup_start][0], word[-x]))
					break
		chosen_word = longest_word(next_words,word )
		if chosen_word == "" or chosen_word == word:
		#	print_final_answer(final_answer)
			finished = True
		if chosen_word != "":
			final_answer.append(chosen_word)
		word = chosen_word
		max_next_word_len = len(word) - 1
		next_words = []
	return final_answer
	
print("loading data from %s" % sys.argv[1])
load_data(sys.argv[1])
#print(ptr)
if len(sys.argv) <= 2:
	print("Choosing random word")
	word = get_random_word()
	print("Chose %s" % word)
else:
	print("Beginning with word %s" % sys.argv[2])
	word = sys.argv[2]


number_of_threads = 50
pool = ThreadPool(number_of_threads)
pool_args = []
for x in range(0, number_of_threads):
	pool_args.append(word)
	results = pool.map(research_words, pool_args)

print("===============================================")
unique = []
unique_mish = []
for x in results:
	if x not in unique:
		unique.append(x)

for x in unique:
	unique_mish.append(print_final_answer(x))
	
print("Done")
print("Number of unique mishymashes: %s" % len(unique))
print("Longest mishymash (words)   : %s" % len(max(unique, key=len)))
print("Longest mishymash (letters) : %s" % len(max(unique_mish, key=len)))
print("===============================================\n")
for r in results:
	print(r)
print("")	

for r in results:
	print(print_final_answer(r))
	

if True:
	
	G = nx.Graph()
	edges = []
	added_nodes = []
	pos_x = 0
	pos_y = 0
	
	
	i = 0
	number_of_results = len(results)
	G.add_node(results[0][0], pos=(0,int(number_of_results /2)*1000))
	added_nodes.append(results[0][0])
	node_sizes = []
	
	for r in results:
		pos_x = 0
		for x in range(0,len(r)):					
			if r[x] not in added_nodes:
				added_nodes.append(r[x])
				node_sizes = len(r[x]) * 600
				G.add_node(r[x], pos=(pos_x,pos_y))
			pos_x += 1000
		pos_y += 1000
					
		
	edges = {'blue':[], 'black':[], 'red':[], '#db8625':[], 'green':[], 'gray':[], 'cyan':[], '#ed125b':[]}
	
	for r in results:
		for x in range(0,len(r)-1):
			edges[list(edges.keys())[i]].append((r[x],r[x+1]))
		i = (i+1) % len(edges.keys())
			
	
	pos = nx.get_node_attributes(G,'pos')
	
	
	nx.draw_networkx_nodes(G, pos, 
                       node_color = 'w', node_size = node_sizes )
        
	nx.draw_networkx_labels(G, pos)
	for k in edges.keys():
		nx.draw_networkx_edges(G, pos, edgelist=edges[k], edge_color = k, width = 2, arrows=True)
	#nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
	
	plt.show()
		




