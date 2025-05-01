from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Import the Service class
from selenium.webdriver.chrome.options import Options  # Optional if you need headless mode
from bs4 import BeautifulSoup
import time

# Path to your web driver (make sure to change this to the correct path of your WebDriver)
driver_path = r'C:\webdriver\chromedriver-win64\chromedriver.exe'  # Adjust with your actual path

# Function to scrape the country chart using Selenium
def scrape_youtube_chart(country_code):
    url = f"https://charts.youtube.com/charts/TopSongs/{country_code}/weekly"
    
    # Set up Chrome options (optional, if you need to run Chrome in headless mode)
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Uncomment this line if you want to run Chrome headlessly
    
    # Set up the Service object
    service = Service(executable_path=driver_path)
    
    # Start the Selenium WebDriver with the Service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    
    # Allow the page to load completely
    time.sleep(5)  # Wait for JavaScript to load the page content
    
    # Get the page source after JavaScript has rendered the content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the chart items (adjust based on actual HTML structure)
    chart_items = soup.find_all('ytmc-entry-row')  # The entries are inside 'ytmc-entry-row'
    chart_data = []

    # Iterate through each chart item and extract the artist and song names
    for idx, item in enumerate(chart_items, start=1):
        try:
            # Extract the song title
            song = item.find('div', class_='title').text.strip()
            
            # Extract the artist(s)
            artist_spans = item.find_all('span', class_='artistName')
            artists = " & ".join([artist.text.strip() for artist in artist_spans])
            
            chart_data.append(f"{idx}. {song} - {artists}")
        except AttributeError:
            continue

    # Close the browser after scraping
    driver.quit()

    return chart_data

# Example usage: scraping Germany's music chart
country_code = 'de'  # Germany's country code
chart_data = scrape_youtube_chart(country_code)

# Write the scraped data to a .txt file with UTF-8 encoding
with open("music_chart.txt", "w", encoding="utf-8") as file:
    for line in chart_data:
        file.write(line + "\n")

# Display a success message
print("Data has been written to 'music_chart.txt'.")
