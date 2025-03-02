from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Load spreadsheet (update filename and column name)
file_path = "contacts.xlsx"  # Change this to your file
df = pd.read_excel(file_path)

# LinkedIn credentials
LINKEDIN_EMAIL = "enter ur email"
LINKEDIN_PASSWORD = "enter ur password"

# Start WebDriver (Ensure you have ChromeDriver installed)
driver = webdriver.Chrome()

def login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)  # Allow page to load

    # Enter email
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(LINKEDIN_EMAIL)

    # Enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(LINKEDIN_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Allow login to complete

def send_connection_request(profile_url):
    driver.get(profile_url)
    time.sleep(3)

    try:
        # Find and click the 'Connect' button
        # connect_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Invite') and contains(@aria-label, 'to connect')]")
        # Example: Wait until the Connect button is clickable using the span text
        # connect_button = WebDriverWait(driver, 15).until(
        #     EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'connect')]/ancestor::button"))
        # )
        # # Save a screenshot for debugging
        # driver.save_screenshot("profile_debug.png")

        # # Optionally, print part of the HTML
        # print(driver.page_source[:1000])

        # connect_button.click()
        # time.sleep(2)

        # Find all "Connect" buttons
        connect_buttons = driver.find_elements(By.XPATH, "//button[.//span[contains(@class, 'artdeco-button__text') and text()='Connect']]")
        print('finding buttons was fine')
        print(connect_buttons)

        for button in connect_buttons:

            # Scroll to the "Connect" button to bring it into view
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)  # Allow time for scrolling

            # Try normal click
            try:
                button.click()
            except:
                # Fallback to JavaScript click if intercepted
                driver.execute_script("arguments[0].click();", button)

            time.sleep(2)  # Allow time for the pop-up to load

            # Click the "Send without a note" button in the pop-up
            try:
                send_without_note_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(@class, 'artdeco-button__text') and text()='Send without a note']]"))
                )
                send_without_note_button.click()
                print("Connection request sent successfully.")
                time.sleep(2)
            except Exception as send_error:
                print(f"Error finding 'Send without a note' button: {send_error}")


        # # Confirm sending the request
        # send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send now')]")
        # send_button.click()
        # time.sleep(2)
        
        print(f"✅ Sent request to {profile_url}")
    except Exception as e:
        print(f"❌ Could not connect with {profile_url}: {e}")

# Run the bot
login()
for index, row in df.iterrows():
    profile_link = row["Person Linkedin Url"]  # Adjust column name if needed
    send_connection_request(profile_link)

driver.quit()
