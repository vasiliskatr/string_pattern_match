# # # # # # # # # # # # # # # # # # #
# Created by Vasileios Katranidis (v.katranidis@gmail.com)
# An open form solution to the string
# pattern matching problem. 
# Example: 
#        word = 'pricepricetag'
#        pattern = 'aab'
#       -----------------------
#  yields--> Pattern match!
#            'a'--> 'price'
#            'a'--> 'price'
#            'b'--> 'tag'
#
#
# To run in command line / terminal,
#   try for example: % python pattern_match.py match sunmoonsun aba 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


from collections import defaultdict
import itertools
import sys

def get_valid_chunks(word,pat):
    dict = defaultdict(set)
    # for 1st value in pattern:
    temp = []
    available_word_subset = word[0:0 + (len(word)-(len(pat)-1))]
    print('available word subset for: '+pat[0] +' -> '+ available_word_subset)
    for chuck_size in range(1, len(available_word_subset)+1):
        for subset in itertools.combinations(available_word_subset, chuck_size):
            subset = ''.join(subset)
            if subset in available_word_subset:
                # check that all subsets are tied to the first letter of the given word
                if subset[0]== available_word_subset[0]:
                    temp.append(subset)
                    dict[pat[0]].update(temp)
                    temp=[]
    if pat[-1]!=pat[0]:                
        # for last value in pattern - only if it is not the same as the 1st:
        temp = []
        available_word_subset = word[len(pat)-1:len(pat)-1 + (len(word)-(len(pat)-1))]
        print('available word subset for: '+pat[-1] +' -> '+ available_word_subset)
        for chuck_size in range(1, len(available_word_subset)+1):
            for subset in itertools.combinations(available_word_subset, chuck_size):
                subset = ''.join(subset)
                # check that the sampled subset exists in the given word
                if subset in available_word_subset:
                    # check that all subsets are tied to the last letter of the given word
                    if subset[-1]== available_word_subset[-1]:
                        temp.append(subset)
                        dict[pat[-1]].update(temp)
    # for the rest of the values in the pattern
    for j in range(1,len(pat)-1):
        temp=[]
        # do nothing for repeated characters in the given pattern
        if (pat[j]!=pat[0])&(pat[j]!=pat[-1]):
            if pat[j] in list(dict):
                continue
            available_word_subset = word[j:j + (len(word)-(len(pat)-1))]
            print('available word subset for: '+pat[j] +' -> '+ available_word_subset)
            for chuck_size in range(1, len(available_word_subset)+1):
                for subset in itertools.combinations(available_word_subset, chuck_size):
                    subset = ''.join(subset)
                    if subset in available_word_subset:
                        temp.append(subset)
            dict[pat[j]].update(temp)
 
    return dict

def comb(first, second, word, roots=None):
    if roots is None:
        combinations=[]
        roots=[]
        for ls in first:
            if ls not in word:
                continue
            print('fixed letter sequence = '+ ls)
            #print('number of fixed combinations= '+str(len(first)))
            #print(type(ls))
            temp = iter(second)
            print('     making iter -> ')
            while True:
                try:
                    t = next(temp)
                    if len(ls+t) <= len(word):
                        combinations.append(ls+t)
                        #print('*      '+ combinations[-1])
                        roots.append('+'.join([ls]+[t]))
                        #print('*           '+ ls +'+'+t)
                        print('*      '+ls +'+'+t+ ' = '+ combinations[-1])
                        print()
                except StopIteration:
                    break
        return combinations, roots
    else:
        combinations=[]
        roots_update=[]
        for ls,ro in zip(first,roots):
            if ls not in word:
                continue
            print('fixed letter sequence = '+ ls)
            #print('number of fixed combinations= '+str(len(first)))
            #print(type(ls))
            temp = iter(second)
            print('     making iter -> ')
            while True:
                try:
                    t = next(temp)
                    if len(ls+t) <= len(word):
                        combinations.append(ls+t)
                        #print('*      '+ combinations[-1])
                        roots_update.append('+'.join([ro]+[t]))
                        #print('*           '+ roots_update[-1] +'+'+t)
                        print('*      '+roots_update[-1]+ ' = '+ combinations[-1])
                        print()
                except StopIteration:
                    break
        return combinations, roots_update

def get_comb(dic, pat, word):
    fir = dic[pat[0]]
    sec = dic[pat[1]]
    res, roo = comb(fir, sec, word)
    if len(pat)>2:
        for i in range(2,len(pat)):
            print(pat[i])
            print(str(i)+'th iteration started - - - - - - - - - - - - - - - - - - - - - ')
            sec = dic[pat[i]]
            res, roo = comb(res, sec, word,roo)
    return res, roo


def pattern_duplicates(pat):
    dd = defaultdict(list)
    for i,item in enumerate(pat):
        dd[item].append(i)
    return (locs for locs in dd.values() if len(locs)>1)

def check(word,pat):
    if len(pat)==1:
        print('inevitably a match')
        return True
        
    if len(word)<len(pat):
        print('No match, word is shorter than the given pattern')
        return False
    
    if len(word)==len(set(pat)):
        print('inevitably a match')
        dictionary = get_valid_chunks(word, pat)
        print(dictionary)
        return True
    
    if len(word)==len(pat):
        print('No match!')
        dictionary = get_valid_chunks(word, pat)
        print(dictionary)
        return False

    if len(set(pat))==len(pat):
        dictionary = get_valid_chunks(word, pat)
        combinations ,roots = get_comb(dictionary,pat, word)
        print()
        print()
        print('Many valid patterns exist since all letters in pattern are unique')
        print('----------------------------------------------')
        for comb,root in zip(combinations,roots):

            if (len(comb) == len(word)) & (word in comb):
                for l in range(len(pat)):
                    print(pat[l]+' --> '+ root.split('+')[l])
                print(root + ' = '+ comb)
                print()
        return True
    
    # i.e. there are duplicate letters in the pattern
    elif len(set(pat))<len(pat):
        dictionary = get_valid_chunks(word, pat)
        combinations ,roots = get_comb(dictionary,pat, word)
        print()
        print()
        print('Candidates:')
        for comb,root in zip(combinations,roots):
            if (len(comb) == len(word)) & (word in comb):
                print('********')
                print(root)
                checklist=[]
                for dup in sorted(pattern_duplicates(pat)):
                    checklist.append(len(set([root.split('+')[x] for x in dup]))==1)
                if all(checklist):
                    print('Pattern match!')
                    print('----------------------------------------------')
                    for l in range(len(pat)):
                        print(pat[l]+' --> '+ root.split('+')[l])
                    print(root + ' = '+ comb)
                    
                    return True
                         
    print('Pattern did not match')
    return False    

def match(w,p):
    check(w,p)
  



if __name__ == '__main__':

    if sys.argv[1] == 'match':
            match(sys.argv[2], sys.argv[3])
  
    else:
        print()
        print("No strings given.")
        print('Try for example: % python pattern_match.py match blabla aa')