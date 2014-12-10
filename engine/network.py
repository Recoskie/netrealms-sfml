class Connection():
	import socket
	import netcmd

	def __init__(address, port):
		connect(address, port)

	def connect(self, address, port):
		self.sock = socket.socket()
        self.sock.connect((address, port))

	def disconnect(self):
		self.sock.close()
		pass

	def recieve(self, data):
        data = self.sock.recv(4096).split("\n".encode('latin-1'))
        for line in data:
            if len(line) > 0:
                if str(line).startswith("PING"):
                    self.send("PONG")
                else:
                    rawmsg = line.decode('latin-1').split(" ")
                    nick = rawmsg[0].split(":")[1].split("!")[0]
                    msg = ' '.join(rawmsg[3:])[1:]
                    source = rawmsg[2]
                    args = msg.split(" ")[1:]
                    self.receive(msg, nick, source)

			        for command in self.cmds.commandStrings:
			            if data.startswith(command):
							self.cmds.commandFunctions[self.cmds.commandStrings.index(command)](self.cmds, msg, nick, source)
			                break

	def send(self, msg):
    	self.sock.send((msg.replace("\n", "").replace("\r", "") + "\r\n").encode())

    def globalChat(self, msg):
        for line in msg.split("\n"):
            self.send("GCHAT :" + line)

    def mapChat(self, msg):
         for line in msg.split("\n"):
            self.send("MCHAT :" + line)

   	def privateChat(self, to, msg):
        for line in msg.split("\n"):
            self.send("PCHAT " + to + " :" + line)