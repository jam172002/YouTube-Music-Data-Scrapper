import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

    # Iterate through each chart item and extract the artist, song names, and views
    for idx, item in enumerate(chart_items, start=1):
        try:
            # Extract the song title
            song = item.find('div', class_='title').text.strip()
            
            # Extract the artist(s)
            artist_spans = item.find_all('span', class_='artistName')
            artists = " & ".join([artist.text.strip() for artist in artist_spans])
            
            # Extract the weekly views (correct class found in HTML)
            views = item.find_all('div', class_='metric content center tablet-non-displayed-metric style-scope ytmc-entry-row')
            
            # Get the last div in the row which contains the weekly views
            views_text = views[-1].text.strip() if views else "No views data"
            
            chart_data.append(f"{idx}. {song} - {artists} | Weekly Views: {views_text}")
        except AttributeError:
            continue

    # Close the browser after scraping
    driver.quit()

    return chart_data

# Function that triggers the scraping based on selected countries
def run_scraper():
    # Get the selected countries
    selected_countries = [country for country, var in country_vars.items() if var.get()]

    if not selected_countries:
        messagebox.showerror("Error", "Please select at least one country.")
        return

    # Scrape data for each selected country and save it to a separate text file
    for country_code in selected_countries:
        chart_data = scrape_youtube_chart(country_code)
        
        # Create a filename based on the country code
        file_name = f"{country_code}_music_chart.txt"
        
        # Write the scraped data to a separate .txt file for each country
        with open(file_name, "w", encoding="utf-8") as file:
            for line in chart_data:
                file.write(line + "\n")
        
        # Show success message for each country
        messagebox.showinfo("Success", f"Data for {country_code} has been written to '{file_name}'.")

# GUI setup
root = tk.Tk()
root.title("YouTube Music Chart Scraper")
root.geometry("500x350")  # Set window size
root.config(bg="#2C3E50")  # Set background color

# Title label
label = tk.Label(root, text="Select countries to scrape music charts from:", fg="#ECF0F1", bg="#2C3E50", font=("Helvetica", 12))
label.pack(pady=20)

# Countries and corresponding checkboxes
country_vars = {
    "Germany": tk.BooleanVar(value=True),
    "Austria": tk.BooleanVar(value=True),
    "US": tk.BooleanVar(value=True),
    "UK": tk.BooleanVar(value=True),
    # Add more countries as needed
}

# Create checkboxes for each country
for country, var in country_vars.items():
    checkbox = tk.Checkbutton(root, text=country, variable=var, fg="#ECF0F1", bg="#2C3E50", font=("Helvetica", 10), selectcolor="#34495E")
    checkbox.pack(anchor='w', padx=20)

# Run button
run_button = tk.Button(root, text="Run Scraper", command=run_scraper, fg="#2C3E50", bg="#3498DB", font=("Helvetica", 12), relief="flat", width=20, height=2)
run_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
# Note: Make sure to have the required libraries installed (selenium, beautifulsoup4, tkinter).