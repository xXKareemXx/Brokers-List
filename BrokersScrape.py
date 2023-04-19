import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the URL of the webpage with the sale brokers data
url = 'https://dubailand.gov.ae/en/eservices/licensed-real-estate-brokers/licensed-real-estate-brokers-list/#/'

# Set the path to the Chrome driver executable
chromedriver_path = '/Users/kareem/Documents/ChromeDriver_mac64/chromedriver'

# Configure Chrome options
options = Options()
options.add_argument('--headless')  # run Chrome in headless mode

# Launch Chrome
driver = webdriver.Chrome(chromedriver_path)

# Load the webpage
driver.get(url)

# Wait for the page to load
time.sleep(7)

# Count number page loaded
pages=1

# Click the "Load more" button repeatedly until it's no longer visible
while 1:
    # if(pages==10):
    #     break
    try:
        if(pages>1):
            time.sleep(7.5)
        # loadButton = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, '//*[@id="load-more"]/div')
        #     )
        # )
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="load-more"]').click()
        print(f"Clicked {pages} time.")
    except:
        print("Reached End of the Page")
        break
    pages += 1


# Initialize empty lists to store the sale brokers data
names = []
emails = []
numbers = []
companies = []

# Counter for brokers
i=0

# print("Total brokers="+str((pages)*9))
time.sleep(5)

while(1):
    # l = len(container.find_elements(By.XPATH, f'//*[@id="broker"]/div[{i+2}]/div/div/div'))
    if(i == (pages)*9):
        print("End of Brokers")
        break
    for broker in driver.find_elements(By.XPATH, f'//*[@id="broker"]/div[{i+2}]/div/div/div'):
        names.append(broker.find_element(By.XPATH, f'//*[@id="broker"]/div[{i+2}]/div/div/div/a/div').text)
        companies.append(broker.find_element(By.XPATH, f'//*[@id="office-name-{i}"]').text)
        emails.append(broker.find_element(By.XPATH, f'//*[@id="email-{i}"]/a').text)
        numbers.append(broker.find_element(By.XPATH, f'//*[@id="phone-{i}"]/a').text)
        print(f'Broker {i+1}')
        i += 1


print('Names: ', names)
print('Emails: ', emails)
print('Phone: ', numbers)
print('Company: ', companies)

# Create a dictionary to store the sale brokers data
data = {
    'Name': names,
    'E-mail': emails,
    'Number': numbers,
    'Comp Name': companies
}

# Create a pandas DataFrame from the data dictionary
df = pd.DataFrame(data)
print(df)

# Append DataFrame to existing excel file
with pd.ExcelWriter('/Users/kareem/Documents/Dubai Rest.xlsx', mode='a') as writer:
    df.to_excel(writer, sheet_name='Final2')

# Quit Chrome
driver.quit()