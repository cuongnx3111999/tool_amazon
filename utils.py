import sys
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from typing import Optional, Dict, Tuple
import time
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_edge(user_data_dir: str = r"C:\Users\ACER\AppData\Local\Google\Chrome\User Data",
              profile_directory: str = "profile01",
              headless: bool = False,
              load_images: bool = True,
              proxy: Optional[str] = None,
              incognito: bool = False,
              page_load_timeout: int = 30) -> webdriver.Edge:
    options = Options()
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"profile-directory={profile_directory}")
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(page_load_timeout)

    return driver


def ep_kieu(input_str: str) -> int:
    try:
        return int(float(input_str.replace('$', '').replace(',', '')) * 1000)
    except ValueError:
        logging.warning(f"Không thể chuyển đổi giá trị: {input_str}")
        return -1


def wait_and_click(driver: webdriver.Edge, selector: str, timeout: int = 10) -> None:
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )
    element.click()


def handle_one_product(driver: webdriver.Edge, user: str, password: str, msx_product: str) -> Tuple[
    str, Dict[str, int]]:
    try:
        # Step 1: Go to Amazon
        driver.get('https://www.amazon.com/')
        time.sleep(5)

        # Step 2: Clear all products in cart
        driver.get('https://www.amazon.com/gp/cart/view.html/ref=lh_cart')
        time.sleep(7)
        delete_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[data-action="delete"]')
        for button in delete_buttons:
            button.click()
            time.sleep(1)

        # Step 3: Go to specific product
        driver.get(f'https://www.amazon.com/dp/{msx_product}')
        time.sleep(5)

        # Step 4: Click "Add to Cart"
        wait_and_click(driver, '#add-to-cart-button')
        time.sleep(5)

        # Step 5: Go to cart page
        driver.get('https://www.amazon.com/gp/cart/view.html/ref=lh_cart')
        time.sleep(5)

        # Step 6: Click "Proceed to checkout"
        wait_and_click(driver, 'input[name="proceedToRetailCheckout"]')
        time.sleep(5)

        # Step 7: Login if necessary
        if 'signin' in driver.current_url:
            driver.find_element(By.CSS_SELECTOR, '#ap_password').send_keys(password)
            wait_and_click(driver, '#signInSubmit')
            time.sleep(5)

        # Step 8 & 9: Get invoice info
        invoice = {}
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#subtotals-marketplace-table'))
        )
        rows = table.find_elements(By.CSS_SELECTOR, 'tr')

        for row in rows:
            cols = row.find_elements(By.CSS_SELECTOR, 'td')
            if len(cols) < 2:
                continue
            key = cols[0].text.strip(':').lower().replace(' & ', '_').replace(' ', '_')
            value = cols[1].text
            invoice[key] = ep_kieu(value)

        return '', invoice

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return str(e), {}


def read_product_codes(filename: str) -> list[str]:
    """Đọc mã sản phẩm từ file txt."""
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"Không tìm thấy file {filename}")
        return
    except Exception as e:
        logging.error(f"Lỗi khi đọc file {filename}: {e}")
        return

if __name__ == "__main__":
    driver = init_edge()
    driver.get('https://www.amazon.com/')
    product_codes=read_product_codes('product_codes.txt')
    if not product_codes:
        logging.error('Không có mã sản phẩm nào')
        sys.exit(1)
    try:
        for msx_product in product_codes:
            error, invoice = handle_one_product(driver,
                                                os.getenv('AMAZON_USER'),
                                                os.getenv('AMAZON_PASSWORD'),
                                                msx_product)
        if error:
            logging.error(f"Error: {error}")
        else:
            logging.info(f"Invoice: {invoice}")
    finally:
        driver.quit()




