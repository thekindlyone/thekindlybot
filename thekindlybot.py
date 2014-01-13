import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import subprocess
import smtplib
import mimetypes
import email
import email.mime.application
import thread
import os
from multiprocessing import *
import re
import eliza
import pickle
import string
from random import choice
from time import time
import unidecode
import sys
from ConfigParser import SafeConfigParser
from hangman import *
from philogame import *
# Mail Thread
def sendmail(fn,to,activeflag,xmobj,recipient,botaddress,pw,smtp_server):
    activeflag.value=1
    filename=fn
    
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] =filename[filename.rfind('\\')+1:] 
    msg['From'] = botaddress
    msg['To'] = to
    
    
    body = email.mime.Text.MIMEText("""thekindlybot abides. Ask and the tunes are thine.""")
    msg.attach(body)       
    
    
    fp=open(filename,'rb')
    #att = email.mime.application.MIMEApplication(fp.read(),_subtype="mp3")
    att = email.mime.application.MIMEApplication(fp.read())
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=filename)
    msg.attach(att)
    s = smtplib.SMTP(smtp_server)
    s.starttls()
    s.login(msg['From'],pw)
    s.sendmail(msg['From'],[msg['To']], msg.as_string())
    s.quit()
    activeflag.value=0
    xmobj.send_message(recipient, mbody='Mail Sent!')
    print 'mail sent! to ',recipient
    thread.exit()








class EchoBot(ClientXMPP):

    def __init__(self, jid, password, smtp_server):
        ClientXMPP.__init__(self, jid, password)
        self.mymail=jid
        self.mymailpw=password
        self.smtp_server=smtp_server
        self.active= Value('i')
        self.active.value=0
        self.therapist=eliza.eliza()
        self.artists=pickle.load(open(r'artists.dat'))
        self.hangman=game()
        self.philo=vgame()
        self.links=open(r'links.txt').read().split('\n')
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence(pstatus="Hello, I am a chat bot. I like distributing music and playing Hangman. Type 'help' for help.")
        print 'Session started'
        
        self.get_roster()
    

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            #msg.reply("Thanks for sending\n%(body)s" % msg).send()
            #print '\n\n\n\n'
            f="%(from)s"%msg
            q="%(body)s"%msg
            q=string.lower(q)
            print '\n************************\n',f,'says: ',q
            pt=self.hangman.playertable
            ppt=self.philo.playertable
            if (f not in pt)and q !='help' and (f not in ppt):
                
                reply="*"+self.therapist.respond(q)+"*"+"\nTYPE _help_ for syntax"
                # search
                if q=='list artists':
                    reply="This is a list of all the artists whose discography is present in my library. Note: There are many more artists besides this in my library, but I do not possess their entire work \n"+self.artists
                if q[0]=='$' and len(q)<=5:
                    reply="This is a 300 GB music library. Do a more specific search. Don't search for 'love' or 'the' etc. *TRY AGAIN*"
                if q[0]=='$' and len(q)>5:
                    
                    ql = filter(None,q[1:].strip().split(' '))
                    cl=["beet","list","-f","$artist-$album-$title ($format)"]+ql
                    #command="beet ls "+q[1:].strip()
                    try:
                        track_output=subprocess.check_output(cl)
                        #file_output=subprocess.check_output("beet ls -p "+q[1:].strip())
                        tracks = filter(None, track_output.split('\n'))
                        #files = filter(None, file_output.split('\n'))
                        s=''
                        n=1
                        ex=""
                        length=len(tracks)
                        if length>500:
                            tracks=tracks[:100]
                            ex="\n"+str(length-100)+" more results founds on given keywords. This is a 300 GB music library. Do a more specific search. Don't search for 'love' or 'the' etc. "
                        for track in tracks:
                            s=s+'['+str(n)+']'+track+'\n'
                            n=int(n)+1
                        reply='\n'+s+ex 
                        if len(track_output)==0:
                            reply='''\n thekindlybot could not find what you looked for. Try again with different keywords. 
If $ zz-top doesn't work try $ zz top or $ zztop. To learn mail command type help.
If you still can't find the track, then most likely I don't have it.'''
                        
                    except:
                        reply='UNRECOGNIZED COMMAND.\nTYPE help for help.'
                
                # EMAIL
                if re.match('@.+?#\d+$',q):
                    if re.match('.+?@gmail.com$',f[:f.rfind('/')]):
                        
                        if self.active.value==0:
                            num=int(q[q.rfind('#')+1:])
                            
                            q=q[:q.rfind('#')]
                            command="beet ls -p "+q[1:].strip()
                            file_output=subprocess.check_output(command)
                            files = filter(None, file_output.split('\n'))
                            fl=files[num-1].strip()
                            size=os.stat(fl).st_size/(1024*1024)
                            if size<24:
                                reply='\n'+'Mailing...'+fl[fl.rfind('\\')+1:]+' File size = '+str(size)+'MB'
                                rec="%(from)s"%msg
                                thread.start_new_thread(sendmail,(fl,f[:f.rfind('/')],self.active,self,rec))
                            else:
                                reply='File larger than 25MB, cannot send. This is a limitation of google smtp server. Take it up with them.'
                        else:
                            reply='Mail server busy, Try again in a while. type sup? for status'
                    else:
                        reply='''Sorry, your email id is coming across all garbled. I suspect this is encryption at some level. Please specify your email id with command like \n@ <search query> #<number> =<email id>
Example:
if your email id is xyz@gmail.com and you want the 3rd result of search query 'ravi raga' mailed to you, use command:
@ ravi raga #3 =xyz@gmail.com'''
                #CUSTOM EMAIL
                if re.match('@.+#\d\s*=.+@gmail.com',q):
                    if self.active.value==0:
                        
                        from_id=q[q.rfind('=')+1:]
                        q=q[:q.rfind('=')]
                        num=int(q[q.rfind('#')+1:])
                        q=q[:q.rfind('#')]
                        command="beet ls -p "+q[1:].strip()
                        file_output=subprocess.check_output(command)
                        files = filter(None, file_output.split('\n'))
                        fl=files[num-1].strip()
                        size=os.stat(fl).st_size/(1024*1024)
                        if size<24:                        
                            reply='/me \n'+'Mailing...'+fl[fl.rfind('\\')+1:]+' File size = '+str(size)+'MB'+' to '+from_id
                            rec="%(from)s"%msg
                            thread.start_new_thread(sendmail,(fl,from_id,self.active,self,rec))
                        else:
                            reply='File larger than 25MB, cannot send. This is a limitation of google smtp server. Take it up with them.'
                    else:
                        reply='Mail server busy, Try again in a while. type sup? for status'
                    
                    
                    

                
                if q=='sup?':
                    if self.active.value==0:
                        reply='/me is ready for mailing!!'
                    else:
                        reply='/me mail server busy.'
                        
                if q=='#start hangman' or q=='# start hangman':
                    self.hangman.cleanup()
                    self.hangman.register_player(f)
                    reply=self.hangman.startgame(f)
                if q=='#start quiz'or q=='# start quiz':
                    self.philo.cleanup()
                    self.philo.register_player(f)
                    reply=self.philo.startgame(f)
            else:            
                if(f in pt) and q!='help' and (f not in ppt):
                    if q=='#stop hangman' or q=='# stop hangman': 
                        reply=self.hangman.delete_player(f)
                    else:    
                        if q=='#start hangman' or q=='# start hangman':
                            r1='Old '+self.hangman.delete_player(f)+'\n'
                            self.hangman.register_player(f)
                            r2=self.hangman.startgame(f)
                            reply=r1+r2
                        else: 
                            reply=self.hangman.gameresponse(q,f)
                if(f not in pt) and q!='help' and (f in ppt):
                    if q=='#stop quiz' or q=='# stop quiz':
                        reply=self.philo.delete_player(f)
                    else:
                        if q=='#start quiz' or q=='# start quiz':
                            r1='Old '+self.philo.delete_player(f)+'\n'
                            self.philo.register_player(f)
                            r2=self.philo.startgame(f)
                            reply=r1+r2
                        else:
                            reply=self.philo.gameresponse(q,f)
            
            #help
            if q=='help':
                
                custom='6. Philo quiz -> start quiz by typing #start quiz\nstop quiz by typing #stop quiz\nIf you want question repeated type #repeat while in quiz session'
                
                reply="""\n1. this service queries music on my library. \nExample: to search for led zeppelin's no quarter, type \n$ led zeppelin no quarter 
*The search feature accepts artists, tracknames, album names and combination of these fields.*
2. To receive email with chosen track as attachment, type :
@ <query that yielded results with $> #<index number>
Example: 
me: $ rolling stones sympathy
thekindlybot@gmail.com: 
[1]The Rolling Stones - 100 Greatest Guitar Solos - Sympathy For The Devil
[2]The Rolling Stones - Beggars Banquet - Sympathy For The Devil
[3]The Rolling Stones - Classic Hits - Sympathy For The Devil
me: @ rolling stones sympathy #2
thekindlybot@gmail.com:
mailing...F:\Music\Discographies\The Rolling Stones Discography MP3@320Kbps)\07 - 1968 -Beggars Banquet\01 Sympathy For The Devil.mp3
3.To find out if mail server is busy, type sup?
4.To list all artists whose discographies are present in the library, type:
list artists
4.HANGMAN I will play hangman with you if you want. to start session type 
#start hangman
note: No other commands will work while in hangman session except _help_ .
To exit hangman session type
#stop hangman
5.For a random interesting link, type 
#random
"""+custom
            if q==':(':
                reply='/me hugs you'
           
            if q=='#random'or q=='# random':
                reply=choice(open(r'links.txt').read().split('\n'))
            msg.reply(reply).send()
            print '\n\n'
            print 'Reply=',reply
            print'\n\n**************************'

            
                
if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    parser=SafeConfigParser()
    
    parser.read('thekindlybot_config.ini')
    emid=parser.get('credentials','emailid')
    pw=parser.get('credentials','password')
    smtp_server=parser.get('credentials','smtpserver')
    xmpp_server=parser.get('credentials','xmppserver')
    port=int(parser.get('credentials','port'))
    xmpp = EchoBot(emid, pw, smtp_server)
    xmpp.connect((xmpp_server, port))
    xmpp.process(block=True)
