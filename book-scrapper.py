import requests
from bs4 import BeautifulSoup
import json

BOOK_ROOT = "shopstyle1"

allUrl = [
  "https://pservir.pt/index.php/catalogo/livros/vida-familiar",
  "https://pservir.pt/index.php/catalogo/livros/saude",
  "https://pservir.pt/index.php/catalogo/livros/estilo-de-vida",
  "https://pservir.pt/index.php/catalogo/livros/educacao",
  "https://pservir.pt/index.php/catalogo/livros/espirituais",
  "https://pservir.pt/index.php/catalogo/livros/manuais-de-estudo",
]

allBooks = []
for url in allUrl:
  # In the future, to get all the books from each page, you have to get the request cookie and put it here
  # And also go through all the links and set to load all books in th pagination
  result = requests.post(url, {"1faf3583e7f60ceb0c9f6e99b1f422b6": "9sm7hrt6gjbk819ebi9es1b794"})

  assert result.status_code == 200
  html = result.content

  soup = BeautifulSoup(html, "html.parser")
  rawBooks = soup.find_all("div", BOOK_ROOT)

  for rawBook in rawBooks:
    titleContainer = rawBook.find("div", class_="product_title")
    title = titleContainer.h3.a.text.strip()
    barcode = int(titleContainer.span.a.text.strip())
    # Convert "19,05 €" to number 19.05
    price = float(rawBook.find("div", class_="price-detail").text.strip().replace(",", ".").replace(" €", ""))
    cover = "https://pservir.pt" + rawBook.find("figcaption").a["href"]

    book = {
      "title": title,
      "barcode": barcode,
      "price": price,
      "cover": cover
    }

    allBooks.append(book)
  
  print(str(len(rawBooks)) + " books in " + url)

print("In total " + str(len(allBooks)) + " books")
f = open("books.json", "w")
f.write(json.dumps(allBooks, indent=2, ensure_ascii=False))
f.close()
