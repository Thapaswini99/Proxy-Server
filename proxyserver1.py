import socket
import thread
import sys
import os
CRLF = "\r\n\r\n"
BACKLOG = 10
MAX_DATA_RECV = 999999
data1  = ""
flag = 1
files = 0
dict1 = {}
dict2 = {}
dict3 = {}
file_path = "cache"
#directory = os.path.dirname(file_path)
if not os.path.exists(file_path):
	 os.makedirs(file_path)

class ProxyServer:
	def __init__(self, host, port):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((host, port))
		self.socket.listen(BACKLOG)

	def connectionFromClient(self):
		while True:
			conn, client_addr = self.socket.accept()
			thread.start_new_thread(self.proxythread, (conn, client_addr))
		self.socket.close()

	def proxythread(self, conn, client_addr):
		host = " "
		port = -1
		request = conn.recv(MAX_DATA_RECV)
		print(request)
		print("##########################################################################################################")
		message = request.split(' ')
		#filename = message[1].split("/")[3]
		if(message[0] == "GET"):
			list1 = message[1].split('/')
			path = list1[3]
			port_pos = list1[2].find(":")
			list1 = list1[2].split(":")
			host = list1[0]

			if(port_pos == -1):
				port = 80
				port_pos = message[1].split('/')
				host = port_pos[2]
				path = host
			else:
				port = int(list1[1])
		#print(request)

		try:
			# create a socket to connect to the web server
			global files,flag,dict1,dict2,dict3

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host, port))
			data1=''
			if dict2.get(path):
				s.send("GET /%s HTTP/1.1\r\nHOST: %s\r\nIf-Modified-Since: %s%s" % (path, host, dict2[path], CRLF))         # send request to webserver
			else:
				s.send("GET /%s HTTP/1.1\r\nHOST: %s%s" % (path, host, CRLF))
			while 1:
				data = s.recv(MAX_DATA_RECV)
				data1+=data
				#f.write(data)
				if not data:
					break
			data9 = data1.split("\r\n")[0].split(" ")[1]
			#print("yoooooooooooooooooooooooooooo")
			print(data1)
			if data9 == "200":
				conn.send(data1)
				data10 = data1.split("\r\n")[8]
				data11 = data1.split("\r\n")[2].split(" ")[5]
				data12 = data1.split("\r\n")[2].split(": ")[1].split(":")
				len4=len(data12[0])
				if dict1.get("cache/f1") == path or dict1.get("cache/f2") == path or dict1.get("cache/f3") == path:
					final_date=data11.split(':')
					hours=(int) (final_date[0])
					mins=(int) (final_date[1])
					mins=(mins+30)
					if(mins>60):
						hours+=mins/60
						mins=mins%60
					hours+=5
					dict2[path]=data12[0][:len4-2]
					dict2[path]+=(str) (hours)
					dict2[path]+=':'+(str) (mins)
					dict2[path]+=':'+final_date[2]
					dict2[path]+= " GMT"
				print(dict1.get("cache/f1"))
				if dict1.get("cache/f1") == path:
					print("Modified and storing in cache")
					try:
						f = open("cache/f1",'w')
					except:
						print("error opening the file")
					f.write(data10)
					f.close()
				elif dict1.get("cache/f2") == path:
					print("Modified and stroing in cache")
					try:
						f = open("cache/f2",'w')
					except:
						print("error opening the file")
					f.write(data10)
					f.close()
				elif dict1.get("cache/f3") == path:
					print("Modified and storing in cache")
					try:
						f = open("cache/f3",'w')
					except:
						print("error opening the file")
					f.write(data10)
					f.close()
			if data9 == "304":
				print("not-modified")
				if dict1.get("cache/f1") == path:
					try:
						f = open("cache/f1",'rb')
					except:
						print("error opening the file")
					l = f.read(1024)
					while(l):
						conn.send(l)
						l = f.read(1024)
					f.close()
				elif dict1.get("cache/f2") == path:
					f = open("cache/f2",'rb')
					l = f.read(1024)
					while(l):
						conn.send(l)
						l = f.read(1024)
					f.close()
				elif dict1.get("cache/f3") == path:
					try:
 						f = open("cache/f3",'rb')
					except:
						print("error opening the file")
 					l = f.read(1024)
					while(l):
						conn.send(l)
						l = f.read(1024)
					f.close()
			s.close()
			conn.close()
			print(len(data1.split("\r\n")))
			if len(data1.split("\r\n"))>8:
				data4 = data1.split("\r\n")[6].split(": ")[1]
				dict3[path] = data4
			if dict2.get(path)==None and dict3.get(path)!="no-cache" and len(data1.split("\r\n"))>8:
				print("Store in cache")
				fn = "cache/"+"f"+str(flag)
				if files > 3:
					del dict2[dict1[fn]]
					del dict3[dict1[fn]]
				f = open(fn,"w")
				#print(data1.split("\r\n"))
				data2 = data1.split("\r\n")[8]
				data3 = data1.split("\r\n")[2].split(" ")[5]
				data5 = data1.split("\r\n")[2].split(": ")[1].split(":")
				len4=len(data5[0])
				f.write(data2)
				f.close()
				dict1[fn] = path
				print(data3)
				final_date=data3.split(':')
				hours=(int) (final_date[0])
				mins=(int) (final_date[1])
				mins=(mins+30)
				if(mins>60):
					hours+=mins/60
					mins=mins%60
				hours+=5
				dict2[path]=data5[0][:len4-2]
				dict2[path]+=(str) (hours)
				dict2[path]+=':'+(str) (mins)
				dict2[path]+=':'+final_date[2]
				dict2[path]+= " GMT"
				flag=flag%3+1
				files = files+1
		except socket.error, (value, message):
			if s:
				s.close()
			if conn:
				conn.close()
			sys.exit(1)

if __name__ == '__main__':
    server = ProxyServer("localhost", 12345)
    server.connectionFromClient()
