from passlib.context import CryptContext

passcontext=CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(password:str):
    return passcontext.hash(password)

def verify(user_added_password,database_stored_password):
    return passcontext.verify(user_added_password,database_stored_password)
    