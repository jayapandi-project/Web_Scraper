from bs4 import BeautifulSoup
import requests,openpyxl,sqlite3
import pandas as pd

# Create a new workbook and select the active sheet
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Product List"

# Write headers to the sheet
sheet.append(['Title', 'Description', 'Price'])

iteam_list = []  # List to collect scraped data

try:
    url = 'https://webscraper.io/test-sites/e-commerce/scroll'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product items
    items = soup.find_all('div', class_="caption")

    for item in items:
        iteam_title = item.find("a", class_="title").text.strip()
        iteam_prices = item.find("h4", class_="price float-end card-title pull-right").text.strip()
        iteam_prices = iteam_prices.replace("$", "RS ")
        iteam_description = item.find("p", class_="description card-text").text.strip()

        # Append data to the Excel sheet and to the list
        sheet.append([iteam_title, iteam_description, iteam_prices])
        iteam_list.append([iteam_title, iteam_description, iteam_prices])
        break  # Remove this break to process all items

except Exception as e:
    print(e)

# Save the workbook
excel.save("products.xlsx")

# Create a DataFrame from the collected data
df = pd.DataFrame(data=iteam_list, columns=['Title', 'Description', 'Price'])
print(df.head())

# Connect to SQLite database and create table
connection = sqlite3.connect("web_scraper.db")
cursor = connection.cursor()

query = """
CREATE TABLE IF NOT EXISTS products (
    iteam_title TEXT,
    iteam_description TEXT,
    iteam_prices TEXT
)
"""
cursor.execute(query)

# Insert data into SQLite database
for index, row in df.iterrows():
    cursor.execute("INSERT INTO products (iteam_title, iteam_description, iteam_prices) VALUES (?, ?, ?)",
                   (row['Title'], row['Description'], row['Price']))

connection.commit()
connection.close()
