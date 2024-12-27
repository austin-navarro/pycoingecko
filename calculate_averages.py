import json
import os
from pathlib import Path
import glob

def load_latest_json(pattern):
    # Get list of all matching files
    files = glob.glob(f'data/{pattern}*.json')
    if not files:
        return None
    
    # Sort by modification time and get the latest
    latest_file = max(files, key=os.path.getmtime)
    
    with open(latest_file, 'r') as f:
        return json.load(f)

def calculate_average(prices_data):
    # Extract all prices
    prices = [entry['price_usd'] for entry in prices_data]
    
    # Calculate sum and count
    total_sum = sum(prices)
    count = len(prices)
    
    # Calculate average
    average = total_sum / count if count > 0 else 0
    
    return {
        'prices': prices,
        'sum': total_sum,
        'count': count,
        'average': average,
        'calculation': f"Sum of all prices (${total_sum:.2f}) ÷ Number of days ({count}) = ${average:.2f}"
    }

def main():
    # Load the latest JSON files
    bnb_data = load_latest_json('bnb_daily_prices')
    eth_data = load_latest_json('eth_daily_prices')
    id_data = load_latest_json('id_daily_prices')
    
    if not all([bnb_data, eth_data, id_data]):
        print("Error: Could not find all required JSON files in data directory")
        return
    
    # Calculate averages
    bnb_analysis = calculate_average(bnb_data)
    eth_analysis = calculate_average(eth_data)
    id_analysis = calculate_average(id_data)
    
    # Create result object
    result = {
        'time_period': {
            'start_date': bnb_data[0]['date'],
            'end_date': bnb_data[-1]['date'],
            'total_days': len(bnb_data)
        },
        'bnb_analysis': {
            'detailed_math': {
                'total_sum': bnb_analysis['sum'],
                'number_of_days': bnb_analysis['count'],
                'calculation': bnb_analysis['calculation']
            },
            'final_average_price': bnb_analysis['average']
        },
        'eth_analysis': {
            'detailed_math': {
                'total_sum': eth_analysis['sum'],
                'number_of_days': eth_analysis['count'],
                'calculation': eth_analysis['calculation']
            },
            'final_average_price': eth_analysis['average']
        },
        'id_analysis': {
            'detailed_math': {
                'total_sum': id_analysis['sum'],
                'number_of_days': id_analysis['count'],
                'calculation': id_analysis['calculation']
            },
            'final_average_price': id_analysis['average']
        }
    }
    
    # Save results
    output_file = 'data/price_averages_analysis.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)
    
    print(f"\nAnalysis Results:")
    print(f"Time Period: {result['time_period']['start_date']} to {result['time_period']['end_date']}")
    print(f"\nBNB Average Price: ${result['bnb_analysis']['final_average_price']:.2f}")
    print(f"ETH Average Price: ${result['eth_analysis']['final_average_price']:.2f}")
    print(f"ID Average Price: ${result['id_analysis']['final_average_price']:.2f}")
    print(f"\nDetailed calculations have been saved to: {output_file}")

if __name__ == "__main__":
    main() 