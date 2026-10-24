from typing import List, Dict

from twisted.internet import reactor
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Factory, P


from twisted.words.protocols.irc import IRC, ERR_NICKCOLLISION, ERR_NICKNAMEINUSE, ERR_ALREADYREGISTRED, RPL_TOPIC, \
    RPL_NAMREPLY, RPL_ENDOFNAMES, ERR_NOSUCHCHANNEL, RPL_ENDOFWHO

from classes.channel import Channel
from classes.user import User
from maze.mazechannel import MazeChannel


class MockIrc(IRC):
    mchannels : Dict[str,Channel]

    def __init__(self,users,channels):
        self.users: Dict[str,User] = users
        self.mchannels: Dict[str,Channel]= channels
        self.user = None

    def irc_NICK(self,prefix,params):
        nick = params[0]

        if nick in self.users.keys():
            self.sendCommand(ERR_NICKNAMEINUSE, ["nick already in use"])

            return


        self.users[nick] = User(nick,self)
        self.user = self.users[nick]


    def irc_USER(self, prefix,params):
        nick = params[0]
        hostname= params[1]



        if nick not in self.users.keys():
            return


        r = self.users[nick].register(hostname)
        if not r:
            self.sendCommand(ERR_ALREADYREGISTRED, parameters=["user already registered"])


        self.sendLine("info connection granted, welcome to the dungeon")

    def irc_PING(self, prefix,params):
        self.sendCommand("PONG",["1792848350753772105"])


    def irc_PASS(self, prefix, params):
        self.sendLine("info passwords not needed")

    def irc_CAP(self,prefix,params):
        # ignore this it is too fancy for us
        pass

    def irc_QUIT(self,_,a):
        nick = self.user.nick
        print(f"user lost: {nick}")

        del self.users[nick]



    def irc_WHO(self, prefix,params):
        self.sendCommand(RPL_ENDOFWHO,[params[0],":End of /WHO list"])

    def irc_PART(self, prefix, params):
        for chan_name in params:
            if chan_name not in self.mchannels.keys():
                self.sendCommand(ERR_NOSUCHCHANNEL, [chan_name, ":No Such Channel"])
                return

            chan = self.mchannels[params[0]]

            chan.part(self.user,"quit")


    # irc command like you nickname for some reason, do not touch this unless oyu want to cry
    def irc_JOIN(self,prefix,params):
        for chan_name in params:
            if chan_name not in self.mchannels.keys():
                self.sendCommand(ERR_NOSUCHCHANNEL,[chan_name,":No Such Channel"])
                return


            chan = self.mchannels[params[0]]

            chan.join(self.user)
            self.sendCommand(RPL_TOPIC,  [chan.name, ":",chan.topic])
            self.sendCommand(RPL_ENDOFNAMES,  [chan.name, ":", "End of /NAMES list"])


    def irc_PRIVMSG(self,prefix,params):
        dest:str = params[0]

        if dest.startswith("#"):


            chan = self.mchannels[dest]

            chan.send(self.user,params[-1])


    def irc_MODE(self,prefix,params):
        # everyone can do everything
        pass



class Server(Factory):

    users = {}
    channels = {"#me": Channel("#me","talk about me"),
                "#maze": MazeChannel("#maze","Enter the maze")}
    def buildProtocol(self, addr: IAddress | None) -> P | None:
        return MockIrc(self.users,self.channels)


if __name__ == "__main__":
    reactor.listenTCP(6667,factory=Server())
    reactor.run()