from flask import Flask,render_template,request,redirect,session
import os
from supabase_client import supabase
from dotenv import load_dotenv
from auth import auth_bp

app=Flask(__name__)
load_dotenv()


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

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method== 'POST':
        title = request.form['title']
        description=request.form['description']
        file = request.files['image_file']

        # Save temporarily
        file_path = file.filename
        file.save(file_path)

        # Upload to Supabase Storage
        bucket_name = "artworks"
        supabase.storage.from_(bucket_name).upload(file_path, open(file_path, "rb"))

        # Get public URL
        img_url = supabase.storage.from_(bucket_name).get_public_url(file_path)


        supabase.table("art_posts").insert({
            "title": title,
            "description": description,
           "img_url": img_url
       }).execute()    

        return redirect('/')

    return render_template('upload.html')
if __name__=='__main__':
    app.run(debug=True)




