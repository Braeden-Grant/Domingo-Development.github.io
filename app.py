from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
import requests
from twilio.rest import Client

load_dotenv('email.env')

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_API_URL = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")

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
        try:
            name = request.form['name']
            email = request.form['email']
            website_type = request.form['website-type']
            ecommerce = request.form['ecommerce']
            physical_products = request.form['physical-products']
            pages_needed = request.form['pages-needed']
            website_needs = request.form['website-needs']
            news_section = request.form['news-section']
            contact_option = request.form['contact-option']
            portfolio = request.form['portfolio']

            sms_body = (
                f"New Contact Form Submission\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Questionnaire:\n"
                f"1. Website Type: {website_type}\n"
                f"2. E-commerce Solutions: {ecommerce}\n"
                f"3. Physical Products: {physical_products}\n"
                f"4. Pages Needed: {pages_needed}\n"
                f"5. Website Needs: {website_needs}\n"
                f"6. News Section: {news_section}\n"
                f"7. Contact Option: {contact_option}\n"
                f"8. Portfolio: {portfolio}"
            )
            
            send_sms(sms_body)
            return redirect(url_for('thank_you'))

        except KeyError as e:
            print(f"Error: {e}")
            return "Bad Request", 400

    return render_template('contact.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

def send_email(name, email, sms_body):
    smtp_server = 'localhost'
    smtp_port = 25
    msg = MIMEText(sms_body)
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

def send_sms(sms_body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=sms_body,
            from_=TWILIO_PHONE_NUMBER,
            to=MY_PHONE_NUMBER
        )
        print("SMS sent successfully!")
    except Exception as e:
        print(f"Error sending SMS: {e}")

if __name__ == '__main__':
    app.run(debug=True)
