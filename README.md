# Centres Scrapping

This project scrapes data from the Algolia API and saves it into a CSV file.

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/david_scrapping.git
   cd david_scrapping
   ```

2. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `.\venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `example.env` file:
   ```sh
   cp .env.example .env
   ```

5. Update the `.env` file with your Algolia API credentials:
   ```plaintext
   ALGOLIA_APP_ID=your_algolia_app_id
   ALGOLIA_API_KEY=your_algolia_api_key
   INDEX_NAME=your_index_name
   ```

## Usage

To run the scrapper and save the data to a CSV file, execute the following command:
```sh
python scrapper_csv.py
```

To run the Algolia scraper and save the data to a JSON file, execute the following command:
```sh
python scraper_algolia.py
```

## Files

- `scrapper_csv.py`: Script to fetch data from Algolia and save it to a CSV file.
- `scraper_algolia.py`: Script to fetch data from Algolia and save it to a JSON file.
- `requirements.txt`: List of dependencies required for the project.
- `.env`: Environment variables for the project (not included in the repository).
- `.env.example`: Example environment variables file.
- `.gitignore`: Specifies files and directories to be ignored by Git.
