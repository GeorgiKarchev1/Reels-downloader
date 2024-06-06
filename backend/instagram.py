from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import requests
import os
import logging

app = Flask(__name__)
CORS(app)

# Настройка на логването
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_driver():
    driver = None
    try:
        # Опит за инициализация на Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        logging.info("Chrome driver initialized successfully.")
    except Exception as e:
        logging.error(f"Chrome initialization failed: {e}")

    if not driver:
        try:
            # Опит за инициализация на Edge
            options = webdriver.EdgeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            logging.info("Edge driver initialized successfully.")
        except Exception as e:
            logging.error(f"Edge initialization failed: {e}")

    if not driver:
        try:
            # Опит за инициализация на Firefox
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            logging.info("Firefox driver initialized successfully.")
        except Exception as e:
            logging.error(f"Firefox initialization failed: {e}")

    if not driver:
        raise RuntimeError("No supported browsers are available.")
    
    return driver

def download_video(video_url, download_path, video_name):
    try:
        video_content = requests.get(video_url).content
        video_filename = os.path.join(download_path, video_name)
        with open(video_filename, 'wb') as video_file:
            video_file.write(video_content)
        logging.info(f"Video downloaded successfully and saved as {video_filename}")
    except Exception as e:
        logging.error(f"Error downloading video {video_name}: {e}")

def accept_cookies(driver):
    try:
        accept_button = driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]')
        accept_button.click()
        time.sleep(2)
        logging.info("Cookies accepted successfully.")
    except Exception as e:
        logging.warning(f"No cookies acceptance button found: {e}")

def click_show_more_posts(driver):
    try:
        show_more_button = driver.find_element(By.XPATH, '//button[contains(text(), "Show more posts")]')
        show_more_button.click()
        time.sleep(2)
        logging.info("Clicked 'Show more posts' button successfully.")
    except Exception as e:
        logging.warning(f"No 'Show more posts' button found: {e}")

def scroll_until_no_new_elements(driver, previous_reels):
    scroll_pause_time = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_reels = set(previous_reels)

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        reels_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/")]')
        new_reels.update([element.get_attribute('href') for element in reels_elements])
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    logging.info("Scrolled until no new elements found.")
    return list(new_reels)

def download_instagram_reels(page_url, download_path):
    logging.info(f"Starting download process for page: {page_url}")
    driver = initialize_driver()
    driver.get(page_url)
    time.sleep(5)  # Изчакай страницата да се зареди напълно
    logging.info("Page loaded successfully.")

    # Приемане на бисквитките
    accept_cookies(driver)

    # Кликване на бутона "Show more posts"
    click_show_more_posts(driver)

    # Скролирай надолу докато не спре да намира нови елементи
    all_reels = []
    all_reels = scroll_until_no_new_elements(driver, all_reels)
    logging.info(f"Found {len(all_reels)} reels.")

    for idx, reel_url in enumerate(all_reels):
        driver.get(reel_url)
        time.sleep(5)
        try:
            video_element = driver.find_element(By.TAG_NAME, 'video')
            video_url = video_element.get_attribute('src')
            video_name = f'reel_{idx + 1}.mp4'
            download_video(video_url, download_path, video_name)
        except Exception as e:
            logging.error(f"An error occurred for {reel_url}: {e}")
    
    driver.quit()
    logging.info("All reels have been downloaded successfully.")

@app.route('/download_reels', methods=['POST'])
def download_reels():
    data = request.json
    instagram_page_url = data['instagram_page_url']
    download_path = './downloads'
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    download_instagram_reels(instagram_page_url, download_path)
    return jsonify({"message": "All reels have been downloaded successfully."})

if __name__ == "__main__":
    app.run(debug=True)
