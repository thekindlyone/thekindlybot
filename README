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

(11:08:12 PM) Thekindlyone: help
(11:08:13 PM) thekindlybot: 
1. this service queries music on my library. 
Example: to search for led zeppelin's no quarter, type 
$ led zeppelin no quarter 
The search feature accepts artists, tracknames, album names and combination of these fields.
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
mailing...F:\Music\Discographies\The Rolling Stones Discography MP3@320Kbps)? - 1968 -Beggars Banquet? Sympathy For The Devil.mp3
3.To find out if mail server is busy, type sup?
4.To list all artists whose discographies are present in the library, type:
list artists
4.HANGMAN I will play hangman with you if you want. to start session type 
#start hangman
note: No other commands will work while in hangman session except help .
To exit hangman session type
#stop hangman
5. Philo quiz -> start quiz by typing #start quiz
stop quiz by typing #stop quiz
If you want question repeated type #repeat while in quiz session
(11:08:34 PM) Thekindlyone: $ war pigs
(11:08:36 PM) thekindlybot: 
[1]Black Sabbath-100 Greatest Guitar Solos-War Pigs (MP3)
[2]Black Sabbath-Paranoid-War Pigs (FLAC)
[3]Black Sabbath-Past Lives Disc I-War Pigs (FLAC)
[4]Black Sabbath-Reunion - Disc 1-War Pigs (FLAC)
[5]Black Sabbath-We Sold Our Soul For Rock 'N' Roll  (Disc 1)-War Pigs (FLAC)
[6]Cake-B-Sides and Rarities-War Pigs (MP3)
[7]Cake-B-Sides and Rarities-War Pigs (Live) (MP3)
[8]Gov't Mule-Live ... With A Little Help Fr-War Pigs (MP3)
[9]Ozzy Osbourne-Just say Ozzy-War pigs (MP3)
[10]Ozzy Osbourne-Speak of the devil-War pigs (MP3)
[11]Ozzy Osbourne-The Ozzman cometh-War pigs (MP3)

(11:09:02 PM) Thekindlyone: @ war pigs #1
(11:09:04 PM) thekindlybot: 
Mailing...56 - War Pigs.mp3 File size = 12MB
(11:09:49 PM) Thekindlyone: sup?
(11:09:52 PM) ***thekindlybot mail server busy.
(11:12:01 PM) Thekindlyone: sup?
(11:12:03 PM) ***thekindlybot mail server busy.
(11:19:38 PM) thekindlybot: Mail Sent!
