import requests
import re
import sys
import os


'''


    This is a python file that will download all PDFs that
    are linked to by a provided URL. It can be run like this:

    python pdf_scraper.py <URL> <OPTIONAL DIRECTORY NAME>


    If a directory name is specified, it will create a directory
    with that name that branches off of the current directory.
    Otherwise, it will create a directory named 'pdf_download'
    that will contain all of the downloads.


    Dependencies:
        python requests library.


    Function synopsis:
        
        new_dir:
            Creates the given path and changes to that directory.
            Will just move to the directory if the path already exists.

        find:
            Finds all of the strings matching the given regular
            expression in the given text.  Works specifically with
            HTML in this context, but would work with any string.

        download:
            Downloads whatever lies at the given source URL
            with a pretty progress bar :)


    Made by:
        Oliver Hill <oliverhi@umich.edu>

        
'''



# Creates a new directory with the
# specified path and goes to that directory,
# attempting to handle exceptions along the way.
def new_dir(path):
    try:
        os.makedirs(path)
    except:
        pass

    # Go to the directory.
    os.chdir(path)



'''Returns a list of found matches for a regular
    expression in a file.

    Inputs:
        expr - a regular expression to search with.
        html - text to search.
'''
def find(expr, html):
        
    # Find all the instances of the
    # provided regular expression.
    found = re.findall(expr, html)
    result = []

    # Iterate over the found instances
    # and return the full paths from each.
    for tup in found:
        if tup[0] != '' and tup[1] != '':
            result.append(tup[0] + tup[1])

    return result




# Download the given PDF file with a status bar.
def download(source):
    print("Downloading: " + source + "...")    

    # Get the name of the file. O(n) :(
    path = source.split('/')
    dest = path[-1]

    # Get the response from the url request.
    response = requests.get(source, stream = True)
    length = response.headers.get('content-length')
    length = int(length)

    # Open the file and download whatever lies there.
    with open(dest, 'wb') as destination:
        progress = 0
        
        # Download the data.
        for data in response.iter_content(chunk_size = 10):
            progress += len(data) 
            destination.write(data)
            
            # Format a progress bar.
            done = int(50 * (progress / length))
            sys.stdout.write('\r[%s%s]' % ('#' * done, '-' * (50 - done)))
            sys.stdout.flush()

        print('\n')




# Main function!
if __name__ == '__main__':

    try:
        url = sys.argv[1]
        page = requests.get(url).text
    except:
        print("Error! Usage: 'python pdf_scraper.py <URL>' Exiting... \n\n\n")
        sys.exit()

    # Find all of the matches for a file path that ends with
    # a pdf file, relative or absolute.  Examples:
    #   https://eecs.umich.edu/handouts/lecture1.pdf
    #   handouts/umich/lecture1.pdf
    pdfs = find('"([0-9A-Za-z:/]*/)*(.*?.pdf)"', page)

    # Create a new directory branching off of the
    # current directory, name it with the URL,
    # and navigate to it so that we can download
    # all the files into this directory.
    if len(sys.argv) == 3:
        new_dir(os.getcwd() + '/' + sys.argv[2])
    else:
        new_dir(os.getcwd() + '/pdf_download')

    # Iterate over the results and download each PDF.
    for result in pdfs:

        # If the file path is a URL, download it
        # with a get request.
        if result[:5] == 'https':
            source = result
        
        # Otherwise append the result onto the
        # base URL given when the program started.
        else:
            source = url + result

        download(source)
        
