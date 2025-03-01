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

def fetch_mapping_data(url: str) -> List[Dict[str, Any]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

def calculate_alch_margins(price_data: Dict[str, Any], mapping_data: List[Dict[str, Any]]) -> List:
    alch_margins = []
    for item in mapping_data:
        if ('highalch' in item and 'value' in item and 'id' in item
                and item['value'] != 0) and str(item['id']) in price_data:
            price_item = price_data[str(item['id'])]
            if "high" in price_item:
                high_price = price_item['high']
                alch_margin = item['highalch'] - high_price

                alch_margins.append({
                    'item_id': item['id'],
                    'name': item['name'],
                    'high_alch': item['highalch'],
                    'buy_price': high_price,
                    'alch_margin': alch_margin
                })

    # Sort alch margins by highest
    alch_margins.sort(key=lambda x: x['alch_margin'], reverse=True)

    return alch_margins

def display_top_alch_margins(data: List, limit: int = 10) -> None:
    """
    Displays a formatted list of the top x price swings

    :param data: A list of price swing data
    :param limit: A number to limit the list to
    """

    for i, item in enumerate(data[:limit]):
        print(f"Item ID: {item['item_id']}, Name: {item['name']}, High Alch: {item['high_alch']}, Buy Price: {item['buy_price']}, Margin: {item['alch_margin']}")

def main():
    # Fetch price and mapping data
    price_data = fetch_price_data('https://prices.runescape.wiki/api/v1/osrs/latest')
    mapping_data = fetch_mapping_data('https://prices.runescape.wiki/api/v1/osrs/mapping')

    # Calculate items with the best alch margins
    alch_margins = calculate_alch_margins(price_data, mapping_data)

    # Display top alch margins
    display_top_alch_margins(alch_margins)

if __name__ == "__main__":
    main()