"""
Provides the function that processes each line of a given Wikipedia page traffic file
Provides a function to reshape a file (that is already split into lines) to a DataFrame
"""

def process_line(line, line_number):
    """
    Processes each line into language-type | article | visits | traffic
    Can handle the most common errors in the data (missing article name, articles names with spaces in them)
    Takes the line_number as input so it can be returned for error tracking
    """
    out = line.split()
    if len(out) == 3:
        # this is for lines that don't have an article name
        out = [out[0], 'blank', out[1], out[2]]
    elif len(out) > 4:
        # this is for lines that split into more than 4 elements
        # because the article name has additional spaces for whatever reason
        # since I don't actually care about the article name, part of it will do
        out = [out[0], out[1], out[-2], out[-1]]
    # check if out has the right length now
    if len(out) != 4:
        print(line_number)
        # raise TooShortError('The line does not have the right length after processing. It is too short. Line: '+ str(line_number))
    # make sure all variables have the right type
    out[2], out[3] = int(out[2]), int(out[3])
    # check that the elements of out are all of the correct type
    if not [type(i) for i in out] == [str, str, int, int]:
        print(line_number)
        print(line)
        print([type(i) for i in out])
        # raise TypeError('The line does not have the right variable types after processing. Line: '+ str(line_number))
    return out



