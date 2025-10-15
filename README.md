# Smart Meal Planner 🍽️

A comprehensive meal planning application that helps users discover recipes across all meal types and cooking methods. Features include ingredient-based filtering, AI-powered recipe generation, nutrition tracking, and customizable color themes.

## ✨ Features

### 🍳 **Recipe Management**
- **500+ Recipes** across breakfast, lunch, dinner, and desserts
- **Multiple Cooking Methods**: Microwave, Air Fryer, Oven, No-Cook
- **Ingredient-based Filtering** with visual chips
- **Dietary Filters**: Vegan, Vegetarian, Keto, Gluten-Free, Paleo, Low-Carb, High-Protein
- **Difficulty Levels** and cooking times for each recipe

### 🤖 **AI-Powered Features**
- **Custom Recipe Generation** using OpenAI API
- **Ingredient-based Suggestions** for personalized meals
- **Smart Filtering** based on available ingredients
- **Strict Mode** to show only recipes you can fully make

### 📊 **Nutrition & Planning**
- **Detailed Nutrition Information** for each recipe
- **Macro Tracking**: Calories, Protein, Carbs, Fat, Fiber, Sugar, Sodium
- **Visual Nutrition Charts** with pie charts and progress bars
- **Weekly Meal Planner** with drag-and-drop functionality
- **Shopping List Generation** from planned meals

### 🎨 **Customization**
- **7 Color Themes**: Gold, Ocean, Forest, Sunset, Ruby, Midnight, Autumn
- **Dynamic Backgrounds** that change with theme selection
- **Persistent Theme Storage** using localStorage
- **Responsive Design** for desktop and mobile

### 🛠️ **Additional Tools**
- **Recipe Collections** for organizing favorites
- **User Account System** with login/signup
- **Share Functionality** for recipe lists
- **API Key Management** for OpenAI integration

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- OpenAI API key (optional, for AI recipe generation)

### Installation
1. Clone or download the repository
2. Open `index.html` in your web browser
3. Start exploring recipes!

### OpenAI API Setup (Optional)
1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Click "Generate Custom Recipe" button
3. Enter your API key when prompted
4. The key will be saved locally for future use

## 📱 Usage

### Navigation
- **Hamburger Menu** (☰) in top-right corner provides access to all features
- **Meal Categories**: Filter by breakfast, lunch, dinner, or desserts
- **Cooking Methods**: Choose your preferred cooking method
- **Dietary Filters**: Select dietary restrictions or preferences
- **Themes**: Access color themes from the Themes submenu

### Recipe Discovery
1. **Add Ingredients**: Type ingredients you have available
2. **Select Filters**: Choose meal type, cooking method, and dietary preferences
3. **Browse Results**: View filtered recipes with nutrition information
4. **Generate Custom**: Use AI to create recipes from your ingredients

### Meal Planning
1. **Open Meal Planner**: Use the hamburger menu to access tools
2. **Drag Recipes**: Drag recipes to meal slots for the week
3. **Generate Shopping List**: Create shopping lists from planned meals
4. **Track Nutrition**: Monitor daily macro intake

## 🎨 Color Themes

The application includes 7 beautiful color themes:

- **Gold** (Default) - Warm yellow and amber tones
- **Ocean** - Cool blue and cyan gradients
- **Forest** - Natural green and teal colors
- **Sunset** - Vibrant purple and pink hues
- **Ruby** - Bold red and orange shades
- **Midnight** - Dark theme with cyan accents
- **Autumn** - Warm orange and brown tones

Each theme changes the entire interface including backgrounds, panels, buttons, and accent colors.

## 🏗️ Technical Details

### Architecture
- **Single Page Application** built with vanilla HTML, CSS, and JavaScript
- **CSS Custom Properties** for dynamic theming
- **Local Storage** for user preferences and generated recipes
- **Responsive Design** with mobile-first approach

### Key Components
- **Recipe Database**: 500+ recipes with detailed nutrition data
- **Filter Engine**: Multi-criteria filtering system
- **Theme System**: CSS custom properties with data attributes
- **AI Integration**: OpenAI API for recipe generation
- **Nutrition Calculator**: Real-time macro tracking

### Browser Support
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📊 Recipe Database

The application includes recipes across multiple categories:

### Breakfast (50+ recipes)
- Microwave scrambled eggs, oatmeal, pancakes
- Oven-baked muffins, casseroles, hash
- Air fryer breakfast wraps, frittatas
- No-cook overnight oats, smoothies

### Lunch (40+ recipes)
- Quick microwave meals, quesadillas
- Oven-baked chicken, salmon, vegetables
- Air fryer wraps, spring rolls, tacos
- No-cook salads, sandwiches, wraps

### Dinner (60+ recipes)
- Microwave mug meals, pasta dishes
- Oven-baked proteins, roasted vegetables
- Air fryer chicken, fish, vegetables
- No-cook salads, grain bowls

### Desserts (30+ recipes)
- Microwave mug cakes, cookies
- Oven-baked pies, bars, scones
- Air fryer donuts, churros
- No-cook parfaits, energy bites

## 🔧 Customization

### Adding New Recipes
Recipes are stored in the `recipes` array in the JavaScript section. Each recipe includes:
- Title, category, cooking method
- Ingredients list
- Step-by-step instructions
- Difficulty level and cooking time
- Detailed nutrition information

### Adding New Themes
New themes can be added by:
1. Creating a new `[data-theme="name"]` CSS rule
2. Defining color variables for the theme
3. Adding a theme button to the navigation menu
4. Updating the theme initialization code

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional recipe categories
- New cooking methods
- Enhanced nutrition tracking
- More color themes
- Mobile app development
- Recipe rating system

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for AI recipe generation capabilities
- Recipe inspiration from various cooking websites and cookbooks
- CSS gradient inspiration from modern design trends
- Icon usage from Unicode emoji standards

---

**Smart Meal Planner** - Making meal planning simple, smart, and beautiful! 🍽️✨
