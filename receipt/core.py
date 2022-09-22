import typing

def getDelimitersIndex(size :int, word :str, delimiterSet :set[str], delimiterIndexArray :list[any]) ->None:
    '''
    finds the start and end index of each delimeter in the word and adds it to the array

    Params:
    size (int): size of the delimiter to lookout for
    word (str): word to search from
    delimiterSet (set[str]): a set containing the delimiters
    delimiterIndexArray (list[any]): empty output array passed by reference. To contain list of start and end index
    
    Returns:
    None
    '''
    i, j = 0, size-1
    length = len(word)

    while j < length:
        delim = word[i:j+1]
        if delim in delimiterSet:
            delimiterIndexArray.append([i, j])
        i += 1
        j += 1


def mergeDelimiterIndexArray(delimiterIndexArray :list[list[int,int]]) ->list[list[int,int]]:
    '''
    This function combines the indices of delimiters that overlap

    Params:
    delimiterIndexArray (list[list[int,int]]): an array of pairs signifiying start and end positions.
    
    Returns: 
    (list[list[int,int]]): An array of merged delimiter indices
    '''

    delimiterIndexArray.sort(key=lambda x: x[1])

    mergedDelimiterIndexArray = [delimiterIndexArray[0]]

    for i in range(1, len(delimiterIndexArray)):
        prev = mergedDelimiterIndexArray[-1]
        val = delimiterIndexArray[i]
        if val[0] <= prev[1]:
            mergedDelimiterIndexArray[-1][0] = min(mergedDelimiterIndexArray[-1][0], val[0])
            mergedDelimiterIndexArray[-1][1] = max(mergedDelimiterIndexArray[-1][1], val[1])
        else:
            mergedDelimiterIndexArray.append(val)
    return mergedDelimiterIndexArray


def GetSubstrings(word: str, delimiterSet: set[str], shortest_delim :int, longest_delim :int) ->list[list[int, int]]:
    '''
    Traverses the word to find the start and end indices of the words separated
    by the delimiters in the delimiter set.

    Param:
    word (str): The string to be traversed
    delimiterSet(set[str]): A set object containing the delimiters
    shortest_delim (int): length of the shortest delimiter
    longest_delim (int): length of the longest delimiter

    Returns:
    list[list[int,int]]: A 2D array conaining the start and end indices of the words separated by the delimiters
    '''
    delimiterArray = []
    finalOutput = []

    # find the index of all delimiters of all sizes
    for i in range(shortest_delim, longest_delim+1):
        getDelimitersIndex(i, word, delimiterSet, delimiterArray)

    ## if delimiter is found
    if len(delimiterArray) !=0 :
        delimiterArray = mergeDelimiterIndexArray(delimiterArray)

        # find index of words before the first delimiter
        start_index = 0
        end_index = delimiterArray[0][0]-1

        while start_index < len(word) and word[start_index].isspace():
            start_index += 1
        while end_index > start_index and word[end_index].isspace():
            end_index -= 1

        if start_index < end_index:
            finalOutput.append([start_index, end_index])

        ## find index of words between delimiters
        n = len(delimiterArray)
        for i in range(1, n):
            start_index = delimiterArray[i-1][1]+1
            end_index = delimiterArray[i][0]-1

            while start_index < len(word) and word[start_index].isspace():
                start_index += 1

            while end_index > start_index and word[end_index].isspace():
                end_index -= 1
            finalOutput.append([start_index, end_index])

        ## find index of trailing words after the last delimiter
        start_index = delimiterArray[-1][1]+1
        end_index = len(word)-1
        while start_index < len(word) and word[start_index].isspace():
            start_index += 1
        while end_index > start_index and word[end_index].isspace():
            end_index -= 1
        if start_index < end_index:
            finalOutput.append([start_index, end_index])

        return finalOutput
    else:
        # word doesn't contain delimiter
        start_index = 0
        end_index = len(word)-1

        while start_index < len(word) and word[start_index].isspace():
            start_index += 1
        while end_index > start_index and word[end_index].isspace():
            end_index -= 1

        if start_index < end_index:
            return [[start_index, end_index]]
