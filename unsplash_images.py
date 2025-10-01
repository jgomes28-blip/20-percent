import requests
import os
import re
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

# Unsplash API (free, no key required for basic usage)
UNSPLASH_API = "https://api.unsplash.com/search/photos"

# Directory to save images
SAVE_DIR = "static/recipe_images"
os.makedirs(SAVE_DIR, exist_ok=True)

def extract_recipes_from_html(html_file: str = "index.html"):
    """Extract all recipe titles from your HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all recipe objects
    recipe_pattern = r'title:\s*"([^"]+)"'
    titles = re.findall(recipe_pattern, content)
    
    return titles

def get_food_image_url(recipe_name):
    """Get a food image URL from Unsplash."""
    # Clean up recipe name for better search
    search_term = recipe_name.lower()
    
    # Remove common prefixes for better search results
    search_term = search_term.replace("microwave ", "").replace("air fryer ", "").replace("oven ", "")
    
    # Map specific terms to better search terms
    search_mapping = {
        "mug": "coffee mug",
        "quesadilla": "quesadilla",
        "burrito": "burrito",
        "pizza": "pizza",
        "pasta": "pasta",
        "chicken": "chicken",
        "eggs": "scrambled eggs",
        "brownie": "brownie",
        "cake": "cake",
        "cookie": "cookie",
        "nachos": "nachos",
        "ramen": "ramen",
        "soup": "soup",
        "salad": "salad",
        "sandwich": "sandwich",
        "tacos": "tacos",
        "wings": "chicken wings",
        "ribs": "bbq ribs",
        "salmon": "salmon",
        "shrimp": "shrimp",
        "fries": "french fries",
        "hash": "hash browns",
        "toast": "toast",
        "pancake": "pancakes",
        "waffle": "waffles",
        "muffin": "muffins",
        "bagel": "bagel",
        "croissant": "croissant",
        "donut": "donuts",
        "churros": "churros",
        "s'mores": "smores",
        "fudge": "fudge",
        "cheesecake": "cheesecake",
        "nutella": "nutella",
        "marshmallow": "marshmallows"
    }
    
    # Use mapping if available, otherwise use original term
    for key, value in search_mapping.items():
        if key in search_term:
            search_term = value
            break
    
    # Add "food" to ensure we get food-related images
    search_term = f"{search_term} food"
    
    try:
        # Use Unsplash's public API (no key required for basic usage)
        params = {
            "query": search_term,
            "per_page": 1,
            "orientation": "squarish"
        }
        
        response = requests.get(UNSPLASH_API, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                image_url = data["results"][0]["urls"]["regular"]
                return image_url
        else:
            logging.warning(f"Unsplash API returned status {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error fetching image for {recipe_name}: {e}")
    
    return None

def download_image(image_url, filepath):
    """Download image from URL and save to filepath."""
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return True
    except Exception as e:
        logging.error(f"Error downloading image: {e}")
        return False

def generate_images_for_all_recipes(html_file: str = "index.html"):
    """Generate images for all recipes using Unsplash."""
    recipes = extract_recipes_from_html(html_file)
    
    logging.info(f"Found {len(recipes)} recipes to process")
    
    recipes_with_images = []
    for i, recipe_title in enumerate(recipes, 1):
        logging.info(f"Processing {i}/{len(recipes)}: {recipe_title}")
        
        # Skip if file already exists
        safe_name = "_".join(recipe_title.lower().split())[:50] + ".jpg"
        filepath = os.path.join(SAVE_DIR, safe_name)
        
        if os.path.exists(filepath):
            logging.info(f"Image already exists for {recipe_title}")
            recipes_with_images.append({"title": recipe_title, "image_path": filepath})
            continue
        
        # Get image URL from Unsplash
        image_url = get_food_image_url(recipe_title)
        
        if image_url:
            # Download the image
            if download_image(image_url, filepath):
                recipes_with_images.append({"title": recipe_title, "image_path": filepath})
                logging.info(f"✓ Success: {recipe_title}")
            else:
                logging.error(f"✗ Failed to download: {recipe_title}")
        else:
            logging.error(f"✗ Failed to find image: {recipe_title}")
        
        # Be respectful to Unsplash API
        time.sleep(1)
    
    return recipes_with_images

def update_html_with_images(recipes_with_images, html_file: str = "index.html"):
    """Update HTML file to include generated images."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create a mapping of titles to image paths
    title_to_image = {recipe["title"]: recipe.get("image_path", "") for recipe in recipes_with_images}
    
    def add_image_to_recipe(match):
        recipe_text = match.group(0)
        title_match = re.search(r'title:\s*"([^"]+)"', recipe_text)
        
        if title_match:
            title = title_match.group(1)
            image_path = title_to_image.get(title, "")
            
            if image_path and 'image:' not in recipe_text:
                # Add image property before the closing brace
                recipe_text = recipe_text.rstrip(' },') + f', image: "{image_path}" }},'
        
        return recipe_text
    
    # Pattern to match recipe objects
    recipe_pattern = r'{\s*title:\s*"[^"]+",\s*category:\s*"[^"]+",\s*method:\s*"[^"]+",\s*ingredients:\s*\[[^\]]+\],\s*steps:\s*\[[^\]]+\],\s*difficulty:\s*"[^"]+",\s*time:\s*"[^"]+"\s*},'
    
    updated_content = re.sub(recipe_pattern, add_image_to_recipe, content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    logging.info("Updated HTML file with image references")

if __name__ == "__main__":
    print("Generating images for all recipes using Unsplash...")
    all_recipes = generate_images_for_all_recipes()
    update_html_with_images(all_recipes)
    print("Done!")
