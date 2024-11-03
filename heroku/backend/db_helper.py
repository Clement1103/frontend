import mysql.connector
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('database.env')

database_host = os.getenv("DATABASE_HOST")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")

global cnx
cnx = mysql.connector.connect(
    host=database_host,
    user=database_name,
    password=database_password,
    database=database_name
)

def get_next_customer_id():
    cursor = cnx.cursor()
    query = 'SELECT MAX(customer_id) FROM customers'
    cursor.execute(query)
    max_id = cursor.fetchone()[0]
    cursor.close()

    if max_id is None:
        return 1
    else:
        return max_id + 1

def format_list_of_interest(list_interests: list, dict_products: dict):
    if len(list_interests)==0:
        return '\\'
    else:
        list_formatted = []
        list_tmp = list(set(list_interests))
        for product in list_tmp:
            if product in dict_products.keys():
                list_formatted.append(str(dict_products[product]))
            else:
                list_formatted.append('Unlisted product')
    return ', '.join(list_formatted)

def get_product_ids():
    cursor = cnx.cursor()
    query = 'SELECT product_name, product_id FROM products'
    cursor.execute(query)
    result = cursor.fetchall()
    product_dict = {row[0]: row[1] for row in result}
    cursor.close()
    product_dict['\\'] = '\\'
    return product_dict

def save_to_db(user_session: dict):
    try:
        cursor = cnx.cursor()

        customer_id = get_next_customer_id()
        email = user_session.get('email')
        phone_number = user_session.get('phone')
        query = 'INSERT INTO customers (customer_id, phone_number, email_address) VALUES (%s, %s, %s)'
        cursor.execute(query, (customer_id, phone_number, email))

        date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        product_ids = get_product_ids()
        list_interest_formatted = format_list_of_interest(user_session['list_interests'], product_ids)
        query = 'INSERT INTO interests (customer_id, interests, date) VALUES (%s, %s, %s)'
        cursor.execute(query, (customer_id, list_interest_formatted, date))
        cnx.commit()
        cursor.close()

    except mysql.connector.Error as e:
        cnx.rollback()
        print("Insertion error :", e)



if __name__ == '__main__':
    print(get_next_customer_id())