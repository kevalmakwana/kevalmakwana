from flask import Flask, render_template, request, redirect
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

app.config['MYSQL_HOST'] = '10.17.50.51'
app.config['MYSQL_USER'] = 'baadalvm'
app.config['MYSQL_PASSWORD'] = 'Keval@11'
app.config['MYSQL_DB'] = 'journify_db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return redirect('/')
    try:
        # read CSV file with pandas
        df = pd.read_csv(file)
        # connect to MySQL database
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        # create MySQL table
        cursor = connection.cursor()
        # insert data into MySQL table
        for i, row in df.iterrows():
            sql = 'INSERT INTO flights_new (airline, flight_number, airline, origin, destination, day_of_week, scheduled_departure, scheduled_arrival, valid_from, valid_to) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            val = (row['airline'], row['flightNumber'], row['origin'], row['destination'], row['daysOfWeek'], row['scheduledDepartureTime'], row['scheduledArrivalTime'], row['validFrom'], row['validTo'])
            cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect('/')
    except Error as e:
        print('Error:', e)
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
