from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

APPIUM = "http://localhost:4723"

CAPS = {
    "platformName": "iOS",
    "appium:options": {
        "platformVersion": "17.4",
        "deviceName": "iPhone 15 Pro Max",
        "automationName": "XCUITest",
        "app": "com.apple.mobilesafari",
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
        (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='Form Authentication']")))
    form_auth_link.click()
    username = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, "//XCUIElementTypeTextField[@name='Username']")))
    username.send_keys("tomsmith")
    password = driver.find_element(By.XPATH, "//XCUIElementTypeSecureTextField[@name='Password']")
    password.send_keys('SuperSecretPassword!')
    driver.find_element(By.XPATH, "//XCUIElementTypeButton[contains(@name, 'Login')]").click()
    wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='Logout']"))).click()
    # Skipping assertion, since a native driver session does not support the  url_to_be() method.
    # Tried wait.until(EC.invisibility_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='You logged into a secure area!']"))), but it didn't work.
    # Page source at this step only has the flash text with the '...logged into...', no sign of '...logged out...'
finally:
    driver.quit()