##########################################################################
# Example usage:
#           make_data_set("science fiction", "/tmp/sci-fi-books.csv")
#           make_data_set("Astronomy", "/tmp/astronomy-books.csv")
##########################################################################


import requests
import urllib.parse
import json
import csv
import os
import time
import argparse

def create_csv_file(filename):
    """
    Creates a new CSV file with the specified filename and writes the header row.
    """
    fieldnames = ["id", "title", "author", "text"]
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def append_to_csv(filename, record):
    """
    Appends a new line (record) to an existing CSV file.
    The record should be a dictionary with keys: "id", "title", "author", and "text".
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"CSV file '{filename}' does not exist.")

    with open(filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=record.keys())
        writer.writerow(record)

def getPageData(url):
    """ parse the json data at the given url api endpoint """
    #print(f"Debug: at get page data {url}")
    response = requests.get(url)
    paresd_books = json.loads(response.content)
    # Pretty-print the parsed data
    pretty_json = json.dumps(paresd_books, indent=4)
    #print(pretty_json)
    return paresd_books

def concat_strings(*args):
    """
    Concatenates a list of strings into a single string.
    # Example usage:
    result = concat_strings("i ", "love ", "common ", "lisp")
    """
    return "".join(args)

def compile_list_of_pages(query):
    """ Compile a list of pages containing books for a topic """
    pages = []
    count = 0
    query = urllib.parse.quote_plus(query, encoding='utf-8')
    url = concat_strings("https://gutendex.com/books/?topic=", query)
    print(f"\rProcessing first page: {url}", end="")
    pages.append(url)
    count = count + 1
    response = requests.get(url)
    parsed_books = json.loads(response.content)
    nexturl = parsed_books.get("next")
    count = count + 1
    print(f"\rProcessing next page: {nexturl}",  end="")
    while nexturl:
        pages.append(nexturl)
        count = count + 1
        response = requests.get(nexturl)
        parsed_books = json.loads(response.content)
        nexturl = parsed_books.get("next")
        print(f"\rProcessing Page: {count} <==> Debug page url: {nexturl} ", end="")
    print(f"Total Pages = {count}")
    return pages

def make_data_set (query, csv_filename):
    """
    This function creates a dataset of books based on a given query and saves it to a CSV file.

    The function first creates a CSV file with the given filename. It then compiles a list of pages containing books for the given query. For each page, it retrieves the data, processes each book in the results, and appends a record for the book to the CSV file. The function prints updates to the console as it processes each page and book.

    Parameters:
    query (str): The query for the books.
    csv_filename (str): The name of the CSV file to save the dataset to.

    Returns:
    None

    Note:
    This function makes requests to an external website to retrieve book data. To avoid making too many requests in a short period of time, it includes a delay of 3 seconds after processing each book.
    """
    create_csv_file(csv_filename)
    print("Collating pages")
    all_page_urls = []
    all_page_urls.extend(compile_list_of_pages(query))
    print("Collecting data")
    count = 0
    for i in all_page_urls:
        print(f"\nProcessing page: {count}")
        count = count + 1
        jsonlist = getPageData(i)
        for j in jsonlist["results"]:
            try:
                print(f"\rID: {j['id']} | Title: {j['title']} | Author: {j['authors'][0]['name']}", end="")
                x = requests.get(j['formats']['text/plain; charset=us-ascii'])
                book_record = {
                    "id": {j['id']},
                    "title": {j['title']},
                    "author": {j['authors'][0]['name']},
                    "text": x.content
                }
                append_to_csv(csv_filename, book_record)
                time.sleep(3)  # Let's not overload the website with lots of requests per minute
            except Exception as e:
                print(f"\nAn error occurred while processing book ID: {j['id']}. Error: {str(e)} \nThis sometimes happens when there is no plaintext version available")


##############



# Create the parser
parser = argparse.ArgumentParser(description="Collects data about books from the Gutendex API and saves it to a CSV file.")

# Add the arguments
parser.add_argument("query", metavar="query", type=str, help="The query for the books.")
parser.add_argument("csv_filename", metavar="csv_filename", type=str, help="The name of the CSV file to save the dataset to.")

# Parse the arguments
args = parser.parse_args()

# Check if both arguments are provided
if not args.query or not args.csv_filename:
    parser.print_help()
else:
    # Call the function with the provided arguments
    make_data_set(args.query, args.csv_filename)


