import os
from flask import Flask, request, render_template, redirect, url_for
import boto3
import io
from PIL import Image
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def load_image(image_path):
    try:
        image = Image.open(image_path)
        stream = io.BytesIO()
        image.save(stream, format="JPEG")
        return stream.getvalue()
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def load_image_from_base64(base64_string):
    try:
        image_data = base64.b64decode(base64_string.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        stream = io.BytesIO()
        image.save(stream, format="JPEG")
        return stream.getvalue()
    except Exception as e:
        print(f"Error loading image from base64: {e}")
        return None

def search_faces(image_binary):
    try:
        response = rekognition.search_faces_by_image(
            CollectionId='thubemployees',
            Image={'Bytes': image_binary}
        )
        return response['FaceMatches']
    except Exception as e:
        print(f"Error searching faces: {e}")
        return []

def get_person_name(face_id):
    try:
        face = dynamodb.get_item(
            TableName='facerecognition',
            Key={'RekognitionId': {'S': face_id}}
        )
        if 'Item' in face:
            return face['Item']['FullName']['S']
        return None
    except Exception as e:
        print(f"Error fetching person name: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                
                image_binary = load_image(file_path)
                
                if image_binary:
                    matches = search_faces(image_binary)
                    results = []
                    
                    for match in matches:
                        person_name = get_person_name(match['Face']['FaceId'])
                        confidence = match['Face']['Confidence']
                        
                        if person_name:
                            results.append(f"Found Person: {person_name} (Confidence: {confidence:.2f}%, Allowed to Use Lift)")
                    
                    if not results:
                        results.append("Person cannot be recognized")
                    
                    return render_template('index.html', results=results)
                else:
                    return render_template('index.html', results=["Failed to load image."])
        elif 'image_base64' in request.form:
            image_base64 = request.form['image_base64']
            image_binary = load_image_from_base64(image_base64)
            
            if image_binary:
                matches = search_faces(image_binary)
                results = []
                
                for match in matches:
                    person_name = get_person_name(match['Face']['FaceId'])
                    confidence = match['Face']['Confidence']
                    
                    if person_name:
                        results.append(f"Found Person: {person_name} (Confidence: {confidence:.2f}%)")
                
                if not results:
                    results.append("Person cannot be recognized")
                
                return render_template('index.html', results=results)
            else:
                return render_template('index.html', results=["Failed to load image."])
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
