import psycopg2
from config import load_config


def update_user(user_id, role: str):
    """ Update user_role based on the vendor id """

    sql = """ update users
                set role = %s
                where user_id = %s"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the UPDATE statement
                cur.execute(sql, (role, user_id))

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)