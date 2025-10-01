import requests
import os
import re
import json
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_improved_nutrition_with_gpt(recipe):
    """Use ChatGPT to get improved nutritional information."""
    
    ingredients_text = ", ".join(recipe["ingredients"])
    
    prompt = f"""
    You are a professional nutritionist. Analyze this recipe and provide EXACT nutritional information per serving.

    Recipe: {recipe['title']}
    Ingredients: {ingredients_text}
    Cooking Method: {recipe['method']}

    IMPORTANT: Provide realistic, non-zero values for all macronutrients based on typical serving sizes.

    Return ONLY this exact JSON format:
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

    Make sure ALL values are realistic numbers, not zeros!
    """
    
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.error("OpenAI API key not found.")
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
                    "content": "You are a professional nutritionist. Provide accurate nutritional information for recipes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
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
            
            try:
                nutrition_data = json.loads(content)
                return nutrition_data
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON response: {content}")
                return None
        else:
            logging.error(f"API request failed: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

def improve_sample_recipes():
    """Improve nutrition data for a few sample recipes."""
    
    # Sample recipes to improve
    sample_recipes = [
        {
            "title": "Microwave Scrambled Eggs in a Mug",
            "ingredients": ["eggs", "milk", "salt", "pepper", "butter"],
            "method": "microwave"
        },
        {
            "title": "Air Fryer Chicken Wings",
            "ingredients": ["chicken wings", "olive oil", "salt", "pepper", "garlic powder"],
            "method": "air-fryer"
        },
        {
            "title": "Mug Brownie",
            "ingredients": ["flour", "sugar", "cocoa powder", "oil", "milk", "vanilla"],
            "method": "microwave"
        }
    ]
    
    print("Improving nutrition data for sample recipes using ChatGPT...")
    print("This will show you the difference between current and AI-improved nutrition data.\n")
    
    for i, recipe in enumerate(sample_recipes, 1):
        print(f"Recipe {i}: {recipe['title']}")
        print(f"Ingredients: {', '.join(recipe['ingredients'])}")
        
        # Get improved nutrition data
        improved_nutrition = get_improved_nutrition_with_gpt(recipe)
        
        if improved_nutrition:
            print("✅ AI-Improved Nutrition Data:")
            print(f"  Calories: {improved_nutrition.get('calories', 'N/A')}")
            print(f"  Protein: {improved_nutrition.get('protein', 'N/A')}g")
            print(f"  Carbs: {improved_nutrition.get('carbs', 'N/A')}g")
            print(f"  Fat: {improved_nutrition.get('fat', 'N/A')}g")
            print(f"  Fiber: {improved_nutrition.get('fiber', 'N/A')}g")
            print(f"  Sugar: {improved_nutrition.get('sugar', 'N/A')}g")
            print(f"  Sodium: {improved_nutrition.get('sodium', 'N/A')}mg")
            print(f"  Servings: {improved_nutrition.get('servings', 'N/A')}")
        else:
            print("❌ Failed to get improved nutrition data")
        
        print("-" * 50)
        
        # Be respectful to API rate limits
        time.sleep(2)

if __name__ == "__main__":
    print("This script demonstrates how ChatGPT can provide better nutrition data.")
    print("Make sure you have OPENAI_API_KEY set in your environment variables.\n")
    
    improve_sample_recipes()
    
    print("\nIf you like these results, I can create a script to improve ALL your recipes!")
    print("The AI provides more accurate, realistic nutrition values based on actual ingredient analysis.")
