# Book Scraper

This project is a Python web scraper that extracts book data from the website [Books to Scrape](https://books.toscrape.com/catalogue/category/books_1/index.html). The script collects information such as book titles, prices, ratings, and availability for further analysis or use in other projects.

## Features

- Extracts book titles, prices, ratings, and stock availability from the website.
- Makes use of `BeautifulSoup` for HTML parsing and `requests` for web requests.
- Outputs the extracted data in a structured format.

## Getting Started

### Prerequisites

Before you start, ensure you have Python 3.x installed on your machine. You can download the latest version of Python [here](https://www.python.org/downloads/).

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/book-scraper.git
    cd book-scraper
    ```

2. **Create a virtual environment**:

    It is recommended to create a virtual environment to manage dependencies. Run the following commands to create and activate a virtual environment:

    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3. **Install dependencies**:

    Install the required Python packages using `pip`:

    ```bash
    pip install beautifulsoup4 requests
    ```

### Usage

Once you have the environment set up and dependencies installed, you can run the scraper by executing the following command:

```bash
python scraping.py
