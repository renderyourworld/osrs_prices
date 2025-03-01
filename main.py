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
    """
    Fetch the latest mapping data showing high and low alch values of items

    :param url: The URL to fetch mapping data from
    :return: A list of dictionaries of each item
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

def calculate_alch_margins(price_data: Dict[str, Any], mapping_data: List[Dict[str, Any]]) -> List:
    """
    Goes over all items in the mapping data finding ones with profitable alch margins.

    :param price_data: A dictionary of the current price data
    :param mapping_data: A list of dictionaries of each item
    :return: A list of alch margins data, sorted highest to lowest
    """

    alch_margins = []
    for item in mapping_data:
        # Safely check for keys
        item_id = item.get('id')
        highalch = item.get('highalch')
        value = item.get('value')

        # Skip invalid items
        if not (item_id and highalch and value and value != 0):
            continue

        # Safely get price data
        price_item = price_data.get(str(item_id), {})
        high_price = price_item.get('high')

        # Skip if not high price found
        if not high_price:
            continue

        alch_margin = highalch - high_price
        alch_margins.append({
            'item_id': item_id,
            'name': item.get('name', 'Unknown'),
            'high_alch': highalch,
            'buy_price': high_price,
            'alch_margin': alch_margin
        })

    # Sort alch margins by highest
    alch_margins.sort(key=lambda x: x['alch_margin'], reverse=True)

    return alch_margins

def display_top_alch_margins(data: List, limit: int = 10) -> None:
    """
    Displays a formatted list of the top x price swings

    :param data: A list of alch margins data
    :param limit: A number to limit the list to
    """

    # Headers with consistent column widths
    print(f"{'Item ID':<8} {'Name':<30} {'High Alch':<10} {'Buy Price':<10} {'Margin':<10}")
    print("-" * 70) # Line separator

    # Rows with the same widths
    for i, item in enumerate(data[:limit]):
        print(f"{item['item_id']:<8} {item['name']:<30} {item['high_alch']:<10} {item['buy_price']:<10} {item['alch_margin']:<10}")

def main():
    # Fetch price and mapping data
    print("Fetching OSRS pricing data...")
    price_data = fetch_price_data('https://prices.runescape.wiki/api/v1/osrs/latest')
    mapping_data = fetch_mapping_data('https://prices.runescape.wiki/api/v1/osrs/mapping')
    print(f"Successfully fetched pricing data for {len(mapping_data)} items!\n")

    # Calculate items with the best alch margins
    alch_margins = calculate_alch_margins(price_data, mapping_data)

    # Display top alch margins
    print(f"Here are the top items with the highest alch margin:\n")
    display_top_alch_margins(alch_margins)

    print("\nThanks for using the OSRS Alch Margin Tool!")

if __name__ == "__main__":
    main()