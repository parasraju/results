from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client
import time
import os

# Twilio API credentials
account_sid = "AC63659c9f9e3776f63be2d5d4e23cf354"
auth_token = "99f2a5d09864e6adcb5be519d14b2f3b"
twilio_phone_number = "+15078660968"
your_phone_number = "+917986313672"

# Student details
year = "2024"
month = "12"
course_type = "C"
course = "1703"
semester = "170301"
roll_number = "2230423"

# URL of the result page
url = "https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx"

# **Manually Set Your Brave Browser Path**
BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# Function to set up Selenium WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = BRAVE_PATH  # Manually setting the path
    options.add_argument("--headless")  # Runs in the background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Function to check if the result is available
def is_result_available(driver):
    driver.get(url)
    time.sleep(2)

    # Select Year and Month
    Select(driver.find_element(By.ID, "DrpDwnYear")).select_by_value(year)
    Select(driver.find_element(By.ID, "DrpDwnMonth")).select_by_value(month)

    # Select Course Type
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "DropDownCourseType"))).click()
    Select(driver.find_element(By.ID, "DropDownCourseType")).select_by_value(course_type)

    # Wait for Course Dropdown
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "DropDownCourse"))).click()
    Select(driver.find_element(By.ID, "DropDownCourse")).select_by_value(course)

    # Wait for Semester Dropdown
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "DropDownSemester"))).click()
    Select(driver.find_element(By.ID, "DropDownSemester")).select_by_value(semester)

    # Enter Roll Number and Check Result
    driver.find_element(By.ID, "TextBoxRollNo").send_keys(roll_number)
    driver.find_element(By.ID, "btnResult").click()
    time.sleep(2)

    # Check if results are displayed
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "lblResult")))
        return True
    except:
        return False

# Function to send an SMS notification
def send_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="🎉 Your GNDU exam results are out! Check now: https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx",
        from_=twilio_phone_number,
        to=your_phone_number
    )
    print(f"📩 SMS sent! SID: {message.sid}")

# Main function
def main():
    driver = setup_driver()
    if is_result_available(driver):
        print("✅ Results are available!")
        send_sms()
    else:
        print("❌ Results are NOT available yet.")
    driver.quit()

# Run the script
if __name__ == "__main__":
    main()
