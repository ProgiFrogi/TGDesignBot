import json


def is_admin_with_json(id: int) -> bool:
    with open("admins.json", "r") as file:
        config = json.load(file)
        admins_list = config["admin_id"]
        return id in admins_list
