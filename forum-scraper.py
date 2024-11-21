import requests
from bs4 import BeautifulSoup

# Class to hold scraped data
class ScrapedData:
  def __init__(self, aid, title, date, publisher, views, comments_count, content):
    self.aid = aid
    self.title = title
    self.date = date
    self.publisher = publisher
    self.views = views
    self.comments_count = comments_count
    self.content = content

  # String representation of the object
  def __str__(self):
      return f"""
      Aid: {self.aid}
      Title: {self.title}
      Date: {self.date}
      Publisher: {self.publisher}
      Views: {self.views}
      Comments Count: {self.comments_count}
      Content: 
      {self.content}
        """

# Scrape article from URL and aid
def scrape_article(url, aid):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title = soup.find('title').text

    # Extract date
    date_tag = soup.find('p', class_='xg1')
    date = date_tag.text.split('|')[0].strip() if date_tag else "Unknown"

    # Extract publisher
    publisher_tag = date_tag.find('a') if date_tag else None
    publisher = publisher_tag.text if publisher_tag else "Unknown"

    # Extract views
    views_tag = soup.find('em', id='_viewnum')
    views = views_tag.text if views_tag else "0"

    # Extract comments count
    comments_tag = soup.find('em', id='_commentnum')
    comments_count = comments_tag.text if comments_tag else "0"

    # Extract content
    content_tag = soup.find('td', id='article_content')
    content = content_tag.get_text(strip=True) if content_tag else ""

    return ScrapedData(aid, title, date, publisher, views, comments_count, content)

# Main function to orchestrate scraping process
def main():
    base_url = "https://b.cari.com.my/portal.php?mod=view&aid="
    
    # List of aids to scrape 
    aid_values = list(range(1,6))  # Should be until 25000+
    aid_values.append(20000) # Because AID is sequential.
    
    for aid in aid_values:
        url = f"{base_url}{aid}"   # Construct full URL
        
        try:
            scraped_data = scrape_article(url, aid)   # Scrape data
            
            print(scraped_data)                         # Print data
            
            print("\n------------------------\n")       # Print separator
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")       # Handle exceptions

if __name__ == "__main__":
    main()                                           # Run main function
