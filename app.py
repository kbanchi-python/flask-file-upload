import io
import os
import string
import random

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
from flask import send_file

from config import File

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024 * 1024

UPLOAD_FOLDER = "static/images"


@app.route("/")
def index():
    search_text = request.args.get("search_text", "")
    if not search_text:
        files = File.select()
    else:
        files = File.select().where(File.name.contains(search_text))
    return render_template("index.html", files=files, search_text=search_text)


@app.route("/add", methods=["GET"])
def addFamilyGet():
    return render_template("add.html")


@app.route("/add", methods=["POST"])
def addFamilyPost():
    name = request.form["name"]
    # file = request.files["file"]
    camera = request.files["camera"]
    # file_name = str(file.filename)
    # file_path = UPLOAD_FOLDER + "/" + file_name
    # file.save(os.path.join(UPLOAD_FOLDER, file_name))
    file_name = str(camera.filename)
    file_path = UPLOAD_FOLDER + "/" + file_name
    camera.save(os.path.join(UPLOAD_FOLDER, file_name))
    File.create(name=name, file_path=file_path)
    return redirect("/")


@app.route("/delete/<id>")
def download(id):
    file = File.get(File.id == id)
    file_path = file.file_path
    os.remove(file_path)
    file.delete_instance()
    return redirect("/")


def get_random_string():
    length_of_string = 8
    return "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length_of_string)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
