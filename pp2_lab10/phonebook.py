import psycopg2
import csv

# Функция создает таблицу phonebook. Она использует команду CREATE TABLE IF NOT EXISTS, чтобы создать таблицу, если она еще не существует
def create_tables():
    """Создание таблиц в базе данных PostgreSQL."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(32) NOT NULL,
            last_name VARCHAR(32) NOT NULL,
            phone_number VARCHAR(11) NOT NULL
        )
        """,
    )
    try:
        with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Ss1234!", port= 5432) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Функция вставляет данные в таблицу. Она запрашивает имя, фамилию и номер, формирует кортеж data и выполняет команду для вставки этих данных в таблицу
def insert_data():
    """Вставка данных в таблицу."""
    data = (input("Введите имя: "), input("Введите фамилию: "), input("Введите номер телефона: "))
    command = """
        INSERT INTO phonebook(name, last_name, phone_number) 
        VALUES(%s, %s, %s)
        """
    try:
        with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Ss1234!", port= 5432) as conn:
            with conn.cursor() as cur:
                cur.execute(command, data)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Функция считывает данные из numbers.csv и вставляет их в таблицу.  Она открывает файл, читает строки CSV и выполняет SQL-команду для вставки данных из каждой строки
def from_csv():
    command = """
        INSERT INTO phonebook(name, last_name, phone_number) 
        VALUES(%s, %s, %s)
        """
    try:
        with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Ss1234!", port= 5432) as conn:
            with conn.cursor() as cur:
                with open('numbers.csv', 'r', newline='') as file:
                    rows = csv.reader(file)
                    
                    for data in rows:
                        with conn.cursor() as cur:
                            cur.execute(command, (data[0], data[1], data[2]))

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
# Функция удаляет данные на основе введенного имени. Она запрашивает имя, формирует SQL-команду для удаления данных с этим именем и выполняет эту команду
def delete_data():
    """Удаление данных из таблицы на основе имени."""
    name = input("Введите имя: ")
    
    command = """
        DELETE FROM phonebook 
        WHERE name = %s;
        """
    try:
        with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Ss1234!", port= 5432) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (name,))
                print(f"Удалено записей: {cur.rowcount}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# Функция проверяет данные в таблице и выводит их
def check_data(id: bool):
    """Удаление данных из таблицы на основе имени."""
    if id:
        command = """
            SELECT id, name, last_name, phone_number FROM phonebook ORDER BY id;
        """
    else:
        command = """
            SELECT id, name, last_name, phone_number FROM phonebook ORDER BY name;
        """
    try:
        with psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Ss1234!", port= 5432) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                print("-----------------------------------------------------")
                for data in cur.fetchall():
                    print(f"| {data[0]} | {data[1]} | {data[2]} | {data[3]} |")
                
                print(f"Удалено записей: {cur.rowcount}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

# Этот блок выполняет все функции в определенном порядке при запуске. Он создает таблицу, вставляет данные в нее, считывает данные из CSV-файла, удаляет данные на основе введенного имени, а затем выводит данные из таблицы
if __name__ == '__main__':
    create_tables()
    insert_data()
    from_csv()
    delete_data()
    check_data(True)
    
    
