import psycopg2
from Repo.TGDesignBot.main.DBHandler.config import load_config
from Repo.TGDesignBot.main.YandexDisk import YaDiskInfo
from Repo.TGDesignBot.main.pptxHandler import pptxHandler
from . import select_scripts as select_scripts


# This func takes a sql query and pack of values. Do query with unpacked values
def __insert_single_value__(sql, *obj) -> int:
    config = load_config()
    obj_id = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                print(sql)
                cur.execute(sql, obj)
                row = cur.fetchone()
                print(row[0])
                print(row[1])
                if row:
                    obj_id = row[0]
                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        return obj_id


# This func takes a sql query and do it with values
def __insert_many_values__(sql, list_of_values: list):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.executemany(sql, list_of_values)

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Insert a new user into the users table
def insert_user(user_id, role: str):
    sql = """insert into users(user_id, role) values (%s, %s) returning *;"""
    __insert_single_value__(sql, user_id, role)


# Insert multiple users into the users table
def insert_many_users(user_list: list):
    sql = "insert into users(user_id, role) values(%s, %s)"
    __insert_many_values__(sql, user_list)


# Insert a new template into the templates table. Return template_id
def insert_template(template_info: YaDiskInfo.TemplateInfo) -> int:
    sql = """insert into templates(link, path, name)
             values (%s, %s, %s)  returning *;"""
    print(template_info.file)
    return __insert_single_value__(sql,
                                   template_info.file,
                                   template_info.path,
                                   template_info.name)


# Insert multiple templates into the templates table
def insert_many_templates(template_list: list):
    for template_info in template_list:
        insert_template(template_info)


# Insert a new font into the fonts table
def insert_font(font_info: YaDiskInfo.FontInfo):
    list_of_template_id = select_scripts.get_templates_from_directory(font_info.path)
    sql = """insert into fonts(link, path, template_id) 
             values (%s, %s, %s)  returning *"""
    for template_id in list_of_template_id:
        __insert_single_value__(sql,
                                font_info.file,
                                font_info.path,
                                template_id[0])


# Insert multiply fonts into the fonts table
def insert_many_fonts(font_list: list):
    for font_info in font_list:
        insert_font(font_info)


def insert_image(image_info: YaDiskInfo.ImageInfo):
    list_of_template_id = select_scripts.get_templates_from_directory(image_info.path)
    sql = """insert into images(template_id, path, link)
             values (%s, %s, %s) returning *;"""
    for template_id in list_of_template_id:
        __insert_single_value__(sql,
                                int(template_id[0]),
                                image_info.path,
                                image_info.position)


def insert_many_images(image_list: list):
    for image_info in image_list:
        insert_image(image_info)


def insert_slides(template_id: int, slide_info: pptxHandler.SlideInfo):
    sql = """insert into slides(slide_id, template_id, tags) 
             values (%s, %s, %s) returning *;"""
    __insert_single_value__(sql,
                            slide_info.slide_idx,
                            template_id,
                            slide_info.tags)


def insert_many_slides(template_id: int, slides_list: list) -> None:
    for slide_info in slides_list:
        insert_slides(template_id, slide_info)