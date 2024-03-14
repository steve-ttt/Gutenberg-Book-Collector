# Gutenberg Book Collector

This Python script collects and creates a dataset of books from the Gutendex API based on a provided "topic" query, and saves it to a CSV file for the purpose of using the dataset to train AI Large Language Models (LLM). 

## Functions

- `create_csv_file(filename)`: Creates a new CSV file with the specified filename and writes the header row.
- `append_to_csv(filename, record)`: Appends a new line (record) to an existing CSV file. The record should be a dictionary with keys: "id", "title", "author", and "text".
- `getPageData(url)`: Parses the JSON data at the given URL API endpoint.
- `concat_strings(*args)`: Concatenates a list of strings into a single string.
- `compile_list_of_pages(query)`: Compiles a list of pages containing books for a topic.
- `make_data_set(query, csv_filename)`: This function creates a dataset of books based on a given query and saves it to a CSV file. The function first creates a CSV file with the given filename. It then compiles a list of pages containing books for the given query. For each page, it retrieves the data, processes each book in the results, and appends a record for the book to the CSV file. The function prints updates to the console as it processes each page and book.

## Usage

Run from the command line with: python ./gutenberg.py "astronomy" /path/to/astronomy-books.csv

Or you can run in the python repl with:

1. Import the necessary modules: `requests`, `urllib.parse`, `json`, `csv`, `os`, and `time`.
2. Call `create_csv_file(filename)` to create a new CSV file.
3. Call `make_data_set(query, csv_filename)` to create a dataset of books based on a given query and save it to a CSV file.

## Note

This script makes requests to an external website to retrieve book data. To avoid making too many requests in a short period of time, it includes a delay of 3 seconds after processing each book.
