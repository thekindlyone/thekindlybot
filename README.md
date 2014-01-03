thekindlybot
============

This is a xmpp chatbot(sleekxmpp) that searches for and shares music via beets and smtp.
It also plays hangman and a philosophy(random feature  for a friend) quiz with contacts.
Allows contacts to search music in local library using beets music organizer and sends music to contacts via smtp on command

Files:
artists.dat : pickle of a list of major artists(I use it as a list of all artists i have discography of)
movielist.p : pickle of a list of movies scrapped from the internet
philobank.p : pickle of dictionary of questions->answers for philosophy quiz, also scrapped from web


Dependencies:
beets: 
http://beets.radbox.org/  
https://github.com/sampsyo/beets
pip install beets

sleekxmpp:
http://sleekxmpp.com/
https://github.com/fritzy/SleekXMPP
pip install sleekxmpp

eliza:
http://nltk.googlecode.com/svn/trunk/nltk-old/contrib/nltk_contrib/misc/eliza/eliza.py



Demonstration:


