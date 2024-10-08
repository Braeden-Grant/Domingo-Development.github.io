from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
import requests

load_dotenv('email.env')

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_API_URL = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'

reviews = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    response = requests.get(GITHUB_API_URL)
    projects = []

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            projects.append({
                'name': repo['name'],
                'description': repo['description'],
                'url': repo['html_url'],
                'image': 'DomingoDev.png'
            })

    return render_template('portfolio.html', projects=projects)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews_page():
    if request.method == 'POST':
        name = request.form['name']
        review = request.form['review']
        reviews.append({'name': name, 'review': review})
    return render_template('reviews.html', reviews=reviews)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email(name, email, message)
        return redirect(url_for('thank_you'))
    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

def send_email(name, email, message):
    smtp_server = 'localhost'
    smtp_port = 25
    msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = "New Contact Form Submission"
    msg['From'] = 'Domingo.Dev@example.local'
    msg['To'] = 'braedengrant0@gmail.com'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    app.run(debug=True)
