from flask import Flask, render_template

app = Flask(__name__)

# Render the homepage
@app.route('/')
def home():
    return render_template('homepage.html')

# Render Page 1
@app.route('/sentMail')
def page1():
    return render_template('sentpage.html')

# Render Page 2
# @app.route('/mailbox')
# def page2():
#     return render_template('mailbox.html')

# Render Page 3
@app.route('/homepage')
def page3():
    return render_template('homepage.html')

####################################################################################################################################################

from flask import request
from flask_mail import Mail, Message
import account
import keyFeature.lib.PAEKS.paeks as pak
import keyFeature.lib.PKE.pke as pke
import keyFeature.lib.SCF.scf as scf

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
#update it with your gmail
app.config['MAIL_USERNAME'] = account.getacc()
#update it with your password
app.config['MAIL_PASSWORD'] = account.getpw()
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#default
messages = ["PAEKS", "PKE_PEKS", "SCF_PEKS", "message", "plaintext"]
pak.setup()
pke.setup()
scf.setup()
text = "This is a test mail."

@app.route("/sent", methods=["GET", "POST"])
def sent():
    if request.method == "POST":
        receiver = request.form.get('receiver')
        purpose = request.form.get('purpose')
        keyword = request.form.get('keyword')
        text = request.form.get('text')
        sigma = ""
        key = ["", "", ""]
        if keyword == "paeks":
            pak.certificate(messages[0])
            key[0] = messages[0]
        if keyword == "pke":
            sigma = pke.getCyphertext(messages[1], text)
            key[1] = messages[1]
        if keyword == "scf":
            scf.certificate(messages[2])
            key[2] = messages[2]
        msg = Message(purpose, sender="noreply@demo.com", recipients=[account.getacc(), receiver])
        msg.body = messages[0] + ": " + key[0] + "\n" + messages[1] + ": " + key[1] + "\n" + messages[2] + ": " + key[2] + "\n" + messages[3] + ": " + sigma + "\n" + messages[4] + ": " + text + "\n"
        mail.send(msg)
        return render_template('resetpage.html')
    return render_template('sentpage.html')

@app.route('/reset', methods=['GET', "POST"])
def reset_page():
    if request.method == "POST":
        return render_template('sentpage.html')
    return render_template('resetpage.html')

####################################################################################################################################################

import mysql.connector

# Function to fetch emails from MySQL database
def fetch_emails_from_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=account.mysqlacc(),
            password=account.mysqlpw(),
            database=account.mysqldb()
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mail")  # Adjust the SQL query based on your table structure
        emails = cursor.fetchall()
        cursor.close()
        connection.close()
        return emails
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return []

@app.route('/mailbox')
def index():
    # Fetch emails from the database
    emails = fetch_emails_from_database()
    return render_template('mailbox.html', emails=emails)

@app.route('/search')
def search():
    keyword = request.args.get('keyword')

    key = ""
    if keyword == "paeks":
        key = messages[0]
    if keyword == "pke":
        key = messages[1]
    if keyword == "scf":
        key = messages[2]
    key = key + "\r"

    emails = fetch_emails_from_database()
    search_result = []
    for email in emails:
        # print(email.get("paeks"), email.get("pke_peks"), email.get("scf_peks"))
        if (email.get("paeks") == key):
            pak_test = pak.getSearchMail(key)
            if (pak_test == 1):
                search_result.append(email)

        # Perform search logic here using database query
        if (email.get("pke_peks") == key):
            pke_test = pke.getSearchMail(key)
            if (pke_test == 1):
                search_result.append(email)
                pke.pke_dec(email.get("message"))

        if (email.get("scf_peks") == key):
            scf_test = scf.getSearchMail(key)
            print(scf_test)
            if (scf_test == 1):
                search_result.append(email)
    
    print(search_result)
    return render_template('mailbox.html', emails=search_result)
    
####################################################################################################################################################

if __name__ == '__main__':
    app.run(debug=True)
