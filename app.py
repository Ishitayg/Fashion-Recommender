from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('mock_fashion_data_uk_us.csv')

# Function to recommend outfits
def recommend_outfits(style_attribute, color, available_sizes, top_n=5):
    # Filter the dataset based on the given style attribute, color, and available sizes
    filtered_data = data[
        (data['Style Attributes'].str.contains(style_attribute, case=False, na=False)) &
        (data['Color'].str.contains(color, case=False, na=False)) &
        (data['Available Sizes'].apply(lambda x: any(size in x for size in available_sizes)))
    ]
    
    # Rank the filtered results based on rating and review count
    filtered_data['Rank'] = filtered_data.apply(lambda x: x['Rating'] * x['Review Count'], axis=1)
    ranked_data = filtered_data.sort_values(by='Rank', ascending=False)
    
    # Get the top N recommendations
    top_recommendations = ranked_data.head(top_n)
    
    # Select relevant columns for the recommendations
    recommendations = top_recommendations[['Product Name', 'Price', 'Brand', 'Category', 'Description', 'Rating', 'Review Count', 'Available Sizes', 'Color', 'Fashion Influencers']]
    
    return recommendations

# Route for the home page
@app.route('/')
def index():
    return render_template('index1.html')

# Route for handling form submission and displaying recommendations
@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    style_attribute = request.form['style_attribute']
    color = request.form['color']
    available_sizes = request.form.getlist('sizes')

    top_five_outfits = recommend_outfits(style_attribute, color, available_sizes)

    return render_template('recommendations.html', recommendations=top_five_outfits.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)