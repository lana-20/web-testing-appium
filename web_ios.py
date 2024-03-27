from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

APPIUM = "http://localhost:4723"

CAPS = {
    "platformName": "iOS",
    "browserName": "Safari",
    "appium:options": {
        "platformVersion": "17.4",
        "deviceName": "iPhone 15 Pro Max",
        "automationName": "XCUITest",
        "showXcodeLog": True    # optional - check the xcodebuild's log details
    }
}

OPTIONS = AppiumOptions().load_capabilities(CAPS)

driver = webdriver.Remote(
    command_executor=APPIUM,
    options=OPTIONS
)

try:
    wait = WebDriverWait(driver, 3)
    driver.get('https://the-internet.herokuapp.com')
    form_auth_link = wait.until(EC.presence_of_element_located(
        (By.LINK_TEXT, 'Form Authentication')))
    form_auth_link.click()
    username = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#username')))
    username.send_keys('tomsmith')
    password = driver.find_element(By.CSS_SELECTOR, '#password')
    password.send_keys('SuperSecretPassword!')
    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
    wait.until(EC.presence_of_element_located(
        (By.LINK_TEXT, 'Logout'))).click()
    wait.until(EC.url_to_be('https://the-internet.herokuapp.com/login'))
    flash = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#flash')))
    assert 'logged out' in flash.text
finally:
    driver.quit()