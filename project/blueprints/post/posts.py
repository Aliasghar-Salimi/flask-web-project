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
    # Connecting to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    # Fetching the post id's and descriptions to display in the page
    fetch_query = "SELECT id, description FROM posts"
    cursor.execute(fetch_query)
    posts = cursor.fetchall()

    # Fetching the categroy id's names to mathe the names with the id's in the post tag table
    fetch_tagNames = "SELECT id, name from categories"
    cursor.execute(fetch_tagNames)
    tags = cursor.fetchall()

    # saving the category id's and names in a dictionary called categories
    categories = {}
    for tag in tags:
        categories.update({tag[0]:tag[1]})
    print("category id and names => "+str(categories))

    # extract post id's from the fetched posts to ... 
    post_ids = []
    for post in posts:
        post_ids.append(post[0])
    
    print("post ids => "+str(post_ids)+"\n")
    
    tags = []
    post_tags = {}

    for post_id in post_ids:
        # Fetching the tags related to each post
        fetch_categories = f"SELECT cat_id from post_tag WHERE post_id={post_id}"
        cursor.execute(fetch_categories)
        the_tags = cursor.fetchall()
        post_tags.update({post_id:the_tags})

    print(post_tags.keys())
    for post_id in post_tags:
        for ids in post_tags[post_id]:
            for category in categories:
                if category == ids[0]:
                    print(categories[category])

    return render_template('posts.html', posts=posts, post_tags=post_tags, categories=categories)