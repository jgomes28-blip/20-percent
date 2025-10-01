import re
import json

def clean_precision_issues(html_file: str = "index.html"):
    """Clean up floating point precision issues in nutrition data."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def clean_nutrition_match(match):
        """Clean up a single nutrition data match."""
        full_match = match.group(0)
        nutrition_str = match.group(1)
        
        try:
            # Parse the nutrition JSON
            nutrition_data = json.loads(nutrition_str)
            
            # Clean up precision issues
            cleaned_nutrition = {
                "calories": int(round(nutrition_data.get("calories", 0))),
                "protein": round(nutrition_data.get("protein", 0), 1),
                "carbs": round(nutrition_data.get("carbs", 0), 1),
                "fat": round(nutrition_data.get("fat", 0), 1),
                "fiber": round(nutrition_data.get("fiber", 0), 1),
                "sugar": round(nutrition_data.get("sugar", 0), 1),
                "sodium": int(round(nutrition_data.get("sodium", 0))),
                "servings": int(nutrition_data.get("servings", 1))
            }
            
            # Convert back to JSON string with proper escaping
            cleaned_str = json.dumps(cleaned_nutrition).replace('"', '\\"')
            
            # Replace the nutrition part in the full match
            return full_match.replace(nutrition_str, cleaned_str)
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse nutrition data: {nutrition_str}")
            return full_match
    
    # Find all nutrition data and clean precision
    nutrition_pattern = r'nutrition:\s*"([^"]+)"'
    
    # Count how many we're cleaning
    matches = re.findall(nutrition_pattern, content)
    print(f"Found {len(matches)} nutrition entries to clean")
    
    # Replace all nutrition data with cleaned versions
    cleaned_content = re.sub(nutrition_pattern, clean_nutrition_match, content)
    
    # Write back to file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print("Cleaned all nutrition precision issues!")

def show_sample_cleaned():
    """Show a sample of the cleaned nutrition data."""
    
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find first few nutrition entries
    nutrition_pattern = r'nutrition:\s*"([^"]+)"'
    matches = re.findall(nutrition_pattern, content)
    
    print("\n🎉 Sample of cleaned nutrition data:")
    print("=" * 50)
    
    for i, match in enumerate(matches[:3]):
        try:
            data = json.loads(match)
            print(f"\nRecipe {i+1}:")
            print(f"  Calories: {data.get('calories', 'N/A')}")
            print(f"  Protein: {data.get('protein', 'N/A')}g")
            print(f"  Carbs: {data.get('carbs', 'N/A')}g")
            print(f"  Fat: {data.get('fat', 'N/A')}g")
            print(f"  Fiber: {data.get('fiber', 'N/A')}g")
            print(f"  Sugar: {data.get('sugar', 'N/A')}g")
            print(f"  Sodium: {data.get('sodium', 'N/A')}mg")
            print(f"  Servings: {data.get('servings', 'N/A')}")
        except Exception as e:
            print(f"  Error parsing: {e}")

if __name__ == "__main__":
    print("Cleaning up nutrition precision issues...")
    clean_precision_issues()
    show_sample_cleaned()
    print("\n✅ Done! All nutrition data now has clean, precise values.")
    print("No more floating point precision issues like 7.199999999999999!")
