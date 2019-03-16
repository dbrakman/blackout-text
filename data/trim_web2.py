with open('propernames.txt', 'r') as f:
    propernames = f.readlines()

with open('words_scrabble_2letter.txt', 'r') as f:
    words2letter = f.readlines()

with open('words_scrabble_3letter.txt', 'r') as f:
    words3letter = f.readlines()

with open('words_scrabble_4letter.txt', 'r') as f:
    words4letter = f.readlines()


with open('web2.txt', 'r') as web2:
    with open('web2_trimmed.txt', 'w') as outfile:
        for line in web2:
            # This could be done more efficiently by tracking indices in each sublist, but it's run once
            if not line.islower():
                if line in propernames:
                    outfile.write(line)
            elif len(line) == 2:
                if line in ['a\n', 'i\n']:
                    outfile.write(line)
            elif len(line) == 3:
                if line in words2letter:
                    outfile.write(line)
            elif len(line) == 4:
                if line in words3letter:
                    outfile.write(line)
            elif len(line) == 5:
                if line in words4letter:
                    outfile.write(line)
            else:
                outfile.write(line)
