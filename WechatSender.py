# coding: utf-8
import itchat

class WechatSender:

    def __init__(self):
        itchat.auto_login(enableCmdQR=2, hotReload=True)  

    def sendMessageToUser(self, message, receiver):
        user = itchat.search_friends(name=receiver)
        for u in user:
            u.send(message)
