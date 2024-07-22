import requests
from bs4 import BeautifulSoup


def scrape_product_data(asin):
    url = f"https://www.amazon.com/dp/{asin}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        name = soup.find(id='productTitle').get_text(strip=True)
        price = float(
            soup.find('span', 'a-price').find('span', 'a-offscreen').get_text(strip=True).replace('$', '').replace(',',
                                                                                                                   ''))
        rating = float(soup.select_one('span[data-hook="rating-out-of-text"]').get_text(strip=True).split(' ')[0])

        rating_text = soup.select_one('span[data-hook="total-review-count"]').get_text(strip=True)
        average_rating = float(rating_text.split()[0].replace(',', ''))

        return {
            'asin': asin,
            'name': name,
            'price': price,
            'rating': rating,
            'average_rating': average_rating
        }
    except AttributeError as e:
        print(f"Error scraping ASIN {asin}: {e}")
        return None
