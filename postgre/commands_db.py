import random

import psycopg2


def connect_bd():
    connect = psycopg2.connect(dbname='postgres', user='postgres1',
                               password='postgres1', host="localhost")
    return connect


def create_table_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS users' \
          ' (ID BIGINT NOT NULL,' \
          ' first_name VARCHAR(200) DEFAULT NULL,' \
          ' username VARCHAR(200) DEFAULT NULL,' \
          ' active BOOL DEFAULT TRUE,' \
          ' created_at timestamp DEFAULT NOW(),' \
          ' updated_at timestamp DEFAULT NOW());'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully")

def create_table_answers():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS answers' \
          ' (ID serial PRIMARY KEY,' \
          ' login_from_user VARCHAR(200) DEFAULT NULL,' \
          ' logim_about_user VARCHAR(200) DEFAULT NULL,' \
          ' text text,' \
          ' created_at timestamp DEFAULT NOW(),' \
          ' updated_at timestamp DEFAULT NOW());'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully")



def drop_table(name_table):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f'DROP TABLE {name_table};'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table drop")


def add_user(id_user, first_name=None, username=None):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"INSERT INTO users (id, first_name, username)" \
          f" VALUES ({id_user}, '{first_name}', '{username}');"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("User append")

def select_all_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, first_name, username, active FROM users"
    cursor.execute(sql)
    all_users = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_users

def select_all_active_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, first_name, username, active FROM users WHERE active=True"
    cursor.execute(sql)
    all_users = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_users


def select_user(id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, first_name, username, active FROM users where id = {id}"
    cursor.execute(sql)
    user = cursor.fetchall()
    connect.commit()
    connect.close()
    return user

def update_active_user(id):
    connect = connect_bd()
    cursor = connect.cursor()
    cursor.execute(f'SELECT id, active FROM users WHERE id={id}')
    user = cursor.fetchall()
    if user[0][1] == True:
        cursor.execute(f'UPDATE users SET active=FALSE WHERE id={id}')
    else:
        cursor.execute(f'UPDATE users SET active=TRUE WHERE id={id}')
    connect.commit()
    connect.close()
    print(f'Change active user {id}')
    return user

def create_new_answer(login_from_user, logim_about_user, text):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"INSERT INTO answers (login_from_user, logim_about_user, text)" \
          f" VALUES ({login_from_user}, {logim_about_user}, '{text}');"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Answer append")


if __name__ == '__main__':
    print('db commands')


    # drop_table('users')
    # drop_table('answers')
    create_table_answers()
    # create_new_answer(354585871, 1908289217, 'gfhvfdfkjdhfkjj sdlkf jdlkfjlskdjf lksjf sldf')
    create_table_users()
    # add_user(354585871, 'Дмитрий', 'DmKusov')
    # add_user(485696536, 'Олег', 'Valeznik')
    # add_user(342857621, 'Елена', 'Elena_kusova')
    # add_user(1075946634, 'Владимир', 'vywakov')

    # all_us = select_all_users()
    # all_act_us = select_all_active_users()
    # print(all_act_us)
    # print(random.choice(all_act_us))
    # for ell in all_us:
    #     print(ell)

    # print('Before')
    # user = select_user(2)
    # print(user)
    # print('Update')
    # update_active_user(2)
    # update_active_user(1)
    # print('After')
    # user = select_user(2)
    # print(user)
