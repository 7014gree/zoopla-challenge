import requests
from bs4 import BeautifulSoup

# Writes html string to text.txt for ease of review.
def write_to_txt(text, path):
    with open(path, 'w', encoding="utf-8") as f:
            f.write(text)
    print(f"Written to {path} successfully.")

class ZooplaScraper:
    def __init__(self, url):
        self.url = url

    def request_html(self):
        r = requests.get(self.url)
        html_string = r.text
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup
    
    def set_next_url(self, soup):
        next_page_button_tag = soup.find(name = 'li', attrs={'class': "css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"})
        self.url = "https://www.zoopla.co.uk" + next_page_button_tag.find(name = 'a', attrs={'class': "eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"})['href']

    def get_house_listings(self, soup):
        listings_on_page = soup.find_all(name = 'div', attrs={'class': "c-iyCMIE c-iyCMIE-rwbZU-borderBottom-true"})
        property_information = []
        for listing in listings_on_page:
            property_information.append(self.listing_to_dict(listing))
        return property_information

    def listing_to_dict(self, listing):
        listing_url =  "https://www.zoopla.co.uk" + listing.find(name = 'a', attrs={'class': "c-enSgsc"})['href']

        summary =  listing.find(name = 'h2', attrs={'data-testid': "listing-title"}).text

        price = int(listing.find(name = 'p', attrs={'class': "c-bTssUX", 'data-testid': "listing-price"}).text.replace(",","").replace("£",""))
        
        room_info = listing.findAll(name = 'span', attrs={'class': "c-PJLV"})

        bedrooms = room_info[0].text
        bathrooms = room_info[0].text
        living_rooms = room_info[0].text

        address = listing.find(name = 'h3', attrs={'class': "c-eFZDwI"}).text

        station_info = listing.findAll(name = 'span', attrs={'class': "c-UazGY"})
        nearest_station_1 = station_info[0].text
        nearest_station_2 = station_info[1].text

        other_info_html = listing.findAll(name = 'div', attrs={'class': "c-PJLV c-PJLV-kQvhQW-centered-true c-PJLV-iPJLV-css"})
        other_info = []
        for html_tag in other_info_html:
            other_info.append(html_tag.text)

        date_listed = listing.find(name = 'li', attrs={'class': "c-eUGvCx"}).text

        listing_dict = {
            'listing url': listing_url,
            'summary': summary,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'living rooms': living_rooms,
            'address': address,
            'nearest station 1': nearest_station_1,
            'nearest station 2': nearest_station_2,
            'other info': other_info,
            'date listed': date_listed
            }

        return listing_dict


if __name__ == "__main__":
    z = ZooplaScraper("https://www.zoopla.co.uk/new-homes/property/london/")
    for i in range(5):
        soup = z.request_html()
        house_listings = z.get_house_listings(soup)
        print(f"Scraping: {z.url}")
        write_to_txt(f"{z.url}\n\n{house_listings}",f"text-{i + 1}.txt")
        z.set_next_url(soup)

