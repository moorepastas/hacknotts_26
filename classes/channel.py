from socketserver import StreamRequestHandler
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from classes.user import User


class Channel:
    users: List[User]
    topic : str
    name: str

    def __init__(self,name, topic):
        self.name = name
        self.topic = topic
        self.users = []

    def part(self, user:User, reason):
        print(user.name())
        print(self.users)
        self.users.remove(user)

        for u in self.users:
            user.protocol.part(user.name(),self.name,reason)

    def join(self, user):
        self.users.append(user)
        user.chans.append(self)

        for u in self.users:
            u.protocol.join(user.name(),self.name)

    def send(self,user, message):
        for u in self.users:
            if u != user:
                u.protocol.privmsg(user.name(),self.name,message)


