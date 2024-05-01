from flask import Flask, render_template, jsonify
import datetime as dt
import requests

app = Flask(__name__)

MY_NAME = 'Gavin "Siris" Martin'  # Defined globally for reuse in routes and/or functions

# Context processor to inject variables into all templates
@app.context_processor
def inject_globals():
    return {
        'CURRENT_YEAR': dt.datetime.now().year,
        'MY_NAME': MY_NAME
    }

@app.route('/')
@app.route('/home')
def home():
    static_posts = [
        {
            "title": "Man must explore, and this is exploration at its greatest",
            "subtitle": "Problems look mighty small from 150 miles up",
            "author": "Start Bootstrap",
            "date": dt.datetime.strptime("2023-09-24", "%Y-%m-%d").strftime("%b %d, %Y %I:%M%p")
        },
        {
            "title": "I believe every human has a finite number of heartbeats. I don't intend to waste any of mine.",
            "author": "Start Bootstrap",
            "date": dt.datetime.strptime("2023-09-18", "%Y-%m-%d").strftime("%b %d, %Y %I:%M%p")
        },
        {
            "title": "Science has not yet mastered prophecy",
            "subtitle": "We predict too much for the next year and yet far too little for the next ten.",
            "author": "Start Bootstrap",
            "date": dt.datetime.strptime("2023-08-24", "%Y-%m-%d").strftime("%b %d, %Y %I:%M%p")
        },
        {
            "title": "Failure is not an option",
            "subtitle": "Many say exploration is part of our destiny, but it’s actually our duty to future generations.",
            "author": "Start Bootstrap",
            "date": dt.datetime.strptime("2023-07-08", "%Y-%m-%d").strftime("%b %d, %Y %I:%M%p")
        }
    ]
    try:
        blog_url = "https://api.npoint.io/e52811763db21dfef489"
        blog_response = requests.get(blog_url)
        blog_response.raise_for_status()  # Ensures we proceed only if the response was successful
        api_posts = blog_response.json()
        for post in api_posts:
            post['author'] = post.get('author', 'Dr. Angela Yu')  # Default author if none specified
            try:
                formatted_date = dt.datetime.strptime(post.get('date', ''), "%Y-%m-%d").strftime("%b %d, %Y %I:%M%p")
                post['date'] = formatted_date[:-2] + formatted_date[-2:].lower()  # Convert "AM/PM" to lowercase
            except ValueError:
                post['date'] = dt.datetime.now().strftime("%b %d, %Y %I:%M%p").lower()  # Default to formatted now if parsing fails
        all_posts = static_posts + api_posts  # Combine static posts with API posts
        all_posts.sort(key=lambda x: x['date'], reverse=True)  # Sort posts by date, most recent first
    except requests.RequestException as e:
        print(f"Failed to retrieve blog data: {e}")
        all_posts = static_posts  # Use static posts if API call fails
    return render_template("index.html", posts=all_posts, page='home')

@app.route('/about')
def about():
    return render_template('about.html', page='about')

@app.route('/contact')
def contact():
    return render_template('contact.html', page='contact')

if __name__ == "__main__":
    app.run(debug=True)
