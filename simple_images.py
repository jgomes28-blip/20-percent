import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

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
    """Get a food image URL using direct Unsplash URLs."""
    # Clean up recipe name for better search
    search_term = recipe_name.lower()
    
    # Remove common prefixes for better search results
    search_term = search_term.replace("microwave ", "").replace("air fryer ", "").replace("oven ", "")
    
    # Map specific terms to better search terms
    search_mapping = {
        "mug": "coffee",
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
        "marshmallow": "marshmallows",
        "oatmeal": "oatmeal",
        "bacon": "bacon",
        "avocado": "avocado",
        "french toast": "french toast",
        "cinnamon roll": "cinnamon roll",
        "mac & cheese": "mac and cheese",
        "grilled cheese": "grilled cheese",
        "tomato soup": "tomato soup",
        "baked potato": "baked potato",
        "sweet potato": "sweet potato",
        "teriyaki": "teriyaki",
        "chili": "chili",
        "hot dog": "hot dog",
        "sloppy joe": "sloppy joe",
        "enchilada": "enchilada",
        "rice": "rice",
        "chocolate chip": "chocolate chip",
        "peanut butter": "peanut butter",
        "lava cake": "lava cake",
        "rice krispie": "rice krispie",
        "apple": "apple",
        "banana": "banana",
        "blueberry": "blueberry",
        "strawberry": "strawberry",
        "lemon": "lemon",
        "pumpkin": "pumpkin",
        "caramel": "caramel",
        "pineapple": "pineapple",
        "pecan": "pecan",
        "coconut": "coconut",
        "garlic": "garlic",
        "turkey": "turkey",
        "tuna": "tuna",
        "ham": "ham",
        "cheese": "cheese",
        "cauliflower": "cauliflower",
        "flatbread": "flatbread",
        "falafel": "falafel",
        "gyro": "gyro",
        "egg roll": "egg roll",
        "meatball": "meatball",
        "parmesan": "parmesan",
        "buffalo": "buffalo",
        "pork": "pork",
        "tilapia": "tilapia",
        "sausage": "sausage",
        "taquitos": "taquitos",
        "mozzarella": "mozzarella",
        "tofu": "tofu",
        "spring rolls": "spring rolls",
        "veggie": "vegetables",
        "skewers": "skewers",
        "zucchini": "zucchini",
        "pretzels": "pretzels",
        "turnovers": "turnovers",
        "shortcake": "shortcake",
        "macaroons": "macaroons",
        "granola": "granola"
    }
    
    # Use mapping if available, otherwise use original term
    for key, value in search_mapping.items():
        if key in search_term:
            search_term = value
            break
    
    # Use direct Unsplash URLs (no API key needed)
    # These are high-quality food photos from Unsplash
    image_urls = {
        "coffee": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop&crop=center",
        "quesadilla": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center",
        "burrito": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "pizza": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center",
        "pasta": "https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=400&h=400&fit=crop&crop=center",
        "chicken": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "scrambled eggs": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400&h=400&fit=crop&crop=center",
        "brownie": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "cake": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "cookie": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "nachos": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center",
        "ramen": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop&crop=center",
        "soup": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=400&fit=crop&crop=center",
        "salad": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=400&fit=crop&crop=center",
        "sandwich": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=400&fit=crop&crop=center",
        "tacos": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "chicken wings": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "bbq ribs": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "salmon": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "shrimp": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "french fries": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=400&fit=crop&crop=center",
        "hash browns": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=400&fit=crop&crop=center",
        "toast": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&h=400&fit=crop&crop=center",
        "pancakes": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center",
        "waffles": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center",
        "muffins": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "bagel": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&h=400&fit=crop&crop=center",
        "croissant": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "donuts": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "churros": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "smores": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "fudge": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "cheesecake": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "nutella": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "marshmallows": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "oatmeal": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop&crop=center",
        "bacon": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400&h=400&fit=crop&crop=center",
        "avocado": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&h=400&fit=crop&crop=center",
        "french toast": "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=400&h=400&fit=crop&crop=center",
        "cinnamon roll": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "mac and cheese": "https://images.unsplash.com/photo-1543339494-b4cd4f7ba686?w=400&h=400&fit=crop&crop=center",
        "grilled cheese": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=400&fit=crop&crop=center",
        "tomato soup": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=400&fit=crop&crop=center",
        "baked potato": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=400&fit=crop&crop=center",
        "sweet potato": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=400&fit=crop&crop=center",
        "teriyaki": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop&crop=center",
        "chili": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=400&fit=crop&crop=center",
        "hot dog": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "sloppy joe": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "enchilada": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "rice": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop&crop=center",
        "chocolate chip": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "peanut butter": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "lava cake": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "rice krispie": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "apple": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "banana": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop&crop=center",
        "blueberry": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "strawberry": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "lemon": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "pumpkin": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "caramel": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "pineapple": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "pecan": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "coconut": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "garlic": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=400&fit=crop&crop=center",
        "turkey": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=400&fit=crop&crop=center",
        "tuna": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=400&fit=crop&crop=center",
        "ham": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "cheese": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=400&fit=crop&crop=center",
        "cauliflower": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "flatbread": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "falafel": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "gyro": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "egg roll": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop&crop=center",
        "meatball": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "parmesan": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "buffalo": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "pork": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "tilapia": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "sausage": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "taquitos": "https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=400&fit=crop&crop=center",
        "mozzarella": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center",
        "tofu": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "spring rolls": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop&crop=center",
        "vegetables": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=400&fit=crop&crop=center",
        "skewers": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=400&fit=crop&crop=center",
        "zucchini": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "pretzels": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "turnovers": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "shortcake": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "macaroons": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop&crop=center",
        "granola": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=400&fit=crop&crop=center"
    }
    
    # Return the appropriate image URL
    return image_urls.get(search_term, "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=400&fit=crop&crop=center")

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
    """Generate images for all recipes using direct Unsplash URLs."""
    recipes = extract_recipes_from_html(html_file)
    
    logging.info(f"Found {len(recipes)} recipes to process")
    
    recipes_with_images = []
    for i, recipe_title in enumerate(recipes, 1):
        logging.info(f"Processing {i}/{len(recipes)}: {recipe_title}")
        
        # Get image URL
        image_url = get_food_image_url(recipe_title)
        
        if image_url:
            recipes_with_images.append({"title": recipe_title, "image_path": image_url})
            logging.info(f"✓ Success: {recipe_title}")
        else:
            logging.error(f"✗ Failed: {recipe_title}")
    
    return recipes_with_images

if __name__ == "__main__":
    print("Generating images for all recipes using direct Unsplash URLs...")
    all_recipes = generate_images_for_all_recipes()
    update_html_with_images(all_recipes)
    print("Done!")
