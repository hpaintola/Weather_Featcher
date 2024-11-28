import requests
import pandas as pd

API_KEY = '5a4ab8c47f756fcabc1393e3d55deb47'  
CITY = 'Delhi'  # City 
URL = f'https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}'

def fetch_weather_data():
    try:
        # Send the GET request to the API
        response = requests.get(URL)
        
        # Check if the response status code is OK (200)
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print("Message:", response.json())  # Show the error message from the API
            return
        
        # Parse the response JSON
        data = response.json()

        # Ensure the 'list' key exists in the response data
        if 'list' not in data:
            print("Error: 'list' key not found in the API response.")
            print(data)  # Show the full response for debugging
            return
        
        # Extract the Weather Data 
        weather_data = {
            "date": [item['dt_txt'] for item in data['list']],
            "temperature": [item['main']['temp'] - 273.15 for item in data['list']],  # Convert from Kelvin to Celsius
            "humidity": [item['main']['humidity'] for item in data['list']]
       }

        # Create a DataFrame and save it as a CSV file
        df = pd.DataFrame(weather_data)
        df.to_csv('weather_data.csv', index=False)
        print("Weather data saved to 'weather_data.csv'.")

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_weather_data()