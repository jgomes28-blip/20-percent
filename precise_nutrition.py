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
    
    # Find all recipe objects with their full data (JavaScript object syntax)
    recipe_pattern = r'{\s*title:\s*"([^"]+)",\s*category:\s*"([^"]+)",\s*method:\s*"([^"]+)",\s*ingredients:\s*\[([^\]]+)\],\s*steps:\s*\[([^\]]+)\],\s*difficulty:\s*"([^"]+)",\s*time:\s*"([^"]+)"(?:\s*,\s*image:\s*"([^"]+)")?(?:\s*,\s*nutrition:\s*"([^"]+)")?\s*},'
    
    recipes = []
    matches = re.findall(recipe_pattern, content)
    
    for match in matches:
        title, category, method, ingredients_str, steps_str, difficulty, time, image, nutrition = match
        
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
            "image": image if image else "",
            "nutrition": nutrition if nutrition else ""
        }
        recipes.append(recipe)
    
    return recipes

def get_precise_nutrition_with_gpt(recipe):
    """Use ChatGPT to get precise nutritional information based on ingredients and quantities."""
    
    # Create a detailed prompt for precise nutrition analysis
    ingredients_text = ", ".join(recipe["ingredients"])
    
    prompt = f"""
    You are a professional nutritionist. Analyze this recipe and provide EXACT nutritional information per serving.

    Recipe: {recipe['title']}
    Ingredients: {ingredients_text}
    Cooking Method: {recipe['method']}

    IMPORTANT INSTRUCTIONS:
    1. Estimate realistic serving sizes based on the recipe (typically 1-2 servings for mug recipes, 2-4 for larger recipes)
    2. Calculate precise macronutrient values based on typical ingredient quantities
    3. Consider cooking method (microwave, air fryer, oven) affects on nutrition
    4. Use standard USDA nutrition data for ingredients
    5. Provide realistic, non-zero values for all macronutrients

    Return ONLY this exact JSON format (no other text):
    {{
        "calories": [exact number],
        "protein": [exact number in grams],
        "carbs": [exact number in grams],
        "fat": [exact number in grams],
        "fiber": [exact number in grams],
        "sugar": [exact number in grams],
        "sodium": [exact number in mg],
        "servings": [realistic serving count]
    }}

    EXAMPLES OF REALISTIC VALUES:
    - Microwave scrambled eggs: ~150 calories, ~12g protein, ~2g carbs, ~10g fat
    - Air fryer chicken wings: ~250 calories, ~25g protein, ~0g carbs, ~15g fat
    - Mug brownie: ~300 calories, ~4g protein, ~35g carbs, ~15g fat
    - Grilled cheese: ~400 calories, ~15g protein, ~30g carbs, ~25g fat

    Make sure ALL values are realistic numbers, not zeros!
    """
    
    try:
        # Use OpenAI API for precise nutrition analysis
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
            return None
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional nutritionist with access to USDA nutrition database. Provide accurate nutritional information for recipes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,  # Low temperature for consistent results
            "max_tokens": 300
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            
            # Try to parse the JSON response
            try:
                nutrition_data = json.loads(content)
                
                # Validate that we got realistic values
                if (nutrition_data.get("calories", 0) > 0 and 
                    nutrition_data.get("protein", 0) >= 0 and 
                    nutrition_data.get("carbs", 0) >= 0 and 
                    nutrition_data.get("fat", 0) >= 0):
                    return nutrition_data
                else:
                    logging.warning(f"Got unrealistic values for {recipe['title']}: {nutrition_data}")
                    return None
                    
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON response for {recipe['title']}: {content}")
                return None
        else:
            logging.error(f"API request failed for {recipe['title']}: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error analyzing nutrition for {recipe['title']}: {e}")
        return None

def update_html_with_precise_nutrition(recipes_with_nutrition, html_file: str = "index.html"):
    """Update HTML file to include precise nutritional information."""
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
            elif nutrition and 'nutrition:' in recipe_text:
                # Update existing nutrition data
                nutrition_str = json.dumps(nutrition).replace('"', '\\"')
                recipe_text = re.sub(r'nutrition:\s*"[^"]*"', f'nutrition: "{nutrition_str}"', recipe_text)
        
        return recipe_text
    
    # Pattern to match recipe objects
    recipe_pattern = r'{\s*title:\s*"[^"]+",\s*category:\s*"[^"]+",\s*method:\s*"[^"]+",\s*ingredients:\s*\[[^\]]+\],\s*steps:\s*\[[^\]]+\],\s*difficulty:\s*"[^"]+",\s*time:\s*"[^"]+"(?:\s*,\s*image:\s*"[^"]+")?(?:\s*,\s*nutrition:\s*"[^"]+")?\s*},'
    
    updated_content = re.sub(recipe_pattern, add_nutrition_to_recipe, content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    logging.info("Updated HTML file with precise nutritional information")

def analyze_all_recipes_precise_nutrition(html_file: str = "index.html"):
    """Analyze nutrition for all recipes using ChatGPT for precise values."""
    recipes = extract_recipes_from_html(html_file)
    
    logging.info(f"Found {len(recipes)} recipes to analyze")
    
    recipes_with_nutrition = []
    successful_count = 0
    
    for i, recipe in enumerate(recipes, 1):
        logging.info(f"Analyzing {i}/{len(recipes)}: {recipe['title']}")
        
        # Analyze nutrition with ChatGPT
        nutrition = get_precise_nutrition_with_gpt(recipe)
        
        if nutrition:
            recipe["nutrition"] = nutrition
            successful_count += 1
            logging.info(f"✓ Success: {recipe['title']}")
            logging.info(f"  Calories: {nutrition.get('calories', 'N/A')}, Protein: {nutrition.get('protein', 'N/A')}g, Carbs: {nutrition.get('carbs', 'N/A')}g, Fat: {nutrition.get('fat', 'N/A')}g")
        else:
            logging.error(f"✗ Failed: {recipe['title']}")
        
        recipes_with_nutrition.append(recipe)
        
        # Be respectful to API rate limits
        time.sleep(2)  # 2 second delay between requests
    
    logging.info(f"Successfully analyzed {successful_count}/{len(recipes)} recipes")
    return recipes_with_nutrition

if __name__ == "__main__":
    print("Analyzing nutrition for all recipes using ChatGPT for precise values...")
    print("Make sure you have OPENAI_API_KEY set in your environment variables.")
    print("This will take several minutes due to API rate limits.")
    
    all_recipes = analyze_all_recipes_precise_nutrition()
    update_html_with_precise_nutrition(all_recipes)
    print("Done! All recipes now have precise nutritional information.")
