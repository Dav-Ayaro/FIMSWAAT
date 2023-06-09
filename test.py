class user():
    def __init__(self, username):
        self.username = username


    def UserGroup():
        def __init__(self, name):
            self.name = name
            self.members = []

    def add_member(self, user):
        self.members.append(user)

    def remove_member(self, user):
        self.member.remove(user)

    def __str__(self):
        return self.name
    

user1 = user('david')
user2 = user('gabr')
user3 = user('marian')

