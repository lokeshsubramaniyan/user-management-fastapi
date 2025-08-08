from app.db_config import db

credential_collection = db.get_collection('credential_data')

def credential_data(user_id, credential):
    return {
        'user_id': user_id,
        'title': credential.title,
        'username': credential.username,
        'password': credential.password,
        'url': credential.url,
        'notes': credential.notes,
        'is_deleted': credential.is_deleted,
        'created_at': credential.created_at,
        'updated_at': credential.updated_at
    }

def credential_data_update(credential):
    return {
        'title': credential.title,
        'username': credential.username,
        'password': credential.password,
        'url': credential.url,
        'notes': credential.notes,
        'updated_at': credential.updated_at
    }