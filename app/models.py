""" Contains the various object models used by the bucketlist app """
class User:
    """ Describes the user model """

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.buckets = {}

    def add_bucket(self, bucket_title):
        """ Adds a new bucket to the user's buckets """
        if bucket_title:
            if bucket_title.strip():
                if len(bucket_title) > 9 and len(bucket_title) < 61:
                    if not bucket_title in self.buckets:
                        self.buckets[bucket_title] = Bucket(bucket_title)
                        return "Bucket added"
                    return "A bucket with this name already exists"
                return "Bucket name should be greater than 10 and less than 60 characters"
            return "Blank input"
        return "None input"

    def update_bucket(self, title, new_title):
        """ Adds a new bucket to the user's buckets """
        if title and new_title:
            if title.strip() and new_title.strip():
                if not title == new_title:
                    if title in self.buckets:
                        if not new_title in self.buckets:
                            if len(new_title) > 9 and len(new_title) < 61:
                                self.buckets[new_title] = self.buckets.pop(title)
                                return "Bucket updated"
                            return (
                                "Bucket name should be greater than 10 and less than 60 characters")
                        return "No change, new name already in bucket"
                    return "Bucket not found"
                return "No change, same name"
            return "Blank input"
        return "None input"

    def delete_bucket(self, bucket_title):
        """ Deletes a bucket whose name is provided from a user's buckets """
        if bucket_title:
            if bucket_title.strip():
                if bucket_title in self.buckets:
                    self.buckets.pop(bucket_title)
                    return "Bucket deleted"
                return "Bucket not found"
            return "Blank input"
        return "None input"

class Bucket:
    """ Describes the bucket model """

    def __init__(self, title):
        self.title = title
        self.items = {}

    def add_item(self, description):
        """ Adds an Item to a bucket """
        if description:
            if description.strip():
                if not description in self.items:
                    self.items[description] = Item(description)
                    return "Item added"
                return "Item already exists"
            return "Blank input"
        return "None input"

    def update_description(self, description, new_description):
        """ Updates an Item's description in a bucket """
        if description and new_description:
            if description.strip() and new_description.strip:
                if not new_description == description:
                    if not new_description in self.items:
                        if description in self.items:
                            self.items[new_description] = self.items.pop(description)
                            return "Item description updated"
                        return "Item not found"
                    return "New description already in bucket"
                return "No changes"
            return "Blank input"
        return "None input"

    def update_status(self, description, status):
        """ Updates an Item's status in a bucket """
        if description and status:
            if description.strip() and status.strip():
                if description in self.items:
                    if status == "Pending" or status == "Done":
                        self.items[description].status = status
                        return "Status updated"
                    return "Invalid status"
                return "Item not found"
            return "Blank input"
        return "None input"

    def delete_item(self, description):
        """ Deletes an Item from a bucket """
        if description:
            if description.strip():
                if description in self.items:
                    self.items.pop(description)
                    return "Item deleted"
                return "Item not found"
            return "Blank input"
        return "None input"

class Item:
    """ Describes the item model """

    def __init__(self, description):
        self.description = description
        self.status = "Pending"
