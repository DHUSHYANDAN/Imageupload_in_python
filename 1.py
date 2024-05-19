from flask import Flask, send_file
from pymongo import MongoClient
import gridfs
import io

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
fs = gridfs.GridFS(db)
# iam the project owner

# Function to upload an image to MongoDB
def upload_image(image_path, image_name):
    with open(image_path, 'rb') as image_file:
        # Delete existing image with the same filename, if it exists
        existing_image = fs.find_one({'filename': image_name})
        if existing_image:
            fs.delete(existing_image._id)
        
        # Upload the new image
        fs.put(image_file, filename=image_name)
        print(f"Image '{image_name}' uploaded successfully.")

# Function to retrieve an image from MongoDB
def retrieve_image(image_name):
    image_data = fs.find_one({'filename': image_name})
    if image_data:
        return image_data.read()
    else:
        return None

# Route to retrieve and view image
@app.route('/image/<image_name>')
def view_image(image_name):
    # Retrieve the image data from MongoDB
    retrieved_image_data = retrieve_image(image_name)
    
    # If image retrieval is successful, return the image
    if retrieved_image_data:
        return send_file(
            io.BytesIO(retrieved_image_data),
            mimetype='image/png'
        )
    else:
        return "Image not found.", 404

if __name__ == '__main__':
    # Specify the path to the new image file and its name
    new_image_path = 'O:/pythonfileupload/saran.png'
    new_image_name = 'saran.png'  # Use the same filename as the existing image
    
    # Upload the updated image
    upload_image(new_image_path, new_image_name)
    
    # Run the Flask application
    app.run(debug=True)
