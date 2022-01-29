from lib2to3.pgen2 import driver                    #not sure what this does
from selenium import webdriver                      #chrome webdriver
from selenium.webdriver.common.keys import Keys     #sending enter
import time                                         #excusivly for waiting
import random                                       #used for veritey in typing speed

PATH = 'C:\Program Files (x86)\chromedriver.exe'

                #boot up discord
Discord = webdriver.Chrome(PATH)
Discord.get("https://discord.com/channels/")
print("booted up!")
time.sleep(5)
                #login discord
usrnme = Discord.find_element_by_name("email")
usrnme.send_keys('')           				#discord email
paswrd = Discord.find_element_by_name("password")
paswrd.send_keys('')                         		#discord password
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
usrnme.send_keys('')          					  #replika email
usrnme.send_keys(Keys.RETURN)
time.sleep(2)
paswrd = Replika.find_element_by_id("login-password")
paswrd.send_keys('')			                          #replika password
paswrd.send_keys(Keys.RETURN)
print("REPLIKA logged in!")


def DiscWait():
    while True:                                                             #detect when the user is typing
        try:
            Discord.find_element_by_class_name('text-3S7XCz')
            break
        except:
            print('not typing')
        finally:
            time.sleep(1)

    print('TYPING DETECTED')
    old = Discord.find_element_by_tag_name("ol").text.split("\n")           #get old data, convert to list
    name = Discord.find_element_by_class_name('text-3S7XCz').find_element_by_tag_name('strong').text
    print(name)

    while True:                                                             #detect when the user not typing
        try:
            Discord.find_element_by_class_name('text-3S7XCz')
            print('typing...')
        except:
            print('not typing after typing')
            break
        finally:
            time.sleep(1)

    print('DONE TYPING')
    new = Discord.find_element_by_tag_name("ol").text.split("\n")           #get old data, convert to list

    if len(old) != len(new):                                                #compare old, new
        msg = []
        res = []

        for i in range(len(new)):                                           #convert to string list
            msg.append(new[i])
            res.append(new[i])
        for x in range(len(old)):                                           #extrapolate differance
            msg.remove(old[x])
            res.remove(old[x])

        print("MESSAGE: ", msg)

        diff = DiscFilter(msg, res, name)                                   #remove unwanted data
        return diff
    else:
        return False


def DiscFilter(msg, res, name):                                             #remove unwanted data
    words = ['NEW', 'PM', 'AM', name]
    y=0

    while y < len(msg):                 #check all words
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
    


def RepWait():
    old = Replika.find_elements_by_class_name("MessageGroup__MessageGroupRoot-h4dfhv-0.xoUuE")
    time.sleep(10)
    new = Replika.find_elements_by_class_name("MessageGroup__MessageGroupRoot-h4dfhv-0.xoUuE")
    
    if len(old) != len(new):                                            #compare old, new
        resWebList = new
        words = ['nyjii', 'PM', 'AM', 'thumb up', 'thumb down', 'show more actions']
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
                    print("INDEXERROR!")
                finally:
                    x+=1
            y+=1
        print("msg complete")

        print(len(res))
        return res                                                      #return response
    else:
        return False





def DiscSend(res):
    print("Replika msg len: ", len(res))
    disc = Discord.find_element_by_class_name("markup-eYLPri.slateTextArea-27tjG0.fontSize16Padding-XoMpjI")
    for i in range(len(res)):

        disc.send_keys('typing')
        for x in range(6):  #used for typing animation
            disc.send_keys(Keys.BACKSPACE)
            time.sleep(random.randint(1,10))

        disc.send_keys(res[i])
        disc.send_keys(Keys.RETURN)


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
