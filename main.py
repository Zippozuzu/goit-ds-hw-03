from pymongo import MongoClient, errors
from functools import wraps

database_name = "test"
url = "mongodb+srv://test:p3ecyRsWF5iqjzxd@cluster0.sp47g.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(url)
db = client[database_name]


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.PyMongoError as e:
            print(f"Database error in function {func.__name__}: {e}")
        except Exception as e:
            print(f"Unexpected error in function {func.__name__}: {e}")

    return wrapper


# Створити один екземпляр
@exception_handler
def create_one(collection, name, age, features):
    result_one = db[collection].insert_one(
        {
            "name": name,
            "age": age,
            "features": features,
        }
    )
    print(f"Document with id {result_one.inserted_id} was created.")


# Знайти всі екзампляри колекції
@exception_handler
def find_all(collection):
    result = db[collection].find({})
    for el in result:
        print(el)


# Знайти колекцію по імені
@exception_handler
def find_name(collection, name):
    result = db[collection].find_one({"name": name})
    print(result)


# Змінити вік по імені
@exception_handler
def update_age(collection, name, age):
    result = db[collection].update_one({"name": name}, {"$set": {"age": age}})
    print(f"Document with name {name} was updated. New age is {age}")


# Додати властивості по імені
@exception_handler
def update_features(collection, name, new_features):
    result = db[collection].update_one(
        {"name": name}, {"$push": {"features": {"$each": new_features}}}
    )
    print(find_name(collection, name))


# Видалити екземпляр по імені
@exception_handler
def delete_name(collection, name):
    result = db[collection].delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Document with name '{name}' deleted.")
    else:
        print(f"No document found with name '{name}'.")


# Видалити всі екземпляри колекції
@exception_handler
def delete_all(collection):
    db[collection].delete_many({})
    print(f"All documents were deleted.")


if __name__ == "__main__":
    find_all("cats")
    # create_one("cats", "barsik", 3, ['ходить в лоток','не дає себе гладити','сірий'])
    # find_all("cats")
    # find_name ("cats", "taras")
    # update_age ("cats", "taras", 3)
    # update_features("cats", "taras", ["test3", "test4"])
    # delete_name("cats", "taras")
    # delete_all("cats")
