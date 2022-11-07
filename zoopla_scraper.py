import requests
from bs4 import BeautifulSoup


r = requests.get("https://www.zoopla.co.uk/new-homes/property/london/")
html_string = r.text
soup = BeautifulSoup(html_string, 'html.parser')

# Writes html string to text.txt for ease of review.
def write_to_txt(string):
    with open('text.txt', 'w', encoding="utf-8") as f:
            f.write(string)
    print("Written successfully")

write_to_txt(soup.prettify())