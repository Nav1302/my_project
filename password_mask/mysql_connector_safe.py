import pymysql
from password_utils import get_decrypted_password

def connect_to_mysql():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password = get_decrypted_password(),
        database="test"
    )

    cursor = conn.cursor()
    cursor.execute('''
        Create table if not exists students_details(
        id int auto_increment primary key,
        Name varchar(10)
      )  
    ''')
    data = [("Alice"), ("BOB")]
    cursor.executemany("insert into students_details(Name) values(%s)", data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    connect_to_mysql()