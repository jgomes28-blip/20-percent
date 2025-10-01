import requests
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Vheer API endpoint
API_URL = "https://vheer.com/api/v1/generate"

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

# Function to generate and save image
def generate_image(recipe_name):
    # Prepare the prompt
    prompt = f"Photorealistic image of {recipe_name}"

    # Prepare the request payload
    data = {
        "prompt": prompt,
        "style": "photorealistic",
        "aspect_ratio": "1:1"
    }

    # Set up headers (no API key needed)
    headers = {
        "Content-Type": "application/json"
    }

    # Send the request
    response = requests.post(API_URL, json=data, headers=headers)

    if response.status_code == 200:
        # Get the image URL from the response
        image_url = response.json().get("image_url")

        # Download the image
        image_data = requests.get(image_url).content
        safe_name = "_".join(recipe_name.lower().split())[:50] + ".png"
        image_path = os.path.join(SAVE_DIR, safe_name)

        with open(image_path, "wb") as f:
            f.write(image_data)
        logging.info(f"Image for '{recipe_name}' saved at {image_path}")
        return image_path
    else:
        logging.error(f"Failed to generate image for '{recipe_name}': {response.text}")
        return None

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

def generate_images_for_all_recipes(html_file: str = "index.html"):
    """Generate images for all recipes in the HTML file."""
    recipes = extract_recipes_from_html(html_file)
    
    logging.info(f"Found {len(recipes)} recipes to process")
    
    recipes_with_images = []
    for i, recipe_title in enumerate(recipes, 1):
        logging.info(f"Processing {i}/{len(recipes)}: {recipe_title}")
        
        # Generate image
        image_path = generate_image(recipe_title)
        
        recipe_data = {"title": recipe_title}
        if image_path:
            recipe_data["image_path"] = image_path
            logging.info(f"✓ Success: {recipe_title}")
        else:
            logging.error(f"✗ Failed: {recipe_title}")
        
        recipes_with_images.append(recipe_data)
    
    return recipes_with_images

if __name__ == "__main__":
    # Example: recipes stored in a list
    example_recipes = ["Spaghetti Carbonara", "Vegan Buddha Bowl", "Chicken Alfredo"]

    # Generate images for example recipes
    print("Generating images for example recipes...")
    for recipe in example_recipes:
        generate_image(recipe)

    # Or generate images for all recipes in your HTML file:
    print("\nGenerating images for all recipes in index.html...")
    all_recipes = generate_images_for_all_recipes()
    update_html_with_images(all_recipes)
    print("Done!")
