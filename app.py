from flask import Flask,render_template,request,redirect,session
import requests
import os
from supabase_client import supabase
from dotenv import load_dotenv
from auth import auth_bp

app=Flask(__name__)
load_dotenv()

DEEPAI_KEY = os.getenv("DEEPAI_KEY")
app.secret_key=os.getenv("secret_key")
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery',methods=['GET','POST'])
def gallery():
    data=supabase.table("art_posts").select("*").execute()
    username=session.get("username")
    return render_template('gallery.html',posts=data.data,username=username)

@app.route('/mygallery', methods=['GET'])
def my_gallery():
    user_id = session.get("user_id")
    username = session.get("username")
    print(session)

    if not user_id:
        return "Unauthorized: Please log in first", 403

    # Fetch only this user's artworks
    data = (
        supabase.table("art_posts")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return render_template('mygallery.html', posts=data.data, username=username)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    load_dotenv()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['image_file']

        user_id = session.get("user_id")
        if not user_id:
            return "Unauthorized: Please log in first", 403
        
        file_bytes = file.read()
        response=requests.post("https://api.deepai.org/api/tagger",
                               files={'image':file_bytes},
                               headers={'Api-Key':DEEPAI_KEY})
        print("📦 DeepAI Response:", response.text)
        if response.status_code !=200:
            return f"Deepai API Error: {response.text}",500
        
        result=response.json()
        tags=[tag['tag'] for tag in result.get("output",{}).get("tags",[])]

        art_keywords = ["art", "painting", "drawing", "illustration", "sketch"]
        is_art = any(word.lower() in [t.lower() for t in tags] for word in art_keywords)

        if not is_art:
            return "Upload rejected: This image doesn’t look like artwork.", 400

        # Reset before uploading
        file.seek(0)

        # Unique filename
        import time
        file_path = f"{user_id}/{int(time.time())}_{file.filename}"
        bucket_name = "artworks"

        supabase.storage.from_(bucket_name).upload(file_path, file.read())
        img_url = supabase.storage.from_(bucket_name).get_public_url(file_path)

        supabase.table("art_posts").insert({
            "title": title,
            "description": description,
            "img_url": img_url,
            "user_id": user_id
        }).execute()

        return redirect('/mygallery')

    return render_template('upload.html')


if __name__=='__main__':
    app.run(debug=True)




