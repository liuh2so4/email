import imaplib
import re
import mysql.connector
import account
from datetime import datetime

# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data

# Function to get the list of emails under this label
def get_emails(result_bytes):
    msgs = []  # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs

def parse_date(date_str):
    # Split the date string into components
    parts = date_str.split()
    
    # Get the day, month, year, time, and timezone
    day = int(parts[1])
    month = datetime.strptime(parts[2], '%b').month
    year = int(parts[3])
    time = parts[4]
    timezone = parts[5]

    # Construct and return the datetime object
    date = datetime(year, month, day)
    time_parts = time.split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    second = int(time_parts[2])
    date = date.replace(hour=hour, minute=minute, second=second)

    return date.strftime('%Y-%m-%d %H:%M:%S')

# Function to extract email data
def extract_email_data(email_text):
    # Initialize variables
    from_address = None
    subject = None
    to_address = None
    date = None
    paeks = None
    scf_peks = None
    pke_peks = None
    message = None
    plaintext = None

    # Extracting From, Subject, To, Date, PKE_PEKS, and Message
    match = re.search(r'From: (.+?)\n', email_text)
    from_address = match.group(1) if match else None

    match = re.search(r'Subject: (.+?)\n', email_text)
    subject = match.group(1) if match else None

    match = re.search(r'To: (.+?)\n', email_text)
    to_address = match.group(1) if match else None

    match = re.search(r'Date: (.+?)\n', email_text)
    if match:
        # Extract and parse date string
        date_str = match.group(1)
        date = parse_date(date_str)

    match = re.search(r'PAEKS: (.+?)\n', email_text)
    paeks = match.group(1) if match else None

    match = re.search(r'PKE_PEKS: (.+?)\n', email_text)
    pke_peks = match.group(1) if match else None

    match = re.search(r'SCF_PEKS: (.+?)\n', email_text)
    scf_peks = match.group(1) if match else None

    match = re.search(r'message: (.+?)\n', email_text)
    message = match.group(1) if match else None

    match = re.search(r'plaintext: (.+?)\n', email_text)
    plaintext = match.group(1) if match else None

    return {
        'from_address': from_address,
        'subject': subject,
        'to_address': to_address,
        'date': date,
        'paeks': paeks,
        'pke_peks': pke_peks,
        'scf_peks': scf_peks,
        'message': message,
        'plaintext': plaintext
    }

# Function to store data in MySQL
def store_in_mysql(data):
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host='localhost',
        user=account.mysqlacc(),
        password=account.mysqlpw(),
        database=account.mysqldb()
    )

    # Create a cursor
    cursor = connection.cursor()

    # Define SQL query to insert data into the table
    insert_query = """
    INSERT INTO mail (from_address, subject, to_address, date, paeks, pke_peks, scf_peks, message, plaintext)
    VALUES (%(from_address)s, %(subject)s, %(to_address)s, %(date)s, %(paeks)s, %(pke_peks)s, %(scf_peks)s, %(message)s ,%(plaintext)s)
    """

    print(data)
    # Execute the query
    cursor.execute(insert_query, data)

    # Commit changes
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    user = account.useracc()
    password = account.userpw()
    imap_url = 'imap.gmail.com'

    # Make SSL connection with Gmail
    con = imaplib.IMAP4_SSL(imap_url)

    # Log in the user
    con.login(user, password)

    # Select the Inbox
    con.select('Inbox')

    # Fetch emails from user's Gmail account
    msgs = get_emails(search('FROM', account.getacc(), con))

    # Loop through each email
    for msg in msgs[::-1]:
        for sent in msg:
            if type(sent) is tuple:
                # Decode email content and extract required information
                content = str(sent[1], 'utf-8')
                data = str(content)

                try:
                    # Extract relevant data from email
                    email_data = extract_email_data(data)

                    # Store the extracted data in MySQL
                    store_in_mysql(email_data)

                except UnicodeEncodeError as e:
                    pass
