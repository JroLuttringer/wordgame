with open("clean-fr-dico", 'w', encoding = 'latin-1') as new_dico:
	with open("francais.txt", encoding='latin-1') as og:
		for line in og.readlines():
			if len(line.rstrip()) == 1:
				continue
			if len(line.rstrip().split(' ')) > 1:
				continue
			new_dico.write(line)
		
