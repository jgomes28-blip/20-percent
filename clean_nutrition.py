import re
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def clean_nutrition_data(html_file: str = "index.html"):
    """Clean up existing nutrition data to have proper integer values."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def clean_nutrition_match(match):
        """Clean up a single nutrition data match."""
        full_match = match.group(0)
        nutrition_str = match.group(1)
        
        try:
            # Parse the nutrition JSON
            nutrition_data = json.loads(nutrition_str)
            
            # Clean up the values - round to reasonable precision
            cleaned_nutrition = {
                "calories": round(nutrition_data.get("calories", 0)),
                "protein": round(nutrition_data.get("protein", 0), 1),
                "carbs": round(nutrition_data.get("carbs", 0), 1),
                "fat": round(nutrition_data.get("fat", 0), 1),
                "fiber": round(nutrition_data.get("fiber", 0), 1),
                "sugar": round(nutrition_data.get("sugar", 0), 1),
                "sodium": round(nutrition_data.get("sodium", 0)),
                "servings": nutrition_data.get("servings", 1)
            }
            
            # Convert back to JSON string
            cleaned_str = json.dumps(cleaned_nutrition).replace('"', '\\"')
            
            # Replace the nutrition part in the full match
            return full_match.replace(nutrition_str, cleaned_str)
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse nutrition data: {nutrition_str}")
            return full_match
    
    # Find all nutrition data and clean it
    nutrition_pattern = r'nutrition:\s*"([^"]+)"'
    
    # Replace all nutrition data with cleaned versions
    cleaned_content = re.sub(nutrition_pattern, clean_nutrition_match, content)
    
    # Write back to file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    logging.info("Cleaned up all nutrition data in the HTML file")

def get_sample_nutrition():
    """Get a sample of current nutrition data to show the improvement."""
    
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find first few nutrition entries
    nutrition_pattern = r'nutrition:\s*"([^"]+)"'
    matches = re.findall(nutrition_pattern, content)
    
    print("Sample of current nutrition data:")
    for i, match in enumerate(matches[:3]):
        try:
            data = json.loads(match)
            print(f"\nRecipe {i+1}:")
            print(f"  Calories: {data.get('calories', 'N/A')}")
            print(f"  Protein: {data.get('protein', 'N/A')}g")
            print(f"  Carbs: {data.get('carbs', 'N/A')}g")
            print(f"  Fat: {data.get('fat', 'N/A')}g")
        except:
            print(f"  Raw data: {match}")

if __name__ == "__main__":
    print("Cleaning up nutrition data...")
    get_sample_nutrition()
    clean_nutrition_data()
    print("Done! All nutrition data has been cleaned up.")
    print("Now let's see the cleaned data:")
    get_sample_nutrition()
