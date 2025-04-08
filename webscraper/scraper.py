import os
import time
import base64
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException # Import exceptions

# Keep your constants
# sample_url = "https://isbh.tmgrup.com.tr/sbh/2021/04/26/eskenar-ucgenin-alani-nasil-bulunur-eskenar-ucgen-alani-hesaplama-formulu-e1-1619438244065.png" # Unused
thumbnail_class = "YQ4gaf" # Google might change this!
# image_class = "FyHeAf" # Potentially for higher-res image after clicking, not used here
negative_class = "wA1Bge" # Class for elements to ignore
# image_search_query = "woman in wedding dress" # Query is embedded in std_url
std_url = "https://www.google.com/search?sca_esv=bb656345beb648fb&sxsrf=AHTn8zqzY6q-9Qzz22SsXJQkiUllzGbepw:1743363918682&q=person+wearing+shoes&udm=2&fbs=ABzOT_AeWVZgM1ygG9loIv1sab0j2HB687sEni7_6XgT5zHBcsCsfcGLPN4HvNuei2LApNF6Psr-0bp5SElH9XJESVvyYWqUcQ4wlYCmmPq0P1eYMZ-hHhU3dpE2BJBZcqjKWS06u12rGRHWctr1tEonBZLMQ9eAHeiMGIT4bAFbcug2q4nf48jJOJYqAPdeFweSykeOtzZ_wo6zi6Mz_eiC3Mj3nPfOaYEfSGmf80RZOr31q_zF2f2EdlmZp4GaJgCRfEnCbNhz&sa=X&ved=2ahUKEwjyjNnYyLKMAxX5RfEDHRp3CD8QtKgLegQIFRAB&biw=1920&bih=967&dpr=1"

chrome_options = Options()
chrome_options.add_argument("--headless") # Optional: Run Chrome without opening a window
# Add other options if needed (e.g., user agent)

# --- Ensure chromedriver path is correct ---
# If chromedriver is in your PATH, you might not need to specify the service path.
# Otherwise, ensure '/usr/bin/chromedriver' is the correct location.
try:
    # Try default setup first (assumes chromedriver is in PATH)
    wd = webdriver.Chrome(options=chrome_options)
except WebDriverException:
    print("WebDriver not found in PATH, trying specified service path...")
    try:
        service = Service("/usr/bin/chromedriver") # Adjust path if necessary
        wd = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        print(f"Failed to start WebDriver: {e}")
        print("Please ensure ChromeDriver is installed and its path is correct or added to your system PATH.")
        exit() # Exit if WebDriver cannot be started

def find_image_urls(wd, delay, photo_number):
    def scroll_down(wd):
        try:
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolled down.")
            time.sleep(delay)
        except WebDriverException as e:
            print(f"Error during scrolling: {e}")


    image_urls = set()
    stagnation_limit = 3 # How many scrolls with no new images before giving up
    stagnation_count = 0
    last_url_count = 0

    print(f"Attempting to navigate to URL: {std_url}")
    try:
        wd.get(std_url)
        print("Navigation successful.")
        # Optional: Add a small wait for the initial page load
        time.sleep(2)
    except WebDriverException as e:
        print(f"Error navigating to the URL: {e}")
        return image_urls # Return empty set if navigation fails

    print(f"Starting image search loop. Target: {photo_number} images.")
    while len(image_urls) < photo_number:
        scroll_down(wd)

        try:
            # Find thumbnails *after* scrolling
            thumbnails = wd.find_elements(By.CLASS_NAME, thumbnail_class)
            print(f"Found {len(thumbnails)} potential thumbnails on page.")

            # Process thumbnails found *since last check* potentially
            # A more robust way might be to process all and rely on the set for uniqueness
            # Let's stick to your original logic for now, but be aware it might re-process if elements shift
            start_index = len(image_urls) # Where we think we left off

            # Iterate through *all* found thumbnails now to be safer
            for tn in thumbnails:
                if len(image_urls) >= photo_number:
                    break # Stop if we've reached the target

                try:
                    # Check if the element is still attached to the DOM
                    # Attempt to access an attribute to trigger StaleElementReferenceException if stale
                    tn_class = tn.get_attribute('class') # Get class first
                    image_src = tn.get_attribute('src')

                    # Validate the src and class
                    if image_src and "http" in image_src and negative_class not in tn_class:
                        # Add to set (duplicates are automatically handled)
                        if image_src not in image_urls:
                           print(f"Adding new image URL: {image_src[:50]}...") # Print start of URL
                           image_urls.add(image_src)

                except WebDriverException as e: # Catch Selenium-specific errors like StaleElementReferenceException
                    print(f"Skipping a thumbnail due to WebDriverException: {e}")
                    continue # Skip this problematic thumbnail
                except Exception as e:
                    print(f"Error processing a thumbnail: {e}")
                    continue # Skip this thumbnail on other errors


            print(f"Current image count: {len(image_urls)}")

            # --- Stagnation Check ---
            if len(image_urls) == last_url_count:
                stagnation_count += 1
                print(f"No new images found on this scroll. Stagnation count: {stagnation_count}/{stagnation_limit}")
                if stagnation_count >= stagnation_limit:
                    print("Reached stagnation limit. Stopping search.")
                    break # Exit the while loop
            else:
                # Reset stagnation count if we found new images
                stagnation_count = 0
                last_url_count = len(image_urls)

            # Optional: Check for "End of results" message (might be brittle)
            # try:
            #    end_marker = wd.find_element(By.XPATH, "//*[contains(text(), 'Looks like you')]") # Example XPATH
            #    if end_marker.is_displayed():
            #        print("Reached end of results marker.")
            #        break
            # except NoSuchElementException:
            #    pass # Marker not found, continue


        except NoSuchElementException:
            print(f"Could not find elements with class name '{thumbnail_class}'. Page structure might have changed.")
            # Decide whether to break or retry
            stagnation_count += 1 # Count as stagnation
            if stagnation_count >= stagnation_limit: break
        except WebDriverException as e:
            print(f"A WebDriver error occurred during thumbnail search: {e}")
            # Decide whether to break or retry
            stagnation_count += 1 # Count as stagnation
            if stagnation_count >= stagnation_limit: break


    print(f"Finished search. Found {len(image_urls)} image URLs.")
    return image_urls


def download_image(path_to_save, url, filename):
    try:
        print(f"Attempting to download: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception if response code isn't 200

        image_content = response.content
        image_file = BytesIO(image_content)
        image = Image.open(image_file)

        # Check if image size is larger than 100x100
        if image.size[0] < 100 or image.size[1] < 100:
            print(f"Image is too small ({image.size[0]}x{image.size[1]}), skipping download.")
            return False  # Skip download if the image is too small

        # Ensure format is suitable for saving (convert if necessary)
        if image.mode == 'P':  # Palette mode might need conversion for JPEG
            image = image.convert('RGB')
        elif image.mode == 'RGBA':  # Handle transparency
            image = image.convert('RGB')  # Or save as PNG if transparency needed

        # Clean filename (basic example)
        filename_safe = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()
        image_path = os.path.join(path_to_save, filename_safe + ".jpg")  # Added .jpg extension

        # Ensure directory exists right before saving
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Save image with quality
        with open(image_path, 'wb') as file:
            image.save(file, "JPEG", quality=85)  # Specify format and optional quality
        print(f"Successfully downloaded and saved: {image_path}")
        return True  # Indicate success

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image (Request failed): {e} - URL: {url}")
    except IOError as e:  # Catch PIL/IO errors
        print(f"Error processing image data: {e} - URL: {url}")
    except Exception as e:
        print(f"An unexpected error occurred during download: {e} - URL: {url}")

    return False  # Indicate failure


if __name__ == "__main__":
    path_to_save = "shoe_raw/"
    # Create directory safely
    try:
        os.makedirs(path_to_save, exist_ok=True)
        print(f"Ensured directory exists: {path_to_save}")
    except OSError as e:
        print(f"Error creating directory {path_to_save}: {e}")
        wd.quit() # Quit driver before exiting
        exit()

    # --- Parameters ---
    TARGET_PHOTO_COUNT = 1250 # How many images to try and find
    SCROLL_DELAY = 0.6       # Increased delay slightly for more reliable loading

    found_urls = find_image_urls(wd, SCROLL_DELAY, TARGET_PHOTO_COUNT)

    # --- Download the found images ---
    download_count = 0
    if found_urls:
        print(f"\nStarting download process for {len(found_urls)} images...")
        for i, url in enumerate(found_urls):
            # Create a simple filename
            filename = f"image_{i+1}"
            if download_image(path_to_save, url, filename):
               download_count += 1
    else:
        print("No image URLs were found.")

    print(f"\nFinished. Downloaded {download_count}/{len(found_urls)} images.")

    # --- IMPORTANT: Close the browser window ---
    print("Closing WebDriver.")
    wd.quit()