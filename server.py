import json
import os
import socket
import struct
import time
from web3 import Web3 , HTTPProvider , IPCProvider , WebsocketProvider
#from solc import compile_source , compile_files
from web3.contract import ConciseContract
import getpass
import os
import time

def GetTime():
	return time.strftime('%m-%d-%H-%M',time.localtime(time.time())).split('-')

def get_time():
	return time.strftime('%m-%d-%H',time.localtime(time.time()))

#打开文件函数
def file_open():
    #打开文件,读取文件内容
    #print(file_object.name)
    mid_str = str(get_time())
    #print(GetTime())
    file_name_log = "NewIDS-" + mid_str + ".log"
    print("日志名：" + file_name_log)
	#file_object = open(file_name_log, "rb")
    file_object = open('NewIDS-06-07-10.log',"rb")
    file_object.seek(0)
    buff_mid = file_object.read()
    buff = str(buff_mid).replace('\\n','\r\n')
    buff = buff.replace('\\','')
    file_object.close()
    return bytes(buff,"ascii")

#账号解密交互
def pass_account(web3,flag):
	if flag == -1:
		while 1:
			if flag > 0:
				#print("Login succeed")
				break
			elif flag == -1:
				personal_password = "rapha"
				#personal_password = getpass.getpass("Input your password:")
			else:
				personal_password = "rapha"
				#personal_password = getpass.getpass("False password!Input your password:")
			flag = web3.personal.unlockAccount(web3.eth.accounts[0],personal_password)
		else :
			flag = web3.personal.unlockAccount(web3.eth.accounts[0],personal_password)

		web3.eth.defaultAccount = web3.eth.accounts[0]

def load_up(web3,read_buff):
    #开始挖矿,将读取的内容传递到区块链上
    #web3.miner.setEtherbase(eth.accounts[0])
    #print(web3.eth.coinbase)
	web3.miner.start(4)

	return_address = web3.eth.sendTransaction({'from':web3.eth.accounts[0],'to':web3.eth.accounts[1],\
                                            'value':web3.toWei(1,"wei"),'data':web3.toHex(read_buff)})
    #print(web3.toHex(return_address))
	while 1:
		mid = web3.eth.getTransaction(return_address)
		if mid.blockNumber != None:
			web3.miner.stop()
			break

def RecvLog():
	ip_port = ('10.255.1.41', 12352)
	sk = socket.socket()
	sk.bind(ip_port)
	sk.listen(1)

	buffer = 1024
	conn, addr = sk.accept()
	pack_len = conn.recv(4)

	head_len = struct.unpack('i', pack_len)[0]
	json_head = conn.recv(head_len).decode('utf-8')
	head = json.loads(json_head)
	filesize = head['filesize']
	print(head['filename'])
	with open(head['filename'], 'w') as f:
		while filesize:
			#print(filesize)
			if filesize >= buffer:
				content = conn.recv(buffer)
				filesize -= buffer
				f.write(str(content))
			else:
				content = conn.recv(filesize)
				print ('接收成功!')
				f.write(str(content))
				break
	conn.close()
	sk.close()

def main():

	# sign = False
	# RecvLog()
	web3 = Web3 ( HTTPProvider ( 'http://localhost:8545' ))
	if web3:
		print("web3连接成功!")
	else:
		print("web3连接失败!")
	flag = -1
	#
	read_buff = file_open()
	#
	pass_account(web3,flag)
	#
	load_up(web3,read_buff)

	# while True:
	# 	minute = int(GetTime()[3])
	# 	if(54<minute < 57):
	# 		RecvLog()
	# 		web3 = Web3 ( HTTPProvider ( 'http://localhost:8545' ))
	# 		if web3:
	# 			print("Connection succeed!")
	# 		else:
	# 			print("Connection failed!")
	# 		flag = -1
	#
	# 		read_buff = file_open()
	#
	# 		pass_account(web3,flag)
	#
	# 		load_up(web3,read_buff)
	# 	else :
	# 		sign = False
	# 	time.sleep(60)

if __name__ == '__main__':		
	main()
