import unittest
from SubsequenceEnumerator.Solver import findSubsequences, findIndicesOfStartsWithEndsWith, isSubsequence

class TestFindSubsequences(unittest.TestCase):
    def testSimple(self):
        simpleWordList = ['a', 'aa', 'ab', 'ace', 'ae', 'be', 'bed', 'de']
        simpleInput = 'abcde'
        expected = [
            'ab de',
            'ace',
            'a de',
            'ab',
            'ae',
            'be',
            'de',
            'a'
        ]
        observed = findSubsequences(simpleInput, simpleWordList)
        self.assertEqual(expected, observed)

    def testSingle(self):
        wordList = ['be']
        expected = ['be']
        observed = findSubsequences('be', wordList)
        self.assertEqual(expected, observed)
        observed = findSubsequences('bce', wordList)
        self.assertEqual(expected, observed)
        observed = findSubsequences('bcce', wordList)
        self.assertEqual(expected, observed)
        observed = findSubsequences('bccce', wordList)
        self.assertEqual(expected, observed)


class TestIsSubsequence(unittest.TestCase):
    def testNonemptyOfEmpty(self):
        self.assertFalse(isSubsequence('a',''))

    def testEmptyOfNonempty(self):
        self.assertTrue(isSubsequence('','a'))

    def testEmptyOfEmpty(self):
        self.assertTrue(isSubsequence('',''))

    def testBigOfSmall(self):
        self.assertFalse(isSubsequence('abcd', 'abc'))

    def testTrueNotEnds(self):
        self.assertTrue(isSubsequence('happy', 'some happi-nessy was here'))

    def testTrueEnds(self):
        self.assertTrue(isSubsequence('aa', 'abba'))

    def testFalseNoRepeats(self):
        self.assertFalse(isSubsequence('house', 'houes'))

    def testFalseRepeats(self):
        self.assertFalse(isSubsequence('abba', 'abcdef'))

class TestIndexFinder(unittest.TestCase):
    simpleWordList = [
        'a',
        'aa',
        'ab',
        'ae',
        'ace',
        'bed',
        'be',
        'de',
    ]

    def testPresent(self):
        target = 'be'
        expected = (6, 6)
        observed = findIndicesOfStartsWithEndsWith(target, self.simpleWordList)
        self.assertEqual(expected, observed)

    def testAbsent(self):
        target = 'bb'
        expected = (-1, -1)
        observed = findIndicesOfStartsWithEndsWith(target, self.simpleWordList)
        self.assertEqual(expected, observed)

    def testFirst(self):
        target = 'aa'
        expected = (0, 1)
        observed = findIndicesOfStartsWithEndsWith(target, self.simpleWordList)
        self.assertEqual(expected, observed)

    def testLast(self):
        target = 'de'
        expected = (7, 7)
        observed = findIndicesOfStartsWithEndsWith(target, self.simpleWordList)
        self.assertEqual(expected, observed)

    def testSingleDict(self):
        target = 'bc'
        expected = (-1, -1)
        observed = findIndicesOfStartsWithEndsWith(target, ['be'])
        self.assertEqual(expected, observed)


if '__main__' == __name__:
    unittest.main()
