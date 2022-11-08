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

s = soup.find_all(name = 'div', attrs={'class': "c-iyCMIE c-iyCMIE-rwbZU-borderBottom-true"})
property_information = []
for listing in s:
    listing_dict = {'listing url': "", 'summary': "", 'price': 0, 'bedrooms': 0, 'bathrooms': 0, 'living rooms': 0, 'address': "",
 'nearest station 1': "", 'nearest station 2': "", 'other info': [], 'date listed': ""}

    listing_dict['listing url'] = "https://www.zoopla.co.uk" + listing.find(name = 'a', attrs={'class': "c-enSgsc"})['href']

    listing_dict['summary'] = listing.find(name = 'h2', attrs={'data-testid': "listing-title"}).text

    listing_dict['price'] = listing.find(name = 'p', attrs={'class': "c-bTssUX", 'data-testid': "listing-price"}).text
    
    room_info = listing.findAll(name = 'span', attrs={'class': "c-PJLV"})

    listing_dict['bedrooms'] = room_info[0].text
    listing_dict['bathrooms'] = room_info[0].text
    listing_dict['living rooms'] = room_info[0].text

    listing_dict['address'] = listing.find(name = 'h3', attrs={'class': "c-eFZDwI"}).text

    station_info = listing.findAll(name = 'span', attrs={'class': "c-UazGY"})
    listing_dict['nearest station 1'] = station_info[0].text
    listing_dict['nearest station 2'] = station_info[1].text

    other_info = listing.findAll(name = 'div', attrs={'class': "c-PJLV c-PJLV-kQvhQW-centered-true c-PJLV-iPJLV-css"})
    for html_tag in other_info:
        listing_dict['other info'].append(html_tag.text)


    listing_dict['date listed'] = listing.find(name = 'li', attrs={'class': "c-eUGvCx"}).text

    property_information.append(listing_dict)

write_to_txt(f"{property_information}")