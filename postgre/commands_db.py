import os
import random

import psycopg2
from dotenv import load_dotenv


load_dotenv()
def connect_bd():
    connect = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                               password=os.getenv("DB_PASSWORD"), host=os.getenv("HOST"), port='5432')
    return connect


def create_table_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS users' \
          ' (ID BIGINT NOT NULL PRIMARY KEY,' \
          ' first_name VARCHAR(200) DEFAULT NULL,' \
          ' username VARCHAR(200) DEFAULT NULL,' \
          ' is_active BOOL DEFAULT TRUE,' \
          ' is_free BOOL DEFAULT TRUE,' \
          ' created_at timestamp DEFAULT NOW(),' \
          ' updated_at timestamp DEFAULT NOW());'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully --> create_table_users")


def create_table_images():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS images' \
          ' (id serial PRIMARY KEY,' \
          ' photo_id text,' \
          ' created_at timestamp DEFAULT NOW())'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully --> create_table_images")


def create_table_rating():
    """id_user - кому балл ставится
       from_user - кто ставит балл"""
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS rating' \
          ' (id serial PRIMARY KEY,' \
          ' id_user BIGINT,' \
          ' from_user BIGINT DEFAULT 0,' \
          ' points INT DEFAULT 1,' \
          ' created_at timestamp DEFAULT NOW(),' \
          ' updated_at timestamp DEFAULT NOW());'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully --> create_table_rating")

def select_stat_rating_users(start_month, end_month):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id_user" \
          f" FROM rating" \
          f" WHERE " \
          f"updated_at>='{start_month}' AND " \
          f"updated_at<='{end_month}';"
    cursor.execute(sql)
    result_rating = cursor.fetchall()
    result_rating2 = []
    for rait_us in result_rating:
        result_rating2.append(rait_us[0])
    connect.commit()
    connect.close()
    return result_rating2

def select_all_stat_rating_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id_user" \
          f" FROM rating;"
    cursor.execute(sql)
    result_rating = cursor.fetchall()
    result_rating3 = []
    for rait_us in result_rating:
        result_rating3.append(rait_us[0])
    connect.commit()
    connect.close()
    return result_rating3
def add_rating(id_user, from_user=0):
    """id_user - кому балл ставится
           who_from_user - кто ставит балл"""
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"INSERT INTO rating (id_user, from_user)" \
          f" VALUES ({id_user}, {from_user});"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("add_rating --> done")


def append_image(photo_id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"INSERT INTO images (photo_id)" \
          f" VALUES ('{photo_id}');"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("add_image --> done")

def select_all_photos(start_month, end_month):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, photo_id FROM images WHERE " \
          f"created_at>'{start_month}' AND " \
          f"created_at<'{end_month}';"
    cursor.execute(sql)
    all_photo = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_photo

def create_table_answers():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS answers' \
          ' (ID serial PRIMARY KEY,' \
          ' login_from_user VARCHAR(200) DEFAULT NULL,' \
          ' login_about_user VARCHAR(200) DEFAULT NULL,' \
          ' text text,' \
          ' created_at timestamp DEFAULT NOW(),' \
          ' updated_at timestamp DEFAULT NOW());'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully")

def create_table_meetings():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS meetings' \
          ' (ID serial PRIMARY KEY,' \
          ' id_from_user BIGINT,' \
          ' id_about_user BIGINT,' \
          ' confirmed_meeting BOOL DEFAULT FALSE,' \
          ' meeting_end BOOL DEFAULT FALSE,' \
          ' days_left_end INT DEFAULT 7,' \
          ' txt_about_place text,' \
          ' txt_about_people text,' \
          ' is_active BOOL DEFAULT TRUE, ' \
          ' created_at timestamp DEFAULT NOW(),' \
          ' updated_at timestamp DEFAULT NOW());'
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Table created successfully")

def select_all_result_meet_month(start_month, end_month):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id," \
          f" id_from_user," \
          f" id_about_user," \
          f" confirmed_meeting," \
          f" meeting_end" \
          f" FROM meetings WHERE " \
          f"meeting_end=TRUE AND " \
          f"updated_at>='{start_month}' AND " \
          f"updated_at<='{end_month}';"
    cursor.execute(sql)
    meetings_all = cursor.fetchall()
    connect.commit()
    connect.close()
    return meetings_all

def select_result_meet_month_for_user(user_id, start_month, end_month):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id," \
          f" id_from_user," \
          f" id_about_user," \
          f" confirmed_meeting," \
          f" meeting_end" \
          f" FROM meetings WHERE " \
          f"id_from_user={user_id} AND " \
          f"meeting_end=TRUE AND " \
          f"updated_at>='{start_month}' AND " \
          f"updated_at<='{end_month}';"
    cursor.execute(sql)
    meetings_all = cursor.fetchall()
    connect.commit()
    connect.close()
    return meetings_all



# def db_confirm_invite(id_from_user, id_about_user):
#     connect = connect_bd()
#     cursor = connect.cursor()
#     sql = f"UPDATE meetings SET confirmed_invite=True, days_left_end=7" \
#           f"WHERE id_from_user={id_from_user} AND " \
#           f"id_about_user={id_about_user} AND " \
#           f"meeting_end=False AND " \
#           f"confirmed_meeting=False;"
#     cursor.execute(sql)
#     connect.commit()
#     connect.close()
#     print("db_confirm_invite Update")

def db_confirm_meeting(id_from_user, id_about_user):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET confirmed_meeting=True, days_left_end=7 " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"meeting_end=False AND " \
          f"is_active=TRUE;"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("db_confirm_invite Update")

def select_one_meeting_confirm_or_not(id_from_user, id_about_user):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT confirmed_meeting FROM meetings " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=True;"
    cursor.execute(sql)
    result_confirm = cursor.fetchall()
    connect.commit()
    connect.close()
    return result_confirm

def db_done_meeting(id_from_user, id_about_user):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET meeting_end=True, days_left_end=0 " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=True;"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("db_done_meeting Update")

def add_text_place_to_meeting(id_from_user, id_about_user, text):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET txt_about_place=\'{text}\' " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=True;"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("add_text_to_meeting Update")

def add_text_about_user_to_meeting(id_from_user, id_about_user, text):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET txt_about_people=\'{text}\' " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=True;"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("add_text_to_meeting Update")

def db_finish_meeting(id_from_user, id_about_user):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET is_active=False " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=True AND " \
          f"days_left_end=0 AND " \
          f"confirmed_meeting=TRUE;"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("add_text_to_meeting Update")

def select_active_meetings():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id, " \
          f"id_from_user," \
          f" id_about_user," \
          f" confirmed_meeting," \
          f" meeting_end," \
          f" days_left_end," \
          f" is_active  FROM meetings WHERE " \
          f"is_active=TRUE AND " \
          f"days_left_end>0 AND " \
          f"meeting_end=FALSE AND " \
          f"confirmed_meeting=FALSE;"
    cursor.execute(sql)
    all_act_meet = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_act_meet

def select_is_active_meeting(id_from_user, id_about_user):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id, " \
          f"id_from_user," \
          f" id_about_user," \
          f" confirmed_meeting," \
          f" meeting_end," \
          f" days_left_end," \
          f" is_active  FROM meetings WHERE " \
          f"id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=TRUE;"
    cursor.execute(sql)
    is_act_meet = cursor.fetchall()
    connect.commit()
    connect.close()
    return is_act_meet

def select_active_meeting_after_confirmed():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT" \
          f" id, " \
          f"id_from_user," \
          f" id_about_user," \
          f" confirmed_meeting," \
          f" meeting_end," \
          f" days_left_end," \
          f" is_active  FROM meetings WHERE " \
          f"is_active=TRUE AND " \
          f"days_left_end>0 AND " \
          f"meeting_end=FALSE AND " \
          f"confirmed_meeting=TRUE;"
    cursor.execute(sql)
    all_act_meet_bef_conf = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_act_meet_bef_conf

def db_change_day(id, new_day):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET days_left_end={new_day} " \
          f"WHERE id={id};"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print('change_day is done')

def add_text_people_to_meeting(id_from_user, id_about_user, text):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET txt_about_people={text} " \
          f"WHERE id_from_user={id_from_user} AND " \
          f"id_about_user={id_about_user} AND " \
          f"is_active=True"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("add_text_to_meeting Update")

def db_deactivate_meeting(id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE meetings SET is_active=False, days_left_end=0 " \
          f"WHERE id={id}"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("db_deactivate_meeting Update")

def add_tabl_meetings(id_from_user, id_about_user):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"INSERT INTO meetings (id_from_user, id_about_user)" \
          f" VALUES ({id_from_user}, {id_about_user});"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("Meetings append")


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
    sql = f"SELECT id, first_name, username, is_active FROM users"
    cursor.execute(sql)
    all_users = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_users

def select_all_active_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, first_name, username, is_active FROM users WHERE is_active=True"
    cursor.execute(sql)
    all_users = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_users

def select_all_active_and_free_users():
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, first_name, username, is_active FROM users WHERE is_active=True AND is_free=True"
    cursor.execute(sql)
    all_users = cursor.fetchall()
    connect.commit()
    connect.close()
    return all_users

def select_is_free_user(user_id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT is_free FROM users WHERE id={user_id} AND is_active=True AND is_free=True"
    cursor.execute(sql)
    is_active_user = cursor.fetchall()
    connect.commit()
    connect.close()
    return is_active_user

def bd_make_free_user(user_id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE users SET is_free=TRUE WHERE id={user_id}"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("bd_make_free_user --> Update")

def bd_make_busy_user(user_id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"UPDATE users SET is_free=FALSE WHERE id={user_id}"
    cursor.execute(sql)
    connect.commit()
    connect.close()
    print("bd_make_busy_user --> Update")

def select_user(id):
    connect = connect_bd()
    cursor = connect.cursor()
    sql = f"SELECT id, first_name, username, is_active FROM users where id = {id}"
    cursor.execute(sql)
    user = cursor.fetchall()
    connect.commit()
    connect.close()
    return user

def update_active_user(id):
    connect = connect_bd()
    cursor = connect.cursor()
    cursor.execute(f'SELECT id, is_active FROM users WHERE id={id}')
    user = cursor.fetchall()
    if user[0][1] == True:
        cursor.execute(f'UPDATE users SET is_active=FALSE WHERE id={id}')
    else:
        cursor.execute(f'UPDATE users SET is_active=TRUE WHERE id={id}')
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

    # print(select_stat_rating_users())
    # bd_make_free_user(354585871)
    # bd_make_free_user(1908289217)
    # print(select_active_meetings())
    drop_table('meetings')
    drop_table('rating')
    # drop_table('answers')
    drop_table('users')
    drop_table('images')
    create_table_images()
    create_table_rating()
    create_table_users()
    # create_table_answers()
    create_table_meetings()
    # # create_new_answer(354585871, 1908289217, 'gfhvfdfkjdhfkjj sdlkf jdlkfjlskdjf lksjf sldf')
    # create_table_users()
    # add_user(354585871, 'Дмитрий', 'DmKusov')
    # add_user(485696536, 'Олег', 'Valeznik')
    # add_user(342857621, 'Елена', 'Elena_kusova')
    # add_user(1075946634, 'Владимир', 'vywakov')
    # add_tabl_meetings(123, 321)
    # all_us = select_all_users()
    # print(all_us)
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
