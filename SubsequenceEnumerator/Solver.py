import os

thisScriptDir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(thisScriptDir, '../data/web2_trimmed.txt')) as f:
    wordsAlpha = [w.strip().lower() for w in f.readlines()]


def findSubsequences(origText, wordList=wordsAlpha):
    # Assumes no duplicates in wordsAlpha
    # Optimization: every time a new word list is passed in, look in a persistence layer (Redis?) for a matching pickle
    wordList.sort(key=lambda s: (s[0], s[-1], s[1:-1]))

    # Subproblem S(i, j): set of valid subsequences that begin with s[i] and end with s[j], for s=origText
    # TODO: Optimize, using scipy to be snazzy with sparse matrices
    # TODO: Optimize, doing stuff with generators
    S = [[set() for c in origText] for c in origText]
    n = len(origText)
    # Populate the upper-triangular array of subproblems diagonally:
    # Main Diagonal of 1-letter words:
    for i in range(n):
        if origText[i] in wordList:
            S[i][i] = set(origText[i])
    for l in range(1, n):
        for i in range(n-l):
            j = i + l
            # Calc S(i, j)
            # 1) Look for single words that start with s[i] and end with s[j]
            S[i][j] = set(getSingleWords(origText[i:j+1], wordList))
            # 2) Also include the cross products of sets of subwords:
            for k in range(i+1, j):
                leftSide = set().union(*S[i][i:k])
                rightSide = S[k+1][j]
                spaceAtK = set(['{0} {1}'.format(leftstr, rightstr) for leftstr in leftSide for rightstr in rightSide])
                S[i][j].update(spaceAtK)
    cumul = set()
    for row in S:
        cumul.update(*row)
    return sorted(list(cumul), key=lambda x: (-1*len(x.replace(' ', '')), x.replace(' ', '')))


def getSingleWords(origSubstring, wordListCustomSorted):
    # 1) Binary search for first and last instance of words beginning with s[0], s[-1]
    target = firstAndLastChars(origSubstring)
    firstInd, lastInd = findIndicesOfStartsWithEndsWith(target, wordListCustomSorted)
    wordCandidates = wordListCustomSorted[firstInd:(lastInd + 1)]
    # 2) For word candidates with 3 or more letters, consider blacking-out some text in the middle
    #   (e.g. find "a#c#e" for "abcde" but not "ra#t###" for "rarthew")
    subseqCandidates = [word[1:-1] for word in wordCandidates]  # some may be empty; needed to preserve matching indices
    subseqIndices = set()
    for i in range(len(subseqCandidates)):
        if isSubsequence(subseqCandidates[i], origSubstring[1:-1]):
            subseqIndices.add(i)
    return [wordListCustomSorted[firstInd + ind] for ind in subseqIndices]


def firstAndLastChars(word):
    return word[0] + word[-1]


def findIndicesOfStartsWithEndsWith(target, wordListCustomSorted):
    """
    Binary search optimization for
        `[w for w in wordListCustomSorted if w.startswith(target[0]) and w.endswith(target[1])]`
    Only works for words of length > 2
    :param target: a 2-character string in which elt. 0 must match elt. 0 of words in the list, and elt. -1 must match
        elt. -1 of words in the list
    :param wordListCustomSorted: a list of words sorted first by their first letter, then by their last letter, then by
        all the letters in between
    :return: (i, j), where i is the first index of words satisfying the condition, and j is the last index thereof
    If words satisfy the condition, return indices corresponding to an empty slice, e.g. [-1:0]
    """
    n = len(wordListCustomSorted)
    firstInd = lastInd = n // 2
    if target == firstAndLastChars(wordListCustomSorted[0]):
        firstInd = 0
    elif target < firstAndLastChars(wordListCustomSorted[0]):
        return (-1, -1)
    if target == firstAndLastChars(wordListCustomSorted[n-1]):
        lastInd = n-1
    elif target > firstAndLastChars(wordListCustomSorted[n-1]):
        return (-1, -1)
    def firstIndIsMatch(firstInd):
        if firstInd == 0:
            return True
        else:
            return firstAndLastChars(wordListCustomSorted[firstInd]) == target and \
                   firstAndLastChars(wordListCustomSorted[firstInd-1]) < target
    def lastIndIsMatch(lastInd):
        if lastInd == n-1:
            return True
        else:
            return firstAndLastChars(wordListCustomSorted[lastInd]) == target and \
                   firstAndLastChars(wordListCustomSorted[lastInd+1]) > target

    lb = 1
    ub = n-1
    while not firstIndIsMatch(firstInd):
        if lb >= ub:
            return (-1, -1)
        if target > firstAndLastChars(wordListCustomSorted[firstInd]):
            lb = firstInd + 1
        else:
            ub = firstInd
        firstInd = (lb + ub) // 2
    lb = firstInd
    ub = n-2
    while not lastIndIsMatch(lastInd):
        if lb > ub:
            return (-1, -1)
        if target >= firstAndLastChars(wordListCustomSorted[lastInd]):
            lb = lastInd + 1
        else:
            ub = lastInd
        lastInd = (lb + ub) // 2
    return firstInd, lastInd


def isSubsequence(small, big):
    if len(small) > len(big):
        return False
    smallInd = bigInd = 0
    while smallInd < len(small) and bigInd < len(big):
        if small[smallInd] == big[bigInd]:
            smallInd += 1
            bigInd += 1
        else:
            bigInd += 1
    return smallInd == len(small)


if '__main__' == __name__:
    for sent in findSubsequences('my time has come'):
        print(sent)
