import os
import tensorflow as tf
import shutil
from PIL import Image
import numpy as np # Needed for array conversion, though tf.keras.preprocessing does it

# Suppress TensorFlow logging messages (optional)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 0 = all logs, 1 = filter INFO, 2 = filter WARNING, 3 = filter ERROR

# --- Configuration ---
TARGET_DIRECTORY = "./shoe_raw"
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff') 
CONFIDENCE_THRESHOLD = 0.1 


try:
    print("Loading MobileNetV2 model...")
    model = tf.keras.applications.MobileNetV2(weights='imagenet')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure you have tensorflow installed ('pip install tensorflow') and internet access for the first download.")
    exit()


def classify_image(image_path):
    """Loads, preprocesses, and classifies an image using the loaded model."""
    try:
        img = Image.open(image_path).convert('RGB') 
        img = img.resize((224, 224))  
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

      
        predictions = model.predict(img_array)
       
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)
        return decoded_predictions

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except UnidentifiedImageError: 
        print(f"Error: Cannot identify image file (possibly corrupted or wrong format): {image_path}")
        return None
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None


def is_wedding_related(predictions):
    """Checks if 'wedding' or 'bride' appears in the top predictions."""
    if predictions is None:
        return False


    for imagenet_id, label, score in predictions[0]:
        label_lower = label.lower()
        if ('shoe' in label_lower or 'sneaker' in label_lower or 'boot' in label_lower or 'heel' in label_lower or 'footwear' in label_lower) and ('foot' in label_lower or 'leg' in label_lower or 'worn' in label_lower):
            return True
    return False

if __name__ == "__main__":
    false_count = 0
    true_count = 0
    processed_files = 0
    skipped_files = 0

    print(f"\nScanning directory: {os.path.abspath(TARGET_DIRECTORY)}")
    print("Looking for wedding dresses or brides...")


    for root, dirs, files in os.walk(TARGET_DIRECTORY):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                image_path = os.path.join(root, file)
                print(f"\nProcessing: {image_path}")
                processed_files += 1

                predictions = classify_image(image_path)
                try:
                    if is_wedding_related(predictions):
                        true_count += 1
                        shutil.move(image_path, "shoe_raw_filtered")
                        if predictions is not None:
                            false_count += 1
                            shutil.move(image_path, "./trash")
                    else:
                        skipped_files += 1
                        shutil.move(image_path, "./trash")
                except Exception as e:
                    print(f"Error moving file {image_path}: {e}")
                    

    # --- Print Final Results ---
    print("\n--- Scan Complete ---")
    print(f"Total image files processed: {processed_files}")
    print(f"Images potentially containing a bride/wedding dress: {true_count}")
    print(f"Images likely NOT containing a bride/wedding dress: {false_count}")
    if skipped_files > 0:
        print(f"Image files skipped due to processing errors: {skipped_files}")
    print("--------------------")