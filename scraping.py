import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import shutil

# Clean file name
def clean_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)


# Clear images and CSV folders if they exist
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        # Remove all files and subfolders inside the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    # Remove the entire folder and its contents
                    shutil.rmtree(file_path)  
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

# Create or clear folders for images and CSVs
if not os.path.exists('images'):
    os.makedirs('images')
else:
    clear_folder('images')

if not os.path.exists('csv'):
    os.makedirs('csv')
else:
    clear_folder('csv')

url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

categories_links = []
categories_names = []
categories = soup.find('div', class_='side_categories').find('ul').find_all('li')

# Store categories href in a list
for category in categories:
    categories_links.append(category.find('a')['href'].replace('..', ''))
    categories_names.append(category.find('a').text.strip().replace(' ', '_'))

# Get all categories links and looks for them
for i in range (len(categories_links)):
    if categories_links[i] == "index.html":
        i += 1
    
    url =  "https://books.toscrape.com/catalogue/category" + categories_links[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    csv_path = os.path.join('csv', categories_names[i] + '.csv')
    
    # Open CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as fichier_csv:
        writter = csv.writer(fichier_csv)
        writter.writerow(['Titre', 'UPC', 'Prix TTC', 'Prix HT', 'Stock', 'Description', 'Categorie', 'Note', 'URL of image'])


    title_page = soup.find('h1').text
    print("Titre Page ", title_page)

    # Store pages links of a cathegory in a list
    books_links = []
    books = soup.find_all('h3')
    for book in books:
        books_links.append(book.find('a')['href'].replace('../../..', 'https://books.toscrape.com/catalogue'))
        # print(books_links)

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
        try:
            price_including_tax = soup.find('table').find_all('tr')[3].text.split('£')[1]
        except:
            price_including_tax = "n/a"

        # Price without taxes
        try:
            price_excluding_tax = soup.find('table').find_all('tr')[2].text.split('£')[1]
        except:
            price_excluding_tax = "n/a"

        # Stock
        try:
            number_available = soup.find('table').find_all('tr')[5].text.split('(')[1].split(' available')[0]
        except:
            number_available = "n/a"

        # Description
        try:
            product_description = soup.find_all('p')[3].text
        except:
            product_description = "n/a"

        # Category
        category = soup.find_all('a')[3].text

        # Review rating
        try:
            review_rating = soup.find('p', class_='star-rating')['class'][1]
        except:
            review_rating = "n/a"

        # Creat folder for each category of images
        if not os.path.exists('images/' + categories_names[i]):
            os.makedirs('images/' + categories_names[i])
        else:
            pass
            
        # Image URL
        image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com')

        # Get image
        image = requests.get(image_url)

        # Check if image is valid
        if image.status_code == 200 and 'image' in image.headers['Content-Type']:
            # Save image
            with open(f"images/{categories_names[i]}/{clean_title}.jpg", 'wb') as file:
                file.write(image.content)
        else:
            print(f"Erreur lors du téléchargement de l'image pour le livre: {title}")

        # Write data in CSV file
        with open(csv_path, 'a', newline='', encoding='utf-8') as fichier_csv:
            writter = csv.writer(fichier_csv)
            writter.writerow([title, universal_product_code, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
