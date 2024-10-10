# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd
import time

# Set up Chrome options for Selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")  # Uncomment to run in headless mode

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Path to your HTML file with the correct protocol
websites = f"file:///{getcwd().replace('\\', '/')}/index.html"
print(f"Loading website from: {websites}")

# Load the HTML file in the browser
driver.get(websites)

# Allow time for the page to load
time.sleep(2)

# File to save the recognized text
rec_file = f"{getcwd()}\\input.txt"

def listen():
    try:
        # Wait for the Start Listening button to be clickable and click it
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'StartButton')))
        start_button.click()
        print("Listening...")
        output_text = ""
        is_second_click = False
        
        while True:
            # Wait for the output element to be present
            output_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()
            
            # Check if the button text indicates it is ready for a new click
            if "Start Listening" in start_button.text:
                is_second_click = False
                
                # If the current text differs from the previous output, save it
                if current_text != output_text:
                    output_text = current_text
                    with open(rec_file, 'w') as file:  # Corrected 'w' to 'w' string
                        file.write(output_text.lower())
                        print("\nUSER: " + output_text)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    listen()  # Start the listening process
