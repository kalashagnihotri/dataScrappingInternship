# Amazon Product Scraper

This project is a web scraper for Amazon products using Selenium and BeautifulSoup. It extracts product details such as name, price, rating, and seller information and saves them to a CSV file.

## Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver
- Required Python packages (install using `pip`)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/amazon-product-scraper.git
    cd amazon-product-scraper
    ```

2. Install the required Python packages:
    ```sh
    pip install selenium beautifulsoup4
    ```

3. Set the `CHROMEDRIVER_PATH` environment variable to the path of your ChromeDriver executable:
    ```sh
    set CHROMEDRIVER_PATH=C:\path\to\your\chromedriver.exe
    ```

## Usage

1. Run the scraper:
    ```sh
    python main.py
    ```

2. The scraped data will be saved to `amazon_products.csv`.

## Project Structure
