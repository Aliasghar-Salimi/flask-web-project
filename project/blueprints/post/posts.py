from flask import Blueprint, request, render_template, redirect, flash
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
        tags = request.form.getlist("tags")
        print(tags)

        desc_insertion_query = f"INSERT INTO posts (description) VALUES (\"{desc}\")"
        cursor.execute(desc_insertion_query)
        cnx.commit()

        tag_ids = []
        for tag in tags:
            fetch_tags_quary = f"SELECT id FROM the_tags WHERE name=\"{tag}\""
            cursor.execute(fetch_tags_quary)
            the_tag = cursor.fetchone()
            tag_ids.append(the_tag)
        print(tag_ids)

        fetch_post_ids = f"SELECT id FROM posts"
        cursor.execute(fetch_post_ids)
        post_ids = cursor.fetchall()
        post_id = post_ids[len(post_ids)-1:][0][0]
        print(post_id)

        for tag_id in tag_ids:
            tag_insertion_query = f"""INSERT INTO post_tag (tag_id, post_id)
                                    VALUES (\"{tag_id[0]}\", \"{post_id}\")"""
            cursor.execute(tag_insertion_query)
            cnx.commit()

        cursor.close()
        cnx.close()
        return redirect("/posts/")
    else:
        fetch_tags_quary = "SELECT id, name FROM the_tags"
        cursor.execute(fetch_tags_quary)
        tags = cursor.fetchall()

        cursor.close()
        cnx.close()
        return render_template('create_post.html', tags=tags)
    

@posts_blueprint.route("/posts/", methods=["GET"])
def fetch_posts():
    # Connecting to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)

    # Fetching the post id's and descriptions to display in the page
    fetch_post_query = "SELECT id, description FROM posts"
    cursor.execute(fetch_post_query)
    posts = cursor.fetchall()

    # Fetching the tag id's names to mathe the names with the id's in the post tag table
    fetch_tags = "SELECT id, name from the_tags"
    cursor.execute(fetch_tags)
    tags = cursor.fetchall()

    # saving the tag id's and names in a dictionary called tags
    tag_dict = {}
    for tag in tags:
        tag_dict.update({tag[0]:tag[1]})

    # extract post id's from the fetched posts to ... 
    post_ids = []
    for post in posts:
        post_ids.append(post[0])

    post_tags = {}

    for post_id in post_ids:
        # Fetching the tags related to each post
        fetch_tag_ids = f"SELECT tag_id from post_tag WHERE post_id={post_id}"
        cursor.execute(fetch_tag_ids)
        tag_ids = cursor.fetchall()
        post_tags.update({post_id:tag_ids})

    cursor.close()
    cnx.close()
    return render_template('posts.html', posts=posts, post_tags=post_tags, tag_dict=tag_dict)

@posts_blueprint.route('/delete-post/', methods=["POST"])
def delete_post():
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)


@posts_blueprint.route('/add-tag/', methods=['POST', 'GET'])
def add_tag():

    if request.method == 'POST':
        cnx = connection.connect()
        cursor = cnx.cursor(buffered=True)
        
        tag_names = request.form.get("tags")
        tag_names = tag_names.split(' ')

        print(tag_names)

        for tag in tag_names: 
            print(tag)
            tag_insertion_query = f"""INSERT INTO the_tags (name) VALUES (\"{tag}\")"""
            cursor.execute(tag_insertion_query)
            cnx.commit()

        if cursor.rowcount > 0:
            flash("tags successfully added", category='success')
            return redirect('/create-post/')
        else:
            flash("tags were not added", category='error')
            return redirect("add_tag")
    else:
        return render_template("add_tag.html")
    