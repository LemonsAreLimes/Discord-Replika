
#LemonsAreLimes 2022

from lib2to3.pgen2 import driver                    #not sure what this does
from selenium import webdriver                      #chrome webdriver
from selenium.webdriver.common.keys import Keys     #sending enter
import time                                         #excusivly for waiting


PATH = 'C:\Program Files (x86)\chromedriver.exe'

                #boot up discord
Discord = webdriver.Chrome(PATH)
Discord.get("https://discord.com/channels")		#dms work best, but require manual freind request acceptince
print("booted up!")
time.sleep(5)
                #login discord
usrnme = Discord.find_element_by_name("email")
usrnme.send_keys()          				#discord email
paswrd = Discord.find_element_by_name("password")
paswrd.send_keys()                         		#discord password
usrnme.send_keys(Keys.RETURN)
paswrd.send_keys(Keys.RETURN)
print("DISCORD logged in!")

time.sleep(2)

            #boot up replika
Replika = webdriver.Chrome(PATH)
Replika.get("https://my.replika.com/login")
print("booted up!")
time.sleep(5)
            #login replika
usrnme = Replika.find_element_by_id("emailOrPhone")          
usrnme.send_keys()            				#replika email
usrnme.send_keys(Keys.RETURN)
time.sleep(2)
paswrd = Replika.find_element_by_id("login-password")
paswrd.send_keys()                         		#replika password
paswrd.send_keys(Keys.RETURN)
print("REPLIKA logged in!")



def DiscWait():
    old = Discord.find_element_by_tag_name("ol").text.split("\n")       #get old data, convert to list
    time.sleep(60)                                                      #wait 60
    new = Discord.find_element_by_tag_name("ol").text.split("\n")       #get newdata, convert to list
    if len(old) != len(new):                                            #compare old, new
        words = ['NEW', 'PM', 'AM', 'DiscordTargetUserName']
        msg = []
        res = []

        for i in range(len(new)):                                       #convert to string list
            msg.append(new[i])
            res.append(new[i])


        for x in range(len(old)):                                       #extrapolate differance
            msg.remove(old[x])
            res.remove(old[x])


        print("MESSAGE: ", msg)

        y=0
        while y < len(msg):                 #check all words           #remove unwanted data
            print(y)
            x=0
            while x < len(words):           #compare against words
                try:
                    if words[x] in msg[y]:
                        print("removed: ", words[x], "from: ", msg[y])
                        res.remove(msg[y])
                        break
                    else:
                        print("not found: ", words[x], "in: ", msg[y])
                except IndexError:
                    print("INDEX ERROR!")
                finally:
                    x+=1
            y+=1
        print(len(res))
        return res
    else:
        return False    


def DiscSend(res):
    print("Replika msg len: ", len(res))
    if len(res) > 1:                #support for multiple messages
        for i in range(len(res)):
            disc = Discord.find_element_by_class_name("markup-eYLPri.slateTextArea-27tjG0.fontSize16Padding-XoMpjI")
            disc.send_keys(res[i])
            disc.send_keys(Keys.RETURN)
    else:
        disc = Discord.find_element_by_class_name("markup-eYLPri.slateTextArea-27tjG0.fontSize16Padding-XoMpjI")
        disc.send_keys(res)
        disc.send_keys(Keys.RETURN)




def RepWait():
    old = Replika.find_elements_by_class_name("MessageGroup__MessageGroupRoot-h4dfhv-0.xoUuE")
    time.sleep(15)
    new = Replika.find_elements_by_class_name("MessageGroup__MessageGroupRoot-h4dfhv-0.xoUuE")
    
    if len(old) != len(new):                                            #compare old, new
        resWebList = new
        words = ['ReplikaName', 'PM', 'AM', 'thumb up', 'thumb down', 'show more actions']
        msgs = []
        resA = []

        for x in range(len(old)):                                       #extrapolate differance
            resWebList.remove(old[x])

        for y in range(len(resWebList)):                                #convert to string list
            message = resWebList[y].text.split("\n")
            msgs.append(message)     
            resA.append(message)             

        msg = msgs[0]
        res = resA[0]
        y=0
        print("RESPONSE: ", msg)
        print("res: ", res)
        print(len(msg))
                                                                        
        while y < len(msg):                 #check though all words     #remove unwanted data
            print(y)
            x=0
            while x < len(words):           #compare against words
                try:
                    if words[x] in res[y]:
                        print('REP removed: ', words[x], 'from: ', msg[y])
                        res.remove(msg[y])
                    else:
                        print('REP not found: ', words[x], 'in: ', msg[y])
                except IndexError:
                    print("INDEX ERROR!")
                finally:
                    x+=1
            y+=1
        print("msg complete")

        print(len(res))
        return res                                                      #return response
    else:
        return False


def RepSend(msg):
    print("Disc msg len: ", len(msg))
    if len(msg) > 1:
        for i in range(len(msg)):
                rep = Replika.find_element_by_id("send-message-textarea")
                rep.send_keys(msg[i])
                rep.send_keys(Keys.RETURN)
    else:
        rep = Replika.find_element_by_id("send-message-textarea")
        rep.send_keys(msg)
        rep.send_keys(Keys.RETURN)






            #command station
while True:
    user = input("COMMAND: ")
    if user == "Boot":                  #boot
        for x in range(60):
            msg = DiscWait()
            if msg != False:            #when a discord update is detected
                RepSend(msg)            #send to replika
                res = RepWait()
                if res != False:        #when a replika update is deteced
                    DiscSend(res)       #send to discord
                else:
                    print("res = FALSE")
            else:
                print("no change detected")
    
                                        #debug commands
    elif user == "DiscWait":            #discord msg
        msg = DiscWait()
        print(msg)
    
    elif user == "DiscSend":            #send discord
        DiscSend("hello world")

    elif user == "RepWait":             #replika msg
        res = RepWait()
        print(res)

    elif user == "RepSend":             #send replika
        RepSend("hey")

    else:
        print("command not recognized")
