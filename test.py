from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

connection_string = "mssql+pyodbc://DESKTOP-8SL7GBI\\SQLEXPRESS/web-test?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/get-data', methods=['GET','POST'])
def get_data():

    sql_query = "SELECT * FROM test"
    result = session.execute(text(sql_query))


    data = [{"ID": row.ID, "Name": row.Name, "Birthday": row.Birthday, "Phone": row.Phone} for row in result]


    return jsonify(data)

if __name__ == '__main__':
    app.run()
