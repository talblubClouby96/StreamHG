import time
import threading
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from pyvirtualdisplay import Display
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

# List of provided links
link_list = [
    "https://cybervynx.com/9r8arlwk41xt",
    "https://cybervynx.com/b5xpdaprn4ro",
    "https://cybervynx.com/gesa9e2ib3wn",
    "https://cybervynx.com/pkj38xxkrb2v",
    "https://cybervynx.com/t4pdjbw8kgws",
    "https://cybervynx.com/56xrd4qefrt6",
    "https://cybervynx.com/9r8arlwk41xt",
    "https://cybervynx.com/x3sjo228txem",
    "https://cybervynx.com/4jabid3z04ms",
    "https://cybervynx.com/zik9lcmrfdoe",
    "https://cybervynx.com/0vs3eoyjvcmx",
]

# Randomly select 3 unique links
selected_links = random.sample(link_list, 3)

# Initialize headless display
#display = Display(visible=0, size=(1024, 768))
#display.start()

def run_browser(thread_id, url):
    while True:
        start_time = time.time()  # Track when the thread starts
        print(f"Thread-{thread_id}: Starting new browser session for {url}")

        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            ua = UserAgent()
            options.add_argument(f"user-agent={ua.random}")
            options.add_argument('--start-maximized')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')

            driver = webdriver.Chrome(options=options)

            # Disable WebDriver property in JavaScript
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # Function to randomly move the mouse safely
            def random_mouse_move():
                try:
                    window_width = driver.execute_script("return window.innerWidth;")
                    window_height = driver.execute_script("return window.innerHeight;")

                    # Get current mouse position
                    current_x, current_y = 0, 0
                    try:
                        pos_script = """
                        return {x: window.screenX + (window.outerWidth - window.innerWidth) / 2, 
                                y: window.screenY + (window.outerHeight - window.innerHeight) / 2};
                        """
                        pos = driver.execute_script(pos_script)
                        current_x, current_y = pos['x'], pos['y']
                    except:
                        pass  

                    # Move within safe bounds
                    x_offset = random.randint(-50, 50)
                    y_offset = random.randint(-50, 50)

                    new_x = max(10, min(current_x + x_offset, window_width - 10))
                    new_y = max(10, min(current_y + y_offset, window_height - 10))

                    action = ActionChains(driver)
                    action.move_by_offset(new_x - current_x, new_y - current_y).perform()
                    time.sleep(random.uniform(0.5, 1.5))  

                except WebDriverException as e:
                    print(f"Thread-{thread_id}: Mouse move error: {e}. Retrying...")
                    time.sleep(1)  

            driver.get(url)
            time.sleep(5)
            driver.save_screenshot(f"screenshot_thread{thread_id}_{time.time()}.png")

            random_mouse_move()

            while time.time() - start_time < 420:  # Run for max 7 minutes (420s)
                try:
                    play_button_xpath = '//div[@aria-label="Play"]'
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
                    play_button = driver.find_element(By.XPATH, play_button_xpath)
                    driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
                    play_button.click()

                    driver.execute_script("""
                        var playButton = document.evaluate("//div[@id='vplayer']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (playButton) {
                            playButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            setTimeout(function() { playButton.click(); }, 500);
                        }""")
                    
                    time.sleep(5)
                    driver.save_screenshot(f"screenshot_thread{thread_id}_{time.time()}.png")
                    random_mouse_move()
                    random_mouse_move()

                except Exception as e:
                    print(f"Thread-{thread_id}: Error playing video: {e}")

                    try:
                        driver.execute_script("""
                            var element = document.getElementById('vplayer');
                            var clickEvent = new MouseEvent('click', {
                              bubbles: true,
                              cancelable: true,
                              view: window
                            });
                            element.dispatchEvent(clickEvent); """)

                        try:
                            element = driver.find_element(By.XPATH, play_button_xpath)
                            actions = ActionChains(driver)
                            actions.move_to_element_with_offset(element, 5, 5).click().perform()
                            time.sleep(30)
                            driver.save_screenshot(f"screenshot_thread{thread_id}_{time.time()}.png")
                        except Exception as e:
                            print(f"Thread-{thread_id}: PyAutoGUI click failed: {e}")

                    except Exception as click_error:
                        print(f"Thread-{thread_id}: Unable to determine click coordinates: {click_error}")

                time.sleep(random.randint(10, 30))  # Wait before checking again

            print(f"Thread-{thread_id}: Max 7 minutes reached. Restarting...")
            driver.quit()
            time.sleep(random.randint(10, 30))  # Wait before restarting the thread

        except Exception as e:
            print(f"Thread-{thread_id}: Unexpected error: {e}")

        finally:
            driver.quit()
            time.sleep(random.randint(10, 30))  # Random delay before restarting the browser

# Launch 3 threads for the selected links
threads = []
for i, link in enumerate(selected_links):
    t = threading.Thread(target=run_browser, args=(i, link))
    threads.append(t)
    t.start()

# Join all threads
for t in threads:
    t.join()
