## might be an older version

import serial, sys, os, time, hashlib, random

BLOCKSIZE = 256

if len(sys.argv) != 3:
	print "usage: {} <serial port> <file>".format(sys.argv[0])
	sys.exit(1)
else:
	sportname = sys.argv[1]
	filename = sys.argv[2]

if not os.path.exists(filename):
	print "file does not exist"
	sys.exit(2)

try:
	ser = serial.Serial(sportname,57600,timeout=0.1)
except:
	print "serial port initialization failed"
	sys.exit(3)

class DoneException:
	pass

nodename = "s" + str(random.randint(10000,1000000))
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
clientid = ''

def mainloop():
	global connected, timer, inbuffer, conntimer, clientid
	if not connected:
		if timer + 5 < time.time(): # send discover every 5 seconds
			timer = time.time()
			print "not connected, sending discovery message"
			ser.write(b':DISCOVER\n')
	inbuffer += ser.read(8)
	tempsp = inbuffer.split('\n',1)
	if len(tempsp) > 1:
		cmd = tempsp[0].split()
		inbuffer = tempsp[1]
		if cmd[0][0] == ':':
			try:
				print "recieved command: " + tempsp[0]
				if cmd[0] == ":CLIENT":
					if not connected:
						connected = True
						clientid = cmd[1]
						print "client discovered: " + clientid + ", replying..."
						ser.write(b':SERVER ' + nodename + '\n')
					conntimer = time.time()
				elif cmd[0] == ":READY":
					ser.write(b':FILENAME ' + filename + '\n')
					conntimer = time.time()
				elif cmd[0] == ":FILESTAT":
					if cmd[1] == 'true': # file exists
						fn = os.path.join(os.getcwd(),filename)
						fv = open(fn,'rb').read()
						m = hashlib.md5()
						m.update(fv)
						if len(fv) == int(cmd[2]) and m.hexdigest() == cmd[3]:
							print "remote file up to date ({})".format(cmd[3])
						else:
							print "remote file out of date ({}), requesting sync".format(cmd[3])
							ser.write(b':SYNC\n')
					else:
						print "remote file does not exist, requesting sync"
						ser.write(b':SYNC\n')
					conntimer = time.time()
				elif cmd[0] == ":READY_SYNC":
					print "syncing..."
					fn = os.path.join(os.getcwd(),filename)
					fv = open(fn,'rb').read()
					mh = hashlib.md5()
					mh.update(fv)
					error = False
					timeout = time.time() + 10
					while fv and not error and time.time() < timeout:
						temp = fv[:BLOCKSIZE]
						fv = fv[BLOCKSIZE:]
						m = hashlib.md5()
						m.update(temp)
						ser.write(b':DATA {} {} {}\n'.format(BLOCKSIZE,m.hexdigest(),hexs(temp)))
						newcmd = False
						while not newcmd and time.time() < timeout:
							inbuffer += ser.read(8)
							tempsp = inbuffer.split('\n',1)
							if len(tempsp) > 1:
								newcmd = True
								cmd = tempsp[0].split()
								print "recieved command: " + tempsp[0]
								timeout = time.time() + 10
								inbuffer = tempsp[1]
								if cmd[0] == ':SUCCESS':
									print "successfully transferred data"
								elif cmd[0] == ':RETRY':
									fv = temp + fv
									print "failed sending data, retrying"
								else:
									error = True
					if not error:
						ser.write(b':DONE {} {}\n'.format(mh.hexdigest(),filename))
					conntimer = time.time()
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
