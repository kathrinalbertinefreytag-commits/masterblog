from flask import Flask
from flask import render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

JSON_FILE = "blog_posts.json"

if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []


def fetch_post_by_id(post_id):
    """fetch post by id"""
    for post in data:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    # Open and load the JSON file
    with open('blog_posts.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Pass the posts to the template
    return render_template('index.html', posts=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """add post by title, author and content via user-input. key id incremented, if ok"""
    global data
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if data:
            new_id = max(post['id'] for post in data) + 1
        else:
            new_id = 1

        # post content will be appended to file or list
        new_post = {
            'id': new_id,
            'title': title,
            'author': author,
            'content': content,
        }

        data.append(new_post)
        with open("blog_posts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """delete post"""
    global data
    data = [post for post in data if post['id'] != post_id]


    with open("blog_posts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        with open("blog_posts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)