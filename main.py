import sys
import requests
from typing import List, Dict, Any

def fetch_price_data(url: str) -> Dict[str, Any]:
    """
    Fetch the latest price data for osrs items

    :param url: The URL to fetch price data from
    :return: A dictionary of the price data
    """
    
    try:
        response  = requests.get(url)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

def calculate_price_swings(data: Dict[str, any]) -> List:
    """
    Calculates the percentage difference between the high and low price of items

    :param data: A dictionary of the price data
    :return: A list of price swing data
    """
    
    price_swings = []
    for item_id, prices in data.items():
        # Skip items with zero or missing values
        if (prices.get('low', 0) in [0, None] or prices.get('high', 0) in [0, None]
                or 'high' not in prices or 'low' not in prices):
            continue

        low = prices['low']
        high = prices['high']

        # Calculate percentage difference
        percentage_diff = ((high - low) / low) * 100

        price_swings.append({
            'item_id': item_id,
            'low': low,
            'high': high,
            'percentage_diff': percentage_diff
        })

    # Sort price swings by highest
    price_swings.sort(key=lambda x: x['percentage_diff'], reverse=True)

    return price_swings

def display_top_price_swings(data: List, limit: int = 10) -> None:
    """
    Displays a formatted list of the top x price swings
        
    :param data: A list of price swing data
    :param limit: A number to limit the list to
    """
    
    for i, item in enumerate(data[:limit]):
        print(f"Item ID: {item['item_id']}, High: {item['high']}, Low: {item['low']}, Difference: {item['percentage_diff']:.2f}%")


def main():
    # Fetch price data
    price_data = fetch_price_data('https://prices.runescape.wiki/api/v1/osrs/latest')

    # Calculate price swings
    price_swings = calculate_price_swings(price_data)

    # Display 10 items with the highest price swings
    display_top_price_swings(price_swings)

if __name__ == "__main__":
    main()