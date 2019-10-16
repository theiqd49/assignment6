from pymongo import MongoClient
import datetime
import logging
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# TODO: put LOG_FORMAT in common place
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


class user_db_api(object):
    """
    A class contains all interfaces to manipulate user data in Mongodb
    
    TODO:
    Attributes
    ----------   

    Methods
    -------
    
    """

    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
        client = MongoClient(
            "mongodb+srv://zed:yy9826@cluster0-uaytj.mongodb.net/" \
            "test?retryWrites=true&w=majority")

        db = client.apt
        self.collection = db.user

        server_status_result = db.command("serverStatus")
        self.log.info(server_status_result)

    def exists_email(self, u_email):
        """
        Return whether email address exists in user records, if exist
            return first record, if not exist, return None
        """
        return self.collection.find({"u_email": u_email}).limit(1)

    def exists_uid(self, u_id):
        """
        Return whether user id exists in user records, if exist
            return first record, if not exist, return None
        """
        return self.collection.find({"_id": u_id}).limit(1)

    def add_user(self, u_email, u_username, u_password,
                 u_gender=None, u_phone=None, u_description="None",
                 u_avatar="None", u_report_list=[], u_subscribed_themes=[]):
        """
        Add one user record into database, need to provide at least email and 
           password
        TODO: password may need to be salted

        :param u_subscribed_themes: user subscribed themes string list
        :param u_email: user email string
        :param u_username: username string
        :param u_password: password hash string
        :param u_gender: gender, 0: female, 1: male, 2 other
        :param u_phone: phone number string
        :param u_description: description string
        :param u_avatar: avatar address string
        :param u_report_list: list[str], a list of report address string
        :return: _id of the inserted user in the "user" collection
        :rtype: str
        """

        assert type(u_email) == str
        assert type(u_username) == str
        assert type(u_password) == str
        # TODO: u_email should fit some kind of regex...
        assert type(u_description) == str
        assert type(u_avatar) == str
        # TODO: r_avatar should fit some kind of regex...
        assert isinstance(u_report_list, list)
        for _report in u_report_list:
            assert type(_report) == str
        for _subscribed in u_subscribed_themes:
            assert type(_subscribed) == str

        new_user = {"u_email": u_email,
                    "u_username": u_username,
                    "u_password": generate_password_hash(u_password),
                    "u_gender": u_gender,
                    "u_phone": u_phone,
                    "u_description": u_description,
                    "u_avatar": u_avatar,
                    "u_report_list": u_report_list,
                    "u_subscribed_themes": u_subscribed_themes
                    }
        result = self.collection.insert_one(new_user)
        self.log.info("New user inserted. New user id: %s" % result.inserted_id)
        return result.inserted_id

    def get_user_by_uid(self, u_id):
        """
        Return user report in dict format by user id

        :param u_id: The _id of the user you are trying to get
        :return: result of the get method
        :rtype: dict
        """

        result = self.collection.find_one({"_id": u_id})
        if result is not None:
            self.log.info("Get user %s." % u_id)
        else:
            self.log.error("Get user %s failed. " % u_id)
        return result

    def get_user_by_username(self, u_username):
        """

        Return user report in dict format by username
        :param u_username: the u_username of the user you are trying to get
        :type u_username: str
        :return: result of the get method
        :rtype: dict
        """
        assert type(u_username) == str

        result = self.collection.find_one({"u_username": u_username})
        if result:
            self.log.info("Get user %s." % u_username)
        else:
            self.log.error("Get user %s failed. " % u_username)
        return result

    def modify_username(self, u_id, new_username):
        """

        Modify username for user identified by user id        
        :param u_id: the u_id of the user whose username is to be modified
        :param new_username: str
        """
        assert type(new_username) == str

        if self.exists_uid(u_id) is not None:
            my_query = {"_id": u_id}
            self.log.info("check if username already exists, get user by username")
            if self.get_user_by_username(new_username) is None:
                new_values = {"$set": {"u_username": new_username}}
                result = self.collection.update_one(my_query, new_values)
                self.log.info("Username modified for user ID: %s" % u_id)
            else:
                self.log.warning("Username taken")
        else:
            self.log.warning("User not exist")


    def modify_password(self, u_id, old_password, new_password):
        """
        Modify password for user identified by user id, need to verify the 
            old password before update

        :param u_id: u_id of the user who is trying to modify password
        :param old_password: old password str
        :param new_password: new password str
        """
        assert type(old_password) == str
        assert type(new_password) == str
        if self.exists_uid(u_id) is not None:
            my_query = {"_id": u_id}
            if check_password_hash(self.get_user_by_uid(u_id)['u_password'], old_password):
                new_values = {"$set": {"u_password": generate_password_hash(new_password)}}
                result = self.collection.update_one(my_query, new_values)
                self.log.info("Password modified for user ID: %s" % u_id)
            else:
                self.log.warning("Wrong password")
        else:
            self.log.warning("User not exist")

    def delete_user_by_id(self, u_id):
        """
        Delete user report identified by user id in database 

        :param u_id: delete user by u_id
        """
        if self.exists_uid(u_id) is not None:
            my_query = {"_id": u_id}
            result = self.collection.delete_one(my_query)
            if result.deleted_count:
                self.log.info("User deleted. ID: %s" % u_id)
            else:
                self.log.warning("User deletion failed: %s" % result.raw_result)

    def get_subscribed_theme_by_id(self, u_id):
        if self.exists_uid(u_id) is not None:
            return self.get_user_by_uid(u_id)['u_subscribed_themes']
        else:
            self.log.warning("User not exist")


# Below is the test part
if __name__ == "__main__":
    print("Test1: init a user_db_api object and connect to db.")
    user = user_db_api()
    print("Test2: add a new user with u_username, u_email and u_password.")
    id = user.add_user("test@utexas.edu", "test", "admin")
    print("Test3: get a new user by user id _id.")
    print(user.get_user_by_uid(id))
    print("Test4: get a new user by username u_username")
    print(user.get_user_by_username("test"))
    print("Test5: delete a user by user id _id.")
    user.delete_user_by_id(id)
    print("Test6: delete a non-exist user by user id _id.")
    user.delete_user_by_id(id)
    id1 = user.add_user("admin1@utexas.edu", "admin1", "admin1")
    print(user.get_user_by_uid(id1))
    print("Test7: modify username by user id _id")
    user.modify_username(id1, "modified_admin1")
    print(user.get_user_by_uid(id1))
    print("Test8: modify user password by user id _id and old password")
    user.modify_password(id1, "admin1", "modified_admin1")
    print(user.get_user_by_uid(id1))
