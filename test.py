from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = Flask(__name__)

connection_string = "mssql+pyodbc://DESKTOP-8SL7GBI\\SQLEXPRESS/web-test?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(connection_string)

Base = declarative_base()

class YourModel(Base):
    __tablename__ = 'test'  # 数据库中的表名

    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Birthday = Column(String)
    Phone = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/get-data', methods=['GET','POST'])
def get_data():
    sql_query = "SELECT * FROM test"
    result = session.execute(text(sql_query))
    
    data = [{"ID": row.ID, "Name": row.Name, "Birthday": row.Birthday, "Phone": row.Phone} for row in result]

    return jsonify(data)

@app.route('/add-data', methods=['POST'])
def add_data():
    data = request.get_json()  # 获取前端发送的JSON数据

    # 插入数据到数据库
    new_row = YourModel(ID=data["id"], Name=data["name"], Birthday=data["birthday"], Phone=data["phone"])
    session.add(new_row)
    session.commit()
    
    # 返回成功响应
    return "Data added successfully", 200

if __name__ == '__main__':
    app.run()
