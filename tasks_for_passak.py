tasks = {
# LEETCODE:
    "number of words in string": [["Two words", "we re qw", ""],[2,3,0]],
    "is string is palindrome": [["palindrome", "qwertytrewq", "ef33fe"],[False, True, True]],
    "Roman to integer": [["XI", "V", "III"], [11,5,3]],
    "merge two sorted list": [[[[1, 2, 4], [1, 3, 4]], [[], []], [[], [0]]], [[1,1,2,3,4,4], [], [0]]],
    "Length of Last Word": [["Hello World","   fly me   to   the moon  ", "luffy is still joyboy"],[5,4,6]],
    "Remove Duplicates from Sorted List": [[[1,1,2],[1,1,2,3,3],[1,1,5,6,7]],[[1,2],[1,2,3],[1,5,6,7]]],
    "sum of two numbers": [[[1,2],[5,55],[12,14]],[3,60,26]],
    "find a single number in list": [[[2,2,1],[4,1,2,1,2],[1]],[1,4,1]],
    "Reverse Integer":[[123,-123,120],[321,-321,21]],       #med
    "String to integer":[["42","   -42","4193"],[42, -42, 4193]], #med
    "calculate x raised to the power n": [[[2,10],[2,3],[2,-2]],[1024,8,0.25]],
    "Increment integer": [[3,5,1],[4,6,2]],
    "Given a positive integer n, generate an n x n matrix filled with elements from 1 to n2 in spiral order": [[3,1,2],[[[1,2,3],[8,9,4],[7,6,5]],[[1]],[[1,2],[4,3]]]],
    "Given a string s containing only digits, return all possible valid IP addresses that can be formed by inserting dots into s": [["0000","255255255255","25525500"],["0.0.0.0","255.255.255.255","255.255.0.0"]],
    "Reverse Words in a String": [["the sky is blue","  hello world  ", "a good   example"],["blue is sky the","world hello","example good a"]],
    "Smallest number in the list": [[[2,3,1],[8,9,7,5],[10,54,2,56]],[1,5,2]],
    "calculate the factorial of a number": [[3,5,7],[6,120,5040]],
    "Sum of the first n fibonacci numbers": [[3,10,5],[2, 88, 7]],
    "damerau-levenshtein distance":[[["XABCDE","ACBYDF"],["OK","STOK"],["PARTY","PARK"]],[4,2,2]],
    "String To Lower Case": [["Hello","here","LOVELY"],["hello","here","lovely"]],
#HumanEval:
    "Return a string containing space-delimited numbers starting from 0 upto n inclusive":[[0,3,10],['0','0 1 2 3', '0 1 2 3 4 5 6 7 8 9 10']], #HumanEval/15
    "Given a string, find out how many distinct characters (regardless of case) does it consist of":[['','aaaaAAAAaaaa aaaaAAAAaaaa','xyzXYZaaaaAAAAaaaa'],[0,2,4]], ##HumanEval/16
    "Return a greatest common divisor of two integers a and b":[[[3,7],[49,14],[144,60]],[1,7,12]], #HumanEval/13
    "Out of list of strings, return the longest one. Return the first one in case of multiple strings of the same length. Return None in case the input list is empty.":[[['x', 'y', 'z'],['x', 'yyy', 'zzzz'],[]],['x','zzzz',None]],#HumanEval/12
    "Input are two strings a and b consisting only of 1s and 0s. Perform binary XOR on these inputs and return result also as a string":[[['111000','101010'],['1','1'],['0101', '0000']],['010010','0','0101']],#HumanEval/11
    "From a given list of integers, generate a list of rolling maximum element found until given moment in the sequence":[[[1, 2, 3, 4],[4, 3, 2, 1],[3, 2, 3, 100, 3]],[[1, 2, 3, 4],[4, 4, 4, 4],[3, 3, 3, 100, 100]]], #HumanEval/9
    "Write a function vowels_count which takes a string representing a word as input and returns the number of vowels in the string":[["IU5","is","lifestyle"],[2,1,4]],#HumanEval/64
    "Concatenate list of strings into a single string": [[["x","y", "z"],["x", "y", "z", "w", "k"],["iu","5"]],["xyz", "xyzwk","iu5"]], #HumanEval/28
    "Return only positive numbers in the list": [[[-1, -2, 4, 5, 6],[5, 3, -5, 2, 3, 3, 9, 0, 123, 1, -10],[-1,-2,-5,7]],[[4, 5, 6],[5, 3, 2, 3, 3, 9, 123, 1],[7]]], #HumanEval/30
    "Return true if a given number is prime, and false otherwise": [[6,11,13441],[False, True, True]], #HumanEval/31
    "Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13": [[50, 70, 4000],[0,2,192]], #HumanEval/36
    "Function takes a list of integers as an input. it returns True if there are three distinct elements in the list that sum to zero, and False otherwise": [[[1, 3, 5, 0], [1, 3, -2, 1], [1, 2, 3, 7]],[False,True, False]], #HumanEval/40
}
