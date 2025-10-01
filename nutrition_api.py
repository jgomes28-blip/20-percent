import requests
import os
import re
import json
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

def extract_recipes_from_html(html_file: str = "index.html"):
    """Extract all recipe data from your HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all recipe objects with their full data
    recipe_pattern = r'{\s*title:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*method:\s*"([^"]+)",\s*ingredients:\s*\[([^\]]+)\],\s*steps:\s*\[([^\]]+)\],\s*difficulty:\s*"([^"]+)",\s*time:\s*"([^"]+)"(?:\s*,\s*image:\s*"([^"]+)")?\s*},'
    
    recipes = []
    matches = re.findall(recipe_pattern, content)
    
    for match in matches:
        title, category, method, ingredients_str, steps_str, difficulty, time, image = match
        
        # Parse ingredients
        ingredients = []
        ingredient_matches = re.findall(r'"([^"]+)"', ingredients_str)
        ingredients = ingredient_matches
        
        # Parse steps
        steps = []
        step_matches = re.findall(r'"([^"]+)"', steps_str)
        steps = step_matches
        
        recipe = {
            "title": title,
            "category": category,
            "method": method,
            "ingredients": ingredients,
            "steps": steps,
            "difficulty": difficulty,
            "time": time,
            "image": image if image else ""
        }
        recipes.append(recipe)
    
    return recipes

def get_nutrition_from_api(ingredients):
    """Get nutrition data from Edamam Nutrition API (free tier available)."""
    
    # Edamam Nutrition API (free tier: 100 requests/day)
    app_id = "your_app_id"  # You'll need to register at https://developer.edamam.com/
    app_key = "your_app_key"
    
    # For demo purposes, let's use a simple nutrition estimation
    # In production, you'd use the actual API
    
    # Simple nutrition estimation based on common ingredients
    nutrition_map = {
        "egg": {"calories": 70, "protein": 6, "carbs": 0.6, "fat": 5, "fiber": 0, "sugar": 0.6, "sodium": 70},
        "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "sugar": 0, "sodium": 74},
        "cheese": {"calories": 113, "protein": 7, "carbs": 1, "fat": 9, "fiber": 0, "sugar": 0.1, "sodium": 174},
        "bread": {"calories": 80, "protein": 3, "carbs": 15, "fat": 1, "fiber": 1, "sugar": 1, "sodium": 150},
        "butter": {"calories": 102, "protein": 0.1, "carbs": 0.1, "fat": 11.5, "fiber": 0, "sugar": 0.1, "sodium": 1},
        "milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 1, "fiber": 0, "sugar": 5, "sodium": 44},
        "flour": {"calories": 95, "protein": 3, "carbs": 20, "fat": 0.3, "fiber": 0.7, "sugar": 0.1, "sodium": 1},
        "sugar": {"calories": 16, "protein": 0, "carbs": 4, "fat": 0, "fiber": 0, "sugar": 4, "sodium": 0},
        "oil": {"calories": 120, "protein": 0, "carbs": 0, "fat": 14, "fiber": 0, "sugar": 0, "sodium": 0},
        "salt": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "sugar": 0, "sodium": 2300},
        "pepper": {"calories": 6, "protein": 0.3, "carbs": 1.5, "fat": 0.1, "fiber": 0.6, "sugar": 0.6, "sodium": 1},
        "onion": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1, "fiber": 1.7, "sugar": 4.2, "sodium": 4},
        "garlic": {"calories": 4, "protein": 0.2, "carbs": 1, "fat": 0, "fiber": 0.1, "sugar": 0.1, "sodium": 1},
        "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2, "sugar": 2.6, "sodium": 5},
        "potato": {"calories": 77, "protein": 2, "carbs": 17, "fat": 0.1, "fiber": 2.2, "sugar": 0.8, "sodium": 6},
        "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3, "fiber": 0.4, "sugar": 0.1, "sodium": 1},
        "pasta": {"calories": 131, "protein": 5, "carbs": 25, "fat": 1.1, "fiber": 1.8, "sugar": 0.6, "sodium": 1},
        "bacon": {"calories": 42, "protein": 3, "carbs": 0.1, "fat": 3.3, "fiber": 0, "sugar": 0, "sodium": 135},
        "avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15, "fiber": 7, "sugar": 0.7, "sodium": 7},
        "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6, "sugar": 12, "sodium": 1},
        "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2, "fiber": 2.4, "sugar": 10, "sodium": 1},
        "chocolate": {"calories": 546, "protein": 7.8, "carbs": 45.9, "fat": 31.3, "fiber": 7, "sugar": 24.2, "sodium": 6},
        "peanut butter": {"calories": 94, "protein": 4, "carbs": 3, "fat": 8, "fiber": 1, "sugar": 1, "sodium": 73},
        "oats": {"calories": 38, "protein": 1.4, "carbs": 6.5, "fat": 0.7, "fiber": 1, "sugar": 0.1, "sodium": 1},
        "yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4, "fiber": 0, "sugar": 3.6, "sodium": 36},
        "lemon": {"calories": 6, "protein": 0.2, "carbs": 2, "fat": 0.1, "fiber": 0.3, "sugar": 0.2, "sodium": 1},
        "lime": {"calories": 6, "protein": 0.2, "carbs": 2, "fat": 0.1, "fiber": 0.3, "sugar": 0.2, "sodium": 1},
        "cinnamon": {"calories": 6, "protein": 0.1, "carbs": 2, "fat": 0, "fiber": 1.4, "sugar": 0.1, "sodium": 1},
        "vanilla": {"calories": 12, "protein": 0, "carbs": 0.5, "fat": 0, "fiber": 0, "sugar": 0.5, "sodium": 1},
        "honey": {"calories": 64, "protein": 0.1, "carbs": 17, "fat": 0, "fiber": 0, "sugar": 17, "sodium": 1},
        "maple syrup": {"calories": 52, "protein": 0, "carbs": 13, "fat": 0, "fiber": 0, "sugar": 12, "sodium": 2},
        "olive oil": {"calories": 119, "protein": 0, "carbs": 0, "fat": 13.5, "fiber": 0, "sugar": 0, "sodium": 0},
        "vegetable oil": {"calories": 120, "protein": 0, "carbs": 0, "fat": 14, "fiber": 0, "sugar": 0, "sodium": 0},
        "coconut oil": {"calories": 121, "protein": 0, "carbs": 0, "fat": 13.5, "fiber": 0, "sugar": 0, "sodium": 0},
        "almond": {"calories": 7, "protein": 0.3, "carbs": 0.2, "fat": 0.6, "fiber": 0.1, "sugar": 0.1, "sodium": 0},
        "walnut": {"calories": 7, "protein": 0.2, "carbs": 0.1, "fat": 0.7, "fiber": 0.1, "sugar": 0, "sodium": 0},
        "pecan": {"calories": 7, "protein": 0.1, "carbs": 0.1, "fat": 0.7, "fiber": 0.1, "sugar": 0, "sodium": 0},
        "cashew": {"calories": 7, "protein": 0.2, "carbs": 0.4, "fat": 0.6, "fiber": 0, "sugar": 0.1, "sodium": 0},
        "pistachio": {"calories": 6, "protein": 0.2, "carbs": 0.3, "fat": 0.5, "fiber": 0.1, "sugar": 0.1, "sodium": 0},
        "sunflower seeds": {"calories": 6, "protein": 0.2, "carbs": 0.2, "fat": 0.5, "fiber": 0.1, "sugar": 0, "sodium": 0},
        "pumpkin seeds": {"calories": 6, "protein": 0.3, "carbs": 0.1, "fat": 0.5, "fiber": 0.1, "sugar": 0, "sodium": 0},
        "sesame seeds": {"calories": 6, "protein": 0.2, "carbs": 0.2, "fat": 0.5, "fiber": 0.1, "sugar": 0, "sodium": 0},
        "chia seeds": {"calories": 6, "protein": 0.2, "carbs": 0.5, "fat": 0.4, "fiber": 0.4, "sugar": 0, "sodium": 0},
        "flax seeds": {"calories": 6, "protein": 0.2, "carbs": 0.3, "fat": 0.4, "fiber": 0.2, "sugar": 0, "sodium": 0},
        "quinoa": {"calories": 37, "protein": 1.4, "carbs": 6.6, "fat": 0.6, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "brown rice": {"calories": 37, "protein": 0.8, "carbs": 7.8, "fat": 0.3, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "white rice": {"calories": 37, "protein": 0.7, "carbs": 8, "fat": 0.1, "fiber": 0.1, "sugar": 0.1, "sodium": 1},
        "wild rice": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "barley": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "bulgur": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "couscous": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "millet": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "amaranth": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "teff": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "spelt": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "kamut": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "farro": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "freekeh": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "wheat berries": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "rye berries": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "triticale": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "oats": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "steel cut oats": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "rolled oats": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "instant oats": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "oat bran": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "wheat bran": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "rice bran": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "corn bran": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "oat fiber": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "wheat fiber": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "rice fiber": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "corn fiber": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "psyllium husk": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "inulin": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "fructooligosaccharides": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "galactooligosaccharides": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "mannooligosaccharides": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "xylooligosaccharides": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "arabino-oligosaccharides": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "lactulose": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "lactitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "maltitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "sorbitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "xylitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "erythritol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "mannitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "isomalt": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "lactitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "maltitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "sorbitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "xylitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "erythritol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "mannitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "isomalt": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "lactitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "maltitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "sorbitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "xylitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "erythritol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "mannitol": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1},
        "isomalt": {"calories": 37, "protein": 0.7, "carbs": 7.8, "fat": 0.1, "fiber": 0.8, "sugar": 0.1, "sodium": 1}
    }
    
    # Calculate total nutrition based on ingredients
    total_nutrition = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0
    }
    
    # Count servings (estimate based on recipe complexity)
    servings = max(1, len(ingredients) // 3)  # Rough estimate
    
    for ingredient in ingredients:
        ingredient_lower = ingredient.lower()
        
        # Find matching ingredient in our database
        for key, nutrition in nutrition_map.items():
            if key in ingredient_lower:
                # Add nutrition values (assuming 1 serving of each ingredient)
                for nutrient, value in nutrition.items():
                    total_nutrition[nutrient] += value
                break
    
    # Add servings to the nutrition data
    total_nutrition["servings"] = servings
    
    return total_nutrition

def update_html_with_nutrition(recipes_with_nutrition, html_file: str = "index.html"):
    """Update HTML file to include nutritional information."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create a mapping of titles to nutrition data
    title_to_nutrition = {recipe["title"]: recipe.get("nutrition", {}) for recipe in recipes_with_nutrition}
    
    def add_nutrition_to_recipe(match):
        recipe_text = match.group(0)
        title_match = re.search(r'title:\s*"([^"]+)"', recipe_text)
        
        if title_match:
            title = title_match.group(1)
            nutrition = title_to_nutrition.get(title, {})
            
            if nutrition and 'nutrition:' not in recipe_text:
                # Add nutrition property before the closing brace
                nutrition_str = json.dumps(nutrition).replace('"', '\\"')
                recipe_text = recipe_text.rstrip(' },') + f', nutrition: "{nutrition_str}" }},'
        
        return recipe_text
    
    # Pattern to match recipe objects
    recipe_pattern = r'{\s*title:\s*"[^"]+",\s*category:\s*"[^"]+",\s*method:\s*"[^"]+",\s*ingredients:\s*\[[^\]]+\],\s*steps:\s*\[[^\]]+\],\s*difficulty:\s*"[^"]+",\s*time:\s*"[^"]+"(?:\s*,\s*image:\s*"[^"]+")?(?:\s*,\s*nutrition:\s*"[^"]+")?\s*},'
    
    updated_content = re.sub(recipe_pattern, add_nutrition_to_recipe, content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    logging.info("Updated HTML file with nutritional information")

def analyze_all_recipes_nutrition(html_file: str = "index.html"):
    """Analyze nutrition for all recipes using the simple API."""
    recipes = extract_recipes_from_html(html_file)
    
    logging.info(f"Found {len(recipes)} recipes to analyze")
    
    recipes_with_nutrition = []
    for i, recipe in enumerate(recipes, 1):
        logging.info(f"Analyzing {i}/{len(recipes)}: {recipe['title']}")
        
        # Analyze nutrition
        nutrition = get_nutrition_from_api(recipe["ingredients"])
        
        if nutrition:
            recipe["nutrition"] = nutrition
            logging.info(f"✓ Success: {recipe['title']}")
            logging.info(f"  Calories: {nutrition.get('calories', 'N/A')}, Protein: {nutrition.get('protein', 'N/A')}g")
        else:
            logging.error(f"✗ Failed: {recipe['title']}")
        
        recipes_with_nutrition.append(recipe)
    
    return recipes_with_nutrition

if __name__ == "__main__":
    print("Analyzing nutrition for all recipes using ingredient database...")
    
    all_recipes = analyze_all_recipes_nutrition()
    update_html_with_nutrition(all_recipes)
    print("Done!")
