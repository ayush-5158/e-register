def noteEntity(item)->dict:
    return{
        "id": str(item["_id"]),
        "uid": item["uid"],
        "desc": item["desc"],
    }

def notesEntity(item)->list:
    return [noteEntity(item) for item in item["notes"]]

def user(item)->dict:
    return {
        "uid": item["uid"],
        "name": item["name"],
        "email ": item["email"],
        "password": item["password"],
    }