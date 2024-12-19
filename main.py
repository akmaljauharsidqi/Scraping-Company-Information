from os import access
from src.utils import get_html
from src.soup import Soup
from src.__init__ import COMPANY_URL, CATEGORY_URL, BASE_URL
from src.utils import get_html, save_to_xlsx

def main():
    output = []
    soup = get_html(BASE_URL)
    categories = soup.scrape_categories()
    for category in categories:
        print(f"Enter Category {category}")
        category = get_html(category)
        urls = category.scrape_urls()
        for url in urls:
            print(f"Scrapping URL {url}")
            url = get_html(url)
            company = url.scrape()
            output.append(company)
    save_to_xlsx(output, "company.xlsx")

    
if __name__ == '__main__':
    main()