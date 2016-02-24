import serial, sys, os, time, hashlib, random

if len(sys.argv) != 2:
	print "usage: {} <serial port>".format(sys.argv[0])
	sys.exit(1)
else:
	sportname = sys.argv[1]

try:
	ser = serial.Serial(sportname,57600,timeout=0.1)
except:
	print "serial port initialization failed"
	sys.exit(3)

class DoneException:
	pass

nodename = "c" + str(random.randint(10000,1000000))
print "initializing node with name " + nodename

def hexs(s):
	return s.encode('hex')

def unhexs(h):
	return h.decode('hex')

# global variables:
connected = False
timer = time.time()
inbuffer = ''
conntimer = 0
serverid = ''
filebuffer = ''

def mainloop():
	global connected, inbuffer, conntimer, serverid, filebuffer
	inbuffer += ser.read(8)
	tempsp = inbuffer.split('\n',1)
	if len(tempsp) > 1:
		cmd = tempsp[0].split()
		inbuffer = tempsp[1]
		if cmd[0][0] == ':':
			try:
				print "recieved command: " + tempsp[0]
				if cmd[0] == ":DISCOVER":
					#connected = True
					if not connected:
						ser.write(b':CLIENT ' + nodename + '\n')
					conntimer = time.time()
				elif cmd[0] == ":SERVER":
					serverid = cmd[1]
					print "server " + serverid + " connected"
					conntimer = time.time()
					ser.write(b':READY\n') # indicate ready for the real syncing stuff
				elif cmd[0] == ":FILENAME":
					fn = os.path.join(os.getcwd(),cmd[1])
					if os.path.exists(fn): # stat file
						fv = open(fn,'rb').read()
						m = hashlib.md5()
						m.update(fv)
						ser.write(b':FILESTAT {} {} {}\n'.format('true',len(fv),m.hexdigest())) # exists, size, hash
					else:
						ser.write(b':FILESTAT false 0 0\n')
				elif cmd[0] == ":SYNC":
					print "sync requested"
					filebuffer = ''
					ser.write(b':READY_SYNC\n')
				elif cmd[0] == ":DATA":
					l = int(cmd[1])
					h = cmd[2]
					dat = unhexs(cmd[3])
					# now check it
					m = hashlib.md5()
					m.update(dat)
					if m.hexdigest() == h:
						filebuffer += dat
						print "successfully recieved {} bytes of data".format(l)
						ser.write(b':SUCCESS\n')
					else:
						print "error recieving data ({}, {}); retrying".format(m.hexdigest(),h)
						ser.write(b':RETRY\n')
				elif cmd[0] == ":DONE":
					m = hashlib.md5()
					m.update(filebuffer)
					if cmd[1] == m.hexdigest():
						print "successfully transferred file"
						fn = os.path.join(os.getcwd(),cmd[2])
						fd = open(fn,'wb')
						fd.write(filebuffer)
						fd.close()
						filebuffer = ''
						ser.write(":RECV_DONE\n")
					else:
						print "failed validating file"
						print filebuffer
						filebuffer = ''
						ser.write(":RECV_FAIL\n")
			except KeyboardInterrupt:
				raise DoneException
			#except:
				print "malformatted command: " + tempsp[0]
	if connected and conntimer + 5 < time.time():
		connected = False
		print "timeout; connection lost"

def main():
	while True:
		try:
			mainloop()
		except DoneException:
			print "exiting......"
			return

if __name__ == '__main__':
	main()
