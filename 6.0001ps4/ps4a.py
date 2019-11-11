# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    
    
    #Base case： if sequence is a single character
    if len(sequence) == 1:
        #return a singleton list containing sequence
        return [sequence]
    #Recursive case:
    else:
        permutation = []
        #recursive call to reduce sequence into base case
        first_char = sequence[0]
        remaining_char = sequence[1:]
        permutation_subsequence = get_permutations(remaining_char)
        #permutations of all characters in sequence would be all the different ways we can insert 
        #the first character into each permutation of the remaining characters
        for subpermutation in permutation_subsequence:
            for index in range (len(remaining_char)+1):
                arrangement = subpermutation[0:index] + first_char + subpermutation[index:len(subpermutation)]
                #extend() and concatenation iterates over its argument and add each element in the argument
                #separately to the list 
                #append() add its argument as a single element
                permutation.append(arrangement)
        return permutation

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    print(get_permutations('ab'))
    print(get_permutations('abc'))
    print(get_permutations('bust'))
