from flask import Blueprint, request, render_template
import connection
import json

posts_blueprint = Blueprint("posts_blueprint", __name__,
                            template_folder='templates')

@posts_blueprint.route('/create-post/', methods=["POST", "GET"])
def create_post():
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    if request.method == "POST":
        desc = request.form.get("desc")

        insertion_query = f"INSERT INTO posts (description) VALUES (\"{desc}\")"
        cursor.execute(insertion_query)
        cnx.commit()

        return json.dumps({"post":"created"})
    else:
        return render_template('create_post.html')
    

@posts_blueprint.route("/posts/", methods=["GET"])
def fetch_posts():
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    fetch_query = "SELECT description FROM posts"
    cursor.execute(fetch_query)
    posts = cursor.fetchall()

    return render_template('posts.html', posts=posts)