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

def analyze_nutrition_with_ai(recipe):
    """Use OpenAI API to analyze nutrition based on ingredients."""
    
    # Create a detailed prompt for nutrition analysis
    ingredients_text = ", ".join(recipe["ingredients"])
    
    prompt = f"""
    Analyze the nutritional content of this recipe and provide accurate macronutrient information.

    Recipe: {recipe['title']}
    Ingredients: {ingredients_text}

    Please provide the nutritional information per serving in this exact JSON format:
    {{
        "calories": number,
        "protein": number (in grams),
        "carbs": number (in grams),
        "fat": number (in grams),
        "fiber": number (in grams),
        "sugar": number (in grams),
        "sodium": number (in mg),
        "servings": number
    }}

    Guidelines:
    - Estimate realistic serving sizes based on the recipe
    - Consider typical ingredient quantities (assume standard measurements if not specified)
    - Provide accurate macronutrient breakdown
    - Round numbers to reasonable precision
    - If ingredients are vague, make reasonable assumptions

    Return ONLY the JSON object, no other text.
    """
    
    try:
        # Use OpenAI API for nutrition analysis
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
                    "content": "You are a nutrition expert. Analyze recipes and provide accurate nutritional information in JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
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
                return nutrition_data
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON response for {recipe['title']}")
                return None
        else:
            logging.error(f"API request failed for {recipe['title']}: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error analyzing nutrition for {recipe['title']}: {e}")
        return None

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
    """Analyze nutrition for all recipes."""
    recipes = extract_recipes_from_html(html_file)
    
    logging.info(f"Found {len(recipes)} recipes to analyze")
    
    recipes_with_nutrition = []
    for i, recipe in enumerate(recipes, 1):
        logging.info(f"Analyzing {i}/{len(recipes)}: {recipe['title']}")
        
        # Analyze nutrition
        nutrition = analyze_nutrition_with_ai(recipe)
        
        if nutrition:
            recipe["nutrition"] = nutrition
            logging.info(f"✓ Success: {recipe['title']}")
            logging.info(f"  Calories: {nutrition.get('calories', 'N/A')}, Protein: {nutrition.get('protein', 'N/A')}g")
        else:
            logging.error(f"✗ Failed: {recipe['title']}")
        
        recipes_with_nutrition.append(recipe)
        
        # Be respectful to API rate limits
        time.sleep(1)
    
    return recipes_with_nutrition

if __name__ == "__main__":
    print("Analyzing nutrition for all recipes...")
    print("Make sure you have OPENAI_API_KEY set in your environment variables.")
    
    all_recipes = analyze_all_recipes_nutrition()
    update_html_with_nutrition(all_recipes)
    print("Done!")
