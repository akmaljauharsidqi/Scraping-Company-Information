from bs4 import BeautifulSoup
from .models import Company
from .__init__ import BASE_URL

from bs4 import BeautifulSoup
from .models import Company

class Soup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, "html.parser")
        
    def scrape(self):
        # Company Name
        company_name = self.safe_find_text(self, "h1")
        
        # Contact Name
        contact_name = ""
        contact_info = self.find("div", class_="member-contact-info")
        if contact_info:
            contact_element = contact_info.find("p")
            if contact_element and "Contact Name:" in contact_element.get_text():
                contact_name = contact_element.get_text(strip=True).replace("Contact Name:", "").strip()
        
        # Address
        address = ""
        if contact_info:
            address_element = contact_info.find_all("p")
            if len(address_element) > 1 and "Address:" in address_element[1].get_text():
                address = address_element[1].get_text(strip=True).replace("Address:", "").strip()
                address = ' '.join(address.split())
        
        # Website
        website = ""
        if contact_info:
            website_element = contact_info.find('a', href=True)
            website = website_element['href'].replace("http://", "").strip() if website_element else ""
        
        # Email
        email = ""
        if contact_info:
            email_element = contact_info.find('a', class_="button", href=True)
            email = email_element['href'].replace("mailto:", "").strip() if email_element else ""
        
        # Company Description
        company_description = ""
        article = self.find("article", class_="members")
        
        if article:
            contact_info = article.find("div", class_="member-contact-info")

            if contact_info:
                paragraphs = article.find_all("p")
                
                for paragraph in paragraphs:
                    if paragraph not in contact_info.find_all("p") and "MEMBER SINCE" not in paragraph.get_text():
                        company_description = paragraph.get_text()
                        
        # Member Since
        member_since = ""
        if article:
            member_since_element = article.find("p", class_="bold italic")
            member_since = member_since_element.get_text(strip=True).replace("MEMBER SINCE", "").strip() if member_since_element else ""
        
        # Tags
        tags = self.safe_find_text(self, "div.mt-40")
        
        # Location
        location = ""
        map_info = self.find("div", class_="acf-map")
        if map_info:
            marker = map_info.find("div", class_="marker")
            if marker:
                lat = marker.get("data-lat")
                lng = marker.get("data-lng")
                if lat and lng:
                    location = f"www.google.com/maps?q={lat},{lng}"
        
        # Return the scraped data
        return Company(
            company_name=company_name,
            contact_name=contact_name,
            address=address,
            website=website,
            email=email,
            company_description=company_description,
            member_since=member_since,
            tags=tags,
            location=location
        )
    
    def safe_find_text(self, parent, selector, default=""):
        element = parent.select_one(selector)
        return element.get_text(strip=True) if element else default
    
    def scrape_urls(self):
        urls = []
        for div in self.find_all("div", class_="column is-one-fifth"):
            url = div.find("a")
            if url and url.get('href'):
                urls.append(url['href'])
        return urls
                
    def scrape_categories(self):
        categories = []
        for div in self.find_all("div", class_="column is-3-desktop is-3-tablet is-6-mobile"):
            url = div.find("a")
            if url and url.get('href'):
                categories.append(url['href'])
        return categories

        
