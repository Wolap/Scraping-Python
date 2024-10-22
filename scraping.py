import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Nom catégories + listes avec les noms des catégories
cathegories_names = ["books"]
cathegories = soup.find('div', class_='side_categories').find('ul').find_all('li')
for cathegorie in cathegories:
    cathegories_names.append(cathegorie.text.strip())
    # print(cathegories_names)


# Phase 2 : toutes les pages de livres d'une catégorie

# Liens vers cathégories
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Récupérer les liens vers les pages de livres et les stocker dans une liste
books_links = []
books = soup.find_all('h3')
for book in books:
    books_links.append(book.find('a')['href'].replace('../../..', 'https://books.toscrape.com/catalogue'))
    print(books_links)

# Ouverture du fichier CSV
with open ('phase_2.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writter = csv.writer(fichier_csv)
    writter.writerow(['Titre', 'UPC', 'Prix TTC', 'Prix HT', 'Stock', 'Description', 'Catégorie', 'Note', 'URL de l\'image'])

# Récupérer les informations de chaque livre
for lien in books_links:
    response = requests.get(lien)
    soup = BeautifulSoup(response.text, "html.parser")

    # UPC
    universal_product_code = soup.find('table').find_all('tr')[0].text.split('UPC')[1]

    # Titres
    title = soup.find('h1').text

    # Price with taxes
    price_including_tax = soup.find('table').find_all('tr')[3].text.split('£')[1]
    price_including_tax.encode('utf-8').decode('utf-8')

    # Price without taxes
    price_excluding_tax = soup.find('table').find_all('tr')[2].text.split('£')[1]
    price_excluding_tax.encode('utf-8').decode('utf-8')

    # Stock
    number_available = soup.find('table').find_all('tr')[5].text.split('(')[1].split(' available')[0]
    number_available.encode('utf-8').decode('utf-8')

    # Description
    product_description = soup.find_all('p')[3].text.encode('utf-8').decode('utf-8')

    # Category
    category = soup.find_all('a')[3].text.encode('utf-8').decode('utf-8')

    # Review rating
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    review_rating.encode('utf-8').decode('utf-8')

    # Image URL
    image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com')
    image_url.encode('utf-8').decode('utf-8')

    with open('phase_2.csv', 'a', newline='', encoding='utf-8') as fichier_csv:
        writter = csv.writer(fichier_csv)
        writter.writerow([title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])

