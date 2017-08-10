""" This module tests all functions in the bucketlist app """
import unittest
from views import register, login, USERS
from models import User, Bucket
class TestViewMethods(unittest.TestCase):
    """ This class tests methods of the views module """
    def setUp(self):
        self.name = "Eric Elem"
        self.correct_username = "eric.elem"
        self.short_username = "eri"
        self.long_username = "ericnelsonelem"
        self.invalid_chars_username = "eric@elem"
        self.correct_password = "password"
        self.short_pass = "pass"
        self.long_pass = "passwordpassword"

    def test_register(self):
        """ Tests the register method of the views class against various inputs """
        self.assertEqual(register(None, None, None, None), "None input")
        self.assertEqual(register("  ", " ", "  ", " "), "Blank input")
        self.assertEqual(register(self.name, self.short_username,
                                  self.correct_password, self.correct_password),
                         "Username should be 4 to 10 characters")
        self.assertEqual(register(self.name, self.long_username, self.correct_password,
                                  self.correct_password),
                         "Username should be 4 to 10 characters")
        self.assertEqual(register(self.name, self.correct_username, self.short_pass,
                                  self.short_pass),
                         "Password should be 6 to 10 characters")
        self.assertEqual(register(self.name, self.correct_username, self.long_pass,
                                  self.long_pass),
                         "Password should be 6 to 10 characters")
        self.assertEqual(register(self.name, self.invalid_chars_username, self.correct_password,
                                  self.correct_password),
                         "Illegal characters in username")
        self.assertEqual(register(self.name, self.correct_username, self.correct_password,
                                  self.long_pass),
                         "Passwords don't match")
        self.assertEqual(register(self.name, self.correct_username, self.correct_password,
                                  self.correct_password),
                         "Registration successful")

    def test_login(self):
        """ Tests the login method of the views module """
        self.assertEqual(login(None, None), "None input")
        self.assertEqual(login(" ", " "), "Blank input")
        self.assertEqual(login("unknownuser", "unknownpass"), "User not found")
        USERS[self.correct_username] = User(self.name, self.correct_username,
                                            self.correct_password)
        self.assertEqual(login(self.correct_username, "wrongpass"), "Wrong password")
        self.assertEqual(login(self.correct_username, self.correct_password), "Login successful")

class TestModelsMethods(unittest.TestCase):
    """ Tests methods from the various model classes in the models module """

    def setUp(self):
        self.user = User("Eric Elem", "eric.elem", "password")

    def test_add_bucket(self):
        """ Tests adding a new bucket """
        self.assertEqual(self.user.add_bucket(None), "None input")
        self.assertEqual(self.user.add_bucket(" "), "Blank input")
        self.assertEqual(self.user.add_bucket("shortname"),
                         "Bucket name should be greater than 10 and less than 60 characters")
        self.assertEqual(self.user.add_bucket
                         ("long name long name long name long name long name long name long name"),
                         "Bucket name should be greater than 10 and less than 60 characters")
        self.assertEqual(self.user.add_bucket("Things I should do before I am 30 years old"),
                         "Bucket added")
        self.assertEqual(self.user.add_bucket
                         ("Things I should do before I am 30 years old"),
                         "A bucket with this name already exists")

    def test_update_bucket(self):
        """ Tests updating a bucket """
        self.assertEqual(self.user.update_bucket(None, None), "None input")
        self.assertEqual(self.user.update_bucket(" ", "  "), "Blank input")
        self.assertEqual(self.user.update_bucket("notinthelistodbuckets", "snewname"),
                         "Bucket not found")
        self.user.add_bucket("Things I should do before I am 90 years old")
        self.user.add_bucket("This is the current bucket name")
        self.assertEqual(self.user.update_bucket(
            "Things I should do before I am 80 years old",
            "Things I should do before I am 80 years old"), "No change, same name")
        self.assertEqual(self.user.update_bucket("This is the current bucket name",
                                                 "Things I should do before I am 90 years old"),
                         "No change, new name already in bucket")
        self.assertEqual(self.user.update_bucket("Things I should do before I am 90 years old",
                                                 "snewname"),
                         "Bucket name should be greater than 10 and less than 60 characters")
        self.assertEqual(self.user.update_bucket
                         ("Things I should do before I am 90 years old",
                          "long name long name long name long name long name long name long name"),
                         "Bucket name should be greater than 10 and less than 60 characters")
        self.assertEqual(self.user.update_bucket("Things I should do before I am 90 years old",
                                                 "Things I should do before I am 50 years old"),
                         "Bucket updated")


    def test_delete_bucket(self):
        """" Test deleting a bucket """
        self.assertEqual(self.user.delete_bucket(None), "None input")
        self.assertEqual(self.user.delete_bucket(" "), "Blank input")
        self.assertEqual(self.user.delete_bucket("This bucket does not exist"), "Bucket not found")
        self.user.add_bucket("Things I should do before I am 90 years old")
        self.assertEqual(self.user.delete_bucket("Things I should do before I am 90 years old"),
                         "Bucket deleted")

    def test_add_item(self):
        """ Tests adding a new item """
        bucket = Bucket('Test')
        self.assertEqual(bucket.add_item(None), "None input")
        self.assertEqual(bucket.add_item(" "), "Blank input")
        self.assertEqual(bucket.add_item("Get married"), "Item added")
        self.assertEqual(bucket.add_item("Get married"), "Item already exists")

    def test_update_description(self):
        """ Tests updating item description """
        bucket = Bucket('Test')
        self.assertEqual(bucket.update_description(None, None), "None input")
        self.assertEqual(bucket.update_description(" ", " "), "Blank input")
        self.assertEqual(bucket.update_description("Get married", "Get married"), "No changes")
        self.assertEqual(bucket.update_description("Get married", "Get schooled"), "Item not found")
        bucket.add_item("Get schooled")
        bucket.add_item("Travel Africa")
        self.assertEqual(bucket.update_description("Get schooled", "Travel Africa"),
                         "New description already in bucket")
        self.assertEqual(bucket.update_description("Get schooled", "Travel Europe"),
                         "Item description updated")

    def test_update_status(self):
        """ Tests updating item status """
        bucket = Bucket('Test')
        self.assertEqual(bucket.update_status(None, None), "None input")
        self.assertEqual(bucket.update_status(" ", " "), "Blank input")
        self.assertEqual(bucket.update_status("Get married", "Pending"), "Item not found")
        bucket.add_item("Get schooled")
        bucket.add_item("Travel Africa")
        self.assertEqual(bucket.update_status("Get schooled", "The status"), "Invalid status")
        self.assertEqual(bucket.update_status("Travel Africa", "Done"),
                         "Status updated")

    def test_delete_item(self):
        """ Tests deleting an item from a bucket """
        bucket = Bucket('Test')
        self.assertEqual(bucket.delete_item(None), "None input")
        self.assertEqual(bucket.delete_item(" "), "Blank input")
        self.assertEqual(bucket.delete_item("Visit rwenzori mountain"), "Item not found")
        bucket.add_item("Get schooled")
        self.assertEqual(bucket.delete_item("Get schooled"), "Item deleted")
                      
if __name__ == '__main__':
    unittest.main()
