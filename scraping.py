import requests
from bs4 import BeautifulSoup
import csv

# # URL of the page we want to scrape
# url = "https://books.toscrape.com/"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")

# # Liens vers les livres
# livres = soup.find_all('article')
# for livre in livres:
#     titre = livre.find('h3').find('a')['href']
#     print(titre)

# Phase 1 : une seule page de livre 

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# UPC
universal_product_code = soup.find('table').find_all('tr')[0].text.split('UPC')[1]
# print("UPC :", universal_product_code)

# Titres
title = soup.find('h1').text
# print("Titre :", title)

# Price with taxes
price_including_tax = soup.find('table').find_all('tr')[3].text.split('£')[1]
price_including_tax.encode('utf-8').decode('utf-8')
# print("Prix :", price_including_tax)

# Price without taxes
price_excluding_tax = soup.find('table').find_all('tr')[2].text.split('£')[1]
price_excluding_tax.encode('utf-8').decode('utf-8')
# print("Prix :", price_excluding_tax)

# Stock
number_available = soup.find('table').find_all('tr')[5].text.split('(')[1].split(' available')[0]
number_available.encode('utf-8').decode('utf-8')
# print("Stock :", number_available)

# Description
product_description = soup.find_all('p')[3].text.encode('utf-8').decode('utf-8')
# print("Description :", product_description)

# Category
category = soup.find_all('a')[3].text.encode('utf-8').decode('utf-8')
# print("Catégorie :", category)

# Review rating
review_rating = soup.find('p', class_='star-rating')['class'][1]
review_rating.encode('utf-8').decode('utf-8')
# print("Note :", review_rating)

# Image URL
image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com')
image_url.encode('utf-8').decode('utf-8')
# print("URL de l'image :", image_url)

# Add to CSV file, one information per row
with open('phase_1.csv', 'w', newline='') as fichier_csv:
    writter = csv.writer(fichier_csv)
    writter.writerow([title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
