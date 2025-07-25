
from flask import Flask,request,redirect,jsonify,render_template
import mysql.connector
import _hashlib
import base64

app = Flask(__name__)

db_conf ={
        'host' : "localhost",
        'user' : "root",
        'password' : "root",
        'database' : "test"
}

def get_db_connection():
    return mysql.connector.connect(**db_conf)

# This fuction to create short url

def get_shorturl(long_url):
    hash_url = _hashlib.openssl_sha256(long_url.encode())
    short_url = base64.urlsafe_b64encode(hash_url.digest())[:6].decode()
    return short_url

#serve the HTML form
@app.route('/')
def home():
    return render_template('index.html')

#Handle url shortening
@app.route('/shorten',methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')
    if not long_url:
        return "invalid URL", 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # if check URL Exists
    cursor.execute("SELECT short_url from url_mapping WHERE long_url = %s",(long_url,))
    existing_entry = cursor.fetchone()
    if existing_entry:
        conn.close()
        return f"shortened URl: <a href='{request.host_url}{existing_entry['short_url']}'>https://su/{existing_entry['short_url']}</a>"
        #return f"Shortened URL: <a href='{request.host_url}{existing_entry['short_url']}' target='_blank'>{request.host_url}{existing_entry['short_url']}</a>"

    short_url = get_shorturl(long_url)
    cursor.execute("INSERT INTO url_mapping(long_url,short_url) VALUES(%s,%s)",(long_url,short_url))
    conn.commit()
    conn.close()
    return f"shortened URl: <a href='{request.host_url}{short_url}'>https://su/{short_url}</a>"

#Redirect shorten URL
@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT long_url from url_mapping WHERE short_url = %s",(short_url,))
    entry = cursor.fetchone()
    if entry:
        cursor.execute("UPDATE url_mapping SET clicks = clicks + 1 WHERE short_url = %s",(short_url,))
        conn.commit()
        conn.close()
        return redirect(entry['long_url'])
    conn.close()
    return "Error: URL not found",404

# Run the Flask application
if __name__ == "__main__":
    app.run(debug = True)







