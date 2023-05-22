from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import date


class Product:
    def __init__(self, pName, pFirstDate, pFirstPrice, pLastPrice):
        self.pName = pName
        self.pFirstDate = pFirstDate.replace("-", "/")
        self.pFirstPrice = pFirstPrice[0:pFirstPrice.find(
            ",")].replace(".", "")
        self.pLastDate = date.today().strftime("%d/%m/%Y")
        self.pLastPrice = pLastPrice[0:pLastPrice.find(",")].replace(".", "")

    def __str__(self):
        return self.pName + "\t" + self.pLastDate + "\t" + self.pLastPrice + "\t" + self.pFirstDate + "\t" + self.pFirstPrice + "\n"


def writeToFile(product):
    with open("products.txt", "a", encoding="utf-8") as file:
        file.write(product)


website = "https://www.cimri.com/"
path = ".\chromedriver.exe"
driver = webdriver.Chrome(path)

file_path = "./productLinks.txt"  # Replace with the actual file path

# Read the contents of the file
with open(file_path, "r") as file:
    products = file.readlines()

# Strip any leading/trailing whitespace characters from each line and create the list
products = [line.strip() for line in products]

print(products)

for i in range(len(products)):
    driver.get(website + products[i])

    try:

        # Click on the button
        oneYearButton = driver.find_element(
            By.XPATH, "//button[@type='button' and text()='1 Yıl']")
        oneYearButton.click()

        priceHistory = driver.find_element(
            By.XPATH, "//div[@name='price-history']")

        productName = priceHistory.find_element(
            By.XPATH, "./p[1]").text.strip()

        productName = productName[0:productName.find(" Son")]

        desiredElement = priceHistory.find_element(By.XPATH, "./div[1]")
        currentPrice = priceHistory.find_element(By.XPATH, "./div[2]").find_element(By.XPATH, "./a[1]").find_element(
            By.XPATH, "./div[2]").find_element(By.XPATH, "./div[1]").find_element(By.XPATH, "./p[1]").text.strip()

        desiredElement = desiredElement.find_element(By.XPATH, "./div[2]")

        size = desiredElement.size
        width = size['width']

        # Create a new ActionChains
        actions = ActionChains(driver)

        # Use move_to_element_with_offset. The offset (0, height/2) should point to the mid-height at the left side of the element.
        actions.move_to_element(desiredElement).perform()

        unn = desiredElement.find_element(By.XPATH, "./div[1]")
        plot = unn.find_element(By.XPATH, "./div[1]")

        try:
            svg = plot.find_element(By.XPATH, ".//*[name()='svg']")
            toClick = svg.find_element(By.XPATH, "(.//*[name()='g'])[last()]")
            actions.move_to_element(toClick).perform()

            cross = plot.find_element(By.XPATH, "./div[1]")
            info = cross.find_element(By.XPATH, "./div[1]")

            try:
                dateX = info.find_element("xpath", "//p[@class='date']").text
            except NoSuchElementException:
                dateX = "N/A"

            try:
                price = info.find_element("xpath", "//p[2]").text
            except NoSuchElementException:
                price = "N/A"

            p = Product(productName, dateX, price, currentPrice)
            writeToFile(str(p))

        except NoSuchElementException:
            print("SVG element not found")

    except NoSuchElementException:
        print("Button element not found")

driver.quit()  # Close the browser window
