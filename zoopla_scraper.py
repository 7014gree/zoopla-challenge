import requests
from bs4 import BeautifulSoup

# Writes html string to text.txt for ease of review.
def write_to_txt(text, path):
    with open(path, 'w', encoding="utf-8") as f:
            f.write(text)
    print("Written successfully")


property_information = []
next_page_url = "https://www.zoopla.co.uk/new-homes/property/london/"

for page in range(1, 6):
    r = requests.get(next_page_url)
    print(page, next_page_url)
    html_string = r.text
    soup = BeautifulSoup(html_string, 'html.parser')

    s = soup.find_all(name = 'div', attrs={'class': "c-iyCMIE c-iyCMIE-rwbZU-borderBottom-true"})

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

    write_to_txt(f"{next_page_url}\n\n{property_information}", f"text-{page}.txt")

    next_page_tag = soup.find(name = 'li', attrs={'class': "css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"})
    next_page_url = "https://www.zoopla.co.uk" + next_page_tag.find(name = 'a', attrs={'class': "eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"})['href']

    