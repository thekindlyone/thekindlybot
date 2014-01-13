from time import time
import pickle
from random import choice
import string
# philo game work
    
class vplayer(object):
    def __init__(self,pname):
        self.name=pname
        self.question=''        
        self.answer=''
        self.done=[]
        self.tried=[]
        self.creationtime=time()
        
    def reset(self):
        self.question,self.answer=self.fetchquestion()
        self.lastaction=time()
        self.tried=[]
        self.done=['']
    
    def fetchquestion(self):
        self.lastaction=time()
        qbank=pickle.load(open(r'philobank.p','r'))
        q=choice(qbank.keys())
        a=qbank[q]
        return q,a.lower()
    
    def getstat(self):
        self.lastaction=time()
        return 'name = '+self.name+' question= '+self.question+' answer ='+self.answer+' tried list='+str(self.tried)+' done list='+str(self.done)
    
    def displaytext(self):
        self.lastaction=time()
        rs=''
        for i in range(len(self.answer)):
            if self.answer[i] in self.done : rs=rs+self.answer[i]
            else:
                if self.answer[i]==' ': rs=rs+'/'
                else: rs=rs+'_'+' '
        return rs





class vgame(object):
    def __init__(self):
        self.playertable={}
    
    def register_player(self,newplayer):
        self.playertable[newplayer]=vplayer(newplayer)        
    def delete_player(self,playername):
        self.playertable.pop(playername,None)
        return 'Quiz session ended!'

        
    def startgame(self,f):
        self.playertable[f].reset()
        return '\n************Game Started!***********\n'+'Question: '+self.playertable[f].question+'\n\n'+self.playertable[f].displaytext()
        
        
        
    def gameresponse(self,q,f):
        q=q.replace(' ','')
        if q:
            if q=='#repeat' or q=='# repeat':
                response='Question: '+self.playertable[f].question
            else:
                if len(q)>1: q=q[0].lower()
                if q in self.playertable[f].answer:
                    self.playertable[f].done.append(q)
                    response='\n'+self.playertable[f].displaytext()+'\n'+'HANGMAN'[:len(self.playertable[f].tried)]
                else:
                    if q in self.playertable[f].tried:
                        response='Already tried!\n'+self.playertable[f].displaytext()+'\n'+'HANGMAN'[:len(self.playertable[f].tried)]
                    else: 
                        self.playertable[f].tried.append(q)
                        response='INCORRECT, Try Again!\n'+self.playertable[f].displaytext()+'\n'+'HANGMAN'[:len(self.playertable[f].tried)]
                if len(self.playertable[f].tried)==len('HANGMAN'):
                    response='HANGMAN\n Game Over, You lost. The answer was '+self.playertable[f].answer+self.startgame(f)
                    
                if '_' not in self.playertable[f].displaytext():
                    response=self.playertable[f].answer+' VICTORY!!!!\n\n\n'+self.startgame(f)
                
        else: response='WTF?'
        return response
    
    def cleanup(self):
        for n in self.playertable:
            if (self.playertable[n].lastaction-self.playertable[n].creationtime)>(30*60):
                self.delete_player(n) 

