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

account_sid = ""
auth_token = ""
twilio_phone_number = ""
your_phone_number = "+"

year = "
month = ""
course_type = ""
course = ""
semester = ""
roll_number = ""

url = ""

BRAVE_PATH = ""

def setup_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = BRAVE_PATH  
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def is_result_available(driver):
    driver.get(url)
    time.sleep(2)

    Select(driver.find_element(By.ID, "DrpDwnYear")).select_by_value(year)
    Select(driver.find_element(By.ID, "DrpDwnMonth")).select_by_value(month)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "DropDownCourseType"))).click()
    Select(driver.find_element(By.ID, "DropDownCourseType")).select_by_value(course_type)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "DropDownCourse"))).click()
    Select(driver.find_element(By.ID, "DropDownCourse")).select_by_value(course)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "DropDownSemester"))).click()
    Select(driver.find_element(By.ID, "DropDownSemester")).select_by_value(semester)

    driver.find_element(By.ID, "TextBoxRollNo").send_keys(roll_number)
    driver.find_element(By.ID, "btnResult").click()
    time.sleep(2)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "lblResult")))
        return True
    except:
        return False

def send_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="🎉 Your  exam results are out! Check now ]",
        from_=twilio_phone_number,
        to=your_phone_number
    )
    print(f"📩 SMS sent! SID: {message.sid}")

def main():
    driver = setup_driver()
    if is_result_available(driver):
        print("✅ Results are available!")
        send_sms()
    else:
        print("❌ Results are NOT available yet.")
    driver.quit()

if __name__ == "__main__":
    main()
