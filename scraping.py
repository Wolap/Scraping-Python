import requests
from bs4 import BeautifulSoup
import csv
import os
import re

# Clen file name
def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# Create folder is not existing
if not os.path.exists('images'):
    os.makedirs('images')

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Store pages links in a list
books_links = []
books = soup.find_all('h3')
for book in books:
    books_links.append(book.find('a')['href'].replace('../../..', 'https://books.toscrape.com/catalogue'))
    print(books_links)

# Open CSV file
with open('phase_2.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writter = csv.writer(fichier_csv)
    writter.writerow(['Titre', 'UPC', 'Prix TTC', 'Prix HT', 'Stock', 'Description', 'Catégorie', 'Note', 'URL de l\'image'])

# Get books information from each page
for lien in books_links:
    response = requests.get(lien)
    soup = BeautifulSoup(response.text, "html.parser")

    # UPC
    universal_product_code = soup.find('table').find_all('tr')[0].text.split('UPC')[1]

    # Titles
    title = soup.find('h1').text.encode('utf-8').decode('utf-8')

    # Nettoyage du titre pour en faire un nom de fichier valide
    clean_title = clean_filename(title)

    # Price with taxes
    price_including_tax = soup.find('table').find_all('tr')[3].text.split('£')[1]

    # Price without taxes
    price_excluding_tax = soup.find('table').find_all('tr')[2].text.split('£')[1]

    # Stock
    number_available = soup.find('table').find_all('tr')[5].text.split('(')[1].split(' available')[0]

    # Description
    product_description = soup.find_all('p')[3].text

    # Category
    category = soup.find_all('a')[3].text

    # Review rating
    review_rating = soup.find('p', class_='star-rating')['class'][1]

    # Image URL + Download image
    image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com')
    print("Image URL", image_url)

    # Get image
    image = requests.get(image_url)

    # Check if image is valid
    if image.status_code == 200 and 'image' in image.headers['Content-Type']:
        # Save image
        with open(f'images/{clean_title}.jpg', 'wb') as file:
            file.write(image.content)
    else:
        print(f"Erreur lors du téléchargement de l'image pour le livre: {title}")

    # Write data in CSV file
    with open('phase_2.csv', 'a', newline='', encoding='utf-8') as fichier_csv:
        writter = csv.writer(fichier_csv)
        writter.writerow([title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
