import requests
import json
from datetime import datetime, date
import os
from dotenv import load_dotenv
import time
from pathlib import Path

# Load environment variables
load_dotenv()

def get_daily_prices(contract_address, start_date, vs_currency='usd'):
    # Calculate days from start date until now
    start_timestamp = datetime.strptime(start_date, '%Y-%m-%d').date()
    days = (date.today() - start_timestamp).days

    # Get API key and URL from environment variables
    api_key = os.getenv('COINGECKO_API_KEY')
    base_url = os.getenv('COINGECKO_API_URL')
    
    url = f'{base_url}/coins/ethereum/contract/{contract_address}/market_chart'
    
    headers = {
        'x-cg-api-key': api_key
    }
    
    params = {
        'vs_currency': vs_currency,
        'days': days,
        'interval': 'daily'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        # Process the daily prices
        daily_prices = []
        for timestamp_ms, price in data['prices']:
            # Convert timestamp from milliseconds to datetime
            day = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d')
            daily_prices.append({
                'date': day,
                'price_usd': price
            })
        
        return daily_prices
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_json(data, filename):
    # Create 'data' directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    # Save to data directory
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Data saved to {filepath}")

def main():
    # ID token contract address
    contract_address = '0x2dff88a56767223a5529ea5960da7a3f5f766406'
    start_date = '2024-03-01'
    
    print(f"Fetching daily ID token prices from {start_date} to today...")
    daily_prices = get_daily_prices(contract_address, start_date)
    
    if daily_prices:
        # Generate filename with current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'id_daily_prices_{timestamp}.json'
        
        # Save the data
        save_to_json(daily_prices, filename)
        
        # Print summary
        print(f"\nSummary:")
        print(f"Total days: {len(daily_prices)}")
        print(f"First day price: ${daily_prices[0]['price_usd']:.2f}")
        print(f"Latest day price: ${daily_prices[-1]['price_usd']:.2f}")

if __name__ == "__main__":
    main() 