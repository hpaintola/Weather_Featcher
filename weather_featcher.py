import requests
import pandas as pd
import json
from custom_logger import setup_logger

class WeatherFetcher:
    def __init__(self, config_file, log_file='weather_app.log'):
        self.config_file = config_file
        self.logger = setup_logger('WeatherFetcher', log_file)
        self.config = self.load_config()
        self.api_key = self.config.get('api_key')
        self.base_url = self.config.get('base_url')
        self.city = self.get_city_choice()
        self.url = f"{self.base_url}?q={self.city}&appid={self.api_key}"

    def load_config(self):
        """Load configuration from a JSON file."""
        try:
            with open(self.config_file, 'r') as file:
                self.logger.info("Configuration file loaded successfully.")
                return json.load(file)
        except FileNotFoundError:
            self.logger.error(f"Configuration file {self.config_file} not found.")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON file: {e}")
            raise

    def get_city_choice(self):
        """Allow the user to choose a city from the list."""
        try:
            cities = self.config.get('cities', [])
            if not cities:
                self.logger.error("No cities found in configuration.")
                raise ValueError("City list is empty in the configuration file.")
            
            print("Available cities:")
            for idx, city in enumerate(cities, start=1):
                print(f"{idx}. {city}")
            
            choice = int(input("Enter the number of the city you want to select: "))
            if 1 <= choice <= len(cities):
                self.logger.info(f"City selected: {cities[choice - 1]}")
                return cities[choice - 1]
            else:
                self.logger.error("Invalid choice. Please select a valid city number.")
                raise ValueError("Invalid city choice.")
        except ValueError as e:
            self.logger.error(f"Error in city selection: {e}")
            raise

    def fetch_data(self):
        """Fetch weather data from the API."""
        try:
            self.logger.info(f"Fetching weather data for {self.city}.")
            response = requests.get(self.url)
            if response.status_code != 200:
                self.logger.error(f"Error: Received status code {response.status_code}.")
                self.logger.error(f"Message: {response.json()}")
                return None
            self.logger.info("Weather data fetched successfully.")
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Request error: {e}")
            raise

    def process_data(self, data):
        """Process the weather data into a DataFrame."""
        try:
            if 'list' not in data:
                self.logger.error("'list' key not found in the API response.")
                self.logger.error(f"Response: {data}")
                return None
            weather_data = {
                "date": [item['dt_txt'] for item in data['list']],
                "temperature": [item['main']['temp'] - 273.15 for item in data['list']],
                "humidity": [item['main']['humidity'] for item in data['list']]
            }
            self.logger.info("Weather data processed successfully.")
            return pd.DataFrame(weather_data)
        except KeyError as e:
            self.logger.error(f"Key error while processing data: {e}")
            raise

    def save_to_csv(self, df, file_name='weather_data.csv'):
        """Save the DataFrame to a CSV file."""
        try:
            df.to_csv(file_name, index=False)
            self.logger.info(f"Weather data saved to {file_name}.")
        except Exception as e:
            self.logger.error(f"Error saving data to CSV: {e}")
            raise

    def run(self):
        """Run the entire workflow."""
        try:
            data = self.fetch_data()
            if data:
                df = self.process_data(data)
                if df is not None:
                    self.save_to_csv(df)
        except Exception as e:
            self.logger.error(f"An error occurred during execution: {e}")
            raise


if __name__ == "__main__":
    # Update the path to your configuration file as needed
    weather_fetcher = WeatherFetcher(config_file='config.json')
    weather_fetcher.run()
