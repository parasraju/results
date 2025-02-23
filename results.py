import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client
import time

# Twilio API credentials (Replace with your actual values)
account_sid = 'AC3bab56e93cacdd77717f5aac09ebb044'
auth_token = '9b42cfb5e9accbf376e584c92eff4fca'
twilio_phone_number = '+16057777609'
your_phone_number = '+917681985728'

# Student details
year = '2024'
month = '12'
course_type = 'C'
course = '1703'
semester = '170301'
roll_number = '17032400172'

# URL of the result page
url = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'

# Auto-detect browser
def get_browser_path():
    paths = [
        "/usr/bin/brave-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium"
    ]
    for path in paths:
        if shutil.which(path):
            return path
    raise Exception("❌ No supported browser found. Install Brave, Chromium, or Chrome!")


# Function to set up Selenium WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Runs in the background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")  # Debugging port

    # Detect and set browser binary location
    options.binary_location = get_browser_path()

    # Install WebDriver automatically
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def is_result_available(driver):
    driver.get(url)
    time.sleep(2)  # Let page load

    try:
        # Select Year and Month
        Select(driver.find_element(By.ID, 'DrpDwnYear')).select_by_value(year)
        Select(driver.find_element(By.ID, 'DrpDwnMonth')).select_by_value(month)

        # Select Course Type (CBES)
        course_type_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'DropDownCourseType'))
        )
        Select(course_type_dropdown).select_by_value(course_type)

        # Wait for Course Dropdown (`DrpDwnCMaster`) to Load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'DrpDwnCMaster'))
        )

        # Get Available Course Options
        course_dropdown = Select(driver.find_element(By.ID, 'DrpDwnCMaster'))
        options = [opt.get_attribute("value") for opt in course_dropdown.options]
        print("Available Courses:", options)  # DEBUG

        # Check if "1703" is Present
        if course in options:
            course_dropdown.select_by_value(course)
        else:
            print(f"Error: Course '{course}' not found in dropdown!")
            return False

        # Wait for Semester Dropdown (`DrpDwnCdetail`) to Load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'DrpDwnCdetail'))
        )

        # Select Semester
        Select(driver.find_element(By.ID, 'DrpDwnCdetail')).select_by_value(semester)

        # Enter Roll Number
        roll_input = driver.find_element(By.ID, 'textboxRno')
        roll_input.clear()
        roll_input.send_keys(roll_number)

        # Submit
        submit_button = driver.find_element(By.ID, 'buttonShowResult')
        submit_button.click()

        time.sleep(3)  # Allow result to load

        # Check if the result is displayed
        try:
            result_element = driver.find_element(By.ID, 'result-indicator-id')  # Update this ID if incorrect
            if "Result is out" in result_element.text:
                return True
        except:
            return False

    except Exception as e:
        print(f"⚠️ Error checking result: {e}")
        return False

# Function to send an SMS notification
def send_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Your GNDU result is out! Check it at: " + url,
        from_=twilio_phone_number,
        to=your_phone_number
    )
    print(f"📩 Message sent: {message.sid}")

# Main function to keep checking the result
def main():
    driver = setup_driver()

    while True:
        if is_result_available(driver):
            send_sms()
            break
        print("🔄 Result not available yet. Checking again in 30 minutes...")
        time.sleep(1800)  # Wait for 30 minutes before checking again

    driver.quit()

if __name__ == "__main__":
    main()
