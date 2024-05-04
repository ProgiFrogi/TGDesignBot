import psycopg2
from Repo.TGDesignBot.main.DBHandler.config import load_config


def delete_template(template_id):
    """ Delete template by part id """

    sql = 'delete from templates where template_id = %s'
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the UPDATE statement
                cur.execute(sql, (template_id,))

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
