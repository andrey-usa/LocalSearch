"""
File: extension_server.py
---------------------
This starts a server! Go to http://localhost:8000 to enjoy it. Currently
the server only serves up the HTML. It does not search. Implement code in
the "TODO" parts of this file to make it work.
"""
import re

# This imports the SimpleServer library
import SimpleServer

# This imports the functions you defined in searchengine.py
from searchengine import create_index, search, textfiles_in_dir

# To get the json.dumps function.
import os
import json

CWD = os.getcwd()
# the directory of files to search over
DIRECTORY = 'bbcnews'
# perhaps you want to limit to only 10 responses per search.
MAX_RESPONSES_PER_REQUEST = 10


class SearchServer:
    def __init__(self):

        """
        load the data that we need to run the search engine. This happens
        once when the server is first created.
        """
        self.files = textfiles_in_dir(DIRECTORY)
        self.index = {}  # index is empty to start
        self.file_titles = {}  # mapping of file names to article titles is empty to start
        create_index(self.files, self.index, self.file_titles)

        self.html = open('extension_client.html').read()

        # TODO: Your code here. Change this code to load any data you want to use!

    # this is the server request callback function. You can't change its name or params!!!

    # def extract_sentences(self, text, term):
    #     sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)  # Split text into sentences
    #     matched_sentences = []
    #     count = 0
    #     for sentence in sentences:
    #         if term.lower() in sentence.lower():
    #             matched_sentences.append(sentence)
    #             count += 1
    #         if count >= 3:  # Limit to three sentences
    #             break
    #     return matched_sentences

    def extract_sentences(self, text, term):
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)  # Split text into sentences
        matched_sentences = []
        count = 0

        for i in range(len(sentences)):
            if term.lower() in sentences[i].lower():
                # Add the previous sentence if it exists
                if i > 0:
                    matched_sentences.append(sentences[i - 1])

                # Add the sentence with the term
                matched_sentences.append(sentences[i])

                # Add the next sentence if it exists
                if i < len(sentences) - 1:
                    matched_sentences.append(sentences[i + 1])

                count += 1

            if count >= 3:  # Limit to three sentences
                break

        return matched_sentences

    def handle_request(self, request):
        """
        This function gets called every time someone makes a request to our
        server. To handle a search, look for the query parameter with key "query"
        """
        # it is helpful to print out each request you receive!
        print(request)

        # if the command is empty, return the html for the search page
        if request.command == '':
            return self.html

        # if the command is search, the client wants you to perform a search!
        if request.command == 'search':
            params = request.get_params()
            query = params['query'].lower()

            files = search(self.index, query)

            results = []
            for file in files:
                with open(file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    sentences = self.extract_sentences(file_content, query)
                    snippet = ' '.join(sentences) if sentences else ''  # Join matched sentences into a snippet
                    result = {'title': self.file_titles[file], 'url': 'file?path=' + file, 'snippet': snippet}
                    results.append(result)
                # of a list of dicts. Use json.dumps(collection) to turn a list into a string
            results_str = json.dumps(results)
            #print("str_return_list=", results_str)
            return results_str

        if request.command == 'file':
            params = request.get_params()
            print(params)
            file = params['path'].lower()
            print(file)
            with open(file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            return file_content


def main():
    # Make an instance of your Server
    handler = SearchServer()

    # Start the server to handle internet requests at http://localhost:8000
    SimpleServer.run_server(handler, 8000)


if __name__ == '__main__':
    main()
