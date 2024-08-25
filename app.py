from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

app = Flask(__name__)

# Load the list of names from the CSV file
def load_names(csv_path):
    return pd.read_csv(csv_path)

# Check if the user's name exists in the CSV
# Check if the user's name exists in the CSV, case-insensitive and ignoring leading/trailing spaces
import re

# Check if the user's name exists in the CSV, case-insensitive and ignoring leading/trailing/multiple spaces
def check_name_exists(name, names_df):
    # Normalize the input name: strip whitespace, replace multiple spaces with a single space, and convert to lowercase
    normalized_name = re.sub(r'\s+', ' ', name.strip()).lower()

    # Normalize the 'Name' column from the CSV in the same way
    normalized_names = names_df['Name'].str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()

    # Check if the normalized name is in the list of normalized names
    return normalized_name in normalized_names.values


# Generate a certificate for the user
def generate_certificate(name, template_path, output_dir, font_path, font_size=40):
    # Load the certificate template
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    
    # Choose a font and size
    font = ImageFont.truetype(font_path, font_size)
    
    # Calculate text bounding box instead of text size
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Define the position where the name will be placed
    position = ((template.width - text_width) // 2, (template.height - text_height) // 2)
    
    # Add the name to the certificate
    draw.text(position, name, font=font, fill="black")
    
    # Save the certificate
    output_path = os.path.join(output_dir, f"{name}_certificate.png")
    template.save(output_path)
    
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['name']
        csv_path = "participants.csv"
        template_path = "certificate_template.png"
        output_dir = "certificates"
        font_path = "fonts/arial.ttf"
        
        # Create the certificates directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load names from CSV
        names_df = load_names(csv_path)
        
        # Check if the user's name exists
        if check_name_exists(user_name, names_df):
            # Generate the certificate
            certificate_path = generate_certificate(user_name, template_path, output_dir, font_path)
            return send_file(certificate_path, as_attachment=True)
        else:
            return "Name not found in the list."
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
