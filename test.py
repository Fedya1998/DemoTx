import telebot
from db import *
from tx import *
import re
import sys
db=DB("./db.sqlite")
'''
db.update_user(1, 0, "a", "b")
print("Users:\n")
db.view_users()
db.update_user(2, 0, "a", "b")
db.update_user(1, 0, "aaaa", "b")
db.view_users()
'''
API_KEY = sys.argv[1]
bot = telebot.TeleBot(API_KEY, parse_mode=None)

@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.reply_to(message, "/start to reset")

@bot.message_handler(commands=['start'])
def send_something(message):
	bot.reply_to(message, "the dialogue has been reset")
	db.update_user(message.chat.id, 0, "", "", 0, "", "", "", "", 0, 0, 0)
	print("reset", db.get_user(message.chat.id))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	user = db.get_user(message.chat.id)
	if message.text.lower() == "send" and user[1] == 0:
		db.update_field(message.chat.id, "step", 1)
		print("update", db.get_user(message.chat.id))
		bot.reply_to(message, "send me the source chain of [rin, rop] for Rinkeby and ropsten")
	elif user[1] == 1:
		#get source chain
		if message.text.lower() == "rin":
			db.update_field(message.chat.id, "source_ch", "rin")
			db.update_field(message.chat.id, "step", 2)
			bot.reply_to(message, "nice, send me the dest chain")
		elif message.text.lower() == "rop":
			db.update_field(message.chat.id, "source_ch", "rop")
			db.update_field(message.chat.id, "step", 2)
			bot.reply_to(message, "nice, send me the dest chain")
		else:
			bot.reply_to(message, "send me the source chain of [rin, rop] for Rinkeby and ropsten please")
	elif user[1] == 2:
		if message.text.lower() == "rin":
			db.update_field(message.chat.id, "dest_ch", "rin")
			db.update_field(message.chat.id, "step", 3)
			bot.reply_to(message, "we got you, send me your source address")
		elif message.text.lower() == "rop":
			db.update_field(message.chat.id, "dest_ch", "rop")
			db.update_field(message.chat.id, "step", 3)
			bot.reply_to(message, "we got you, send me your source address")
		else:
			bot.reply_to(message, "send me the dest chain of [rin, rop] for Rinkeby and ropsten please")
	elif user[1] == 3:
		if re.match("0x[a-fA-F0-9]{40}$", message.text):
			db.update_field(message.chat.id, "source_ad", message.text[:42])
			db.update_field(message.chat.id, "step", 4)
			bot.reply_to(message, "we got you, send me your dest address")
		else:
			bot.reply_to(message, "eth address /^0x[a-fA-F0-9]{40}$/ please")
	elif user[1] == 4:
		if re.match("0x[a-fA-F0-9]{40}$", message.text):
			db.update_field(message.chat.id, "dest_ad", message.text[:42])
			db.update_field(message.chat.id, "step", 5)
			bot.reply_to(message, "how much would you like to send")
		else:
			bot.reply_to(message, "eth address /^0x[a-fA-F0-9]{40}$/ please")
	elif user[1] == 5:
		if float(message.text):
			db.update_field(message.chat.id, "value", float(message.text))
			db.update_field(message.chat.id, "step", 6)
			bot.reply_to(message, "we got you. Now our validators will generate a bridge address using your address")
			bot.send_message(message.chat.id, "0xeB75f110985Ed415dD396eb96D617483Bdacddb0")
			bot.send_message(message.chat.id, "send your amount to that address and send me your txid")

		else:
			bot.reply_to(message, "please send a float value")
	elif user[1] == 6:
		#validate txid
		bot.send_message(message.chat.id, f"now imagine that ypu are a validator (1 of 3). You need to check if the transaction with id {message.text} is ok. Type yes if ok and no if not ok")
		db.update_field(message.chat.id, "step", 7)
	elif user[1] == 7:
		if message.text.lower() == "yes":
			db.update_field(message.chat.id, "val1", 1)
			db.update_field(message.chat.id, "step", 8)
			bot.send_message(message.chat.id, "now imagine that ypu are a validator (2 of 3). Type yes if ok and no if not ok")
		elif message.text.lower() == "no":
			db.update_field(message.chat.id, "val1", 0)
			db.update_field(message.chat.id, "step", 8)
			bot.send_message(message.chat.id, "now imagine that ypu are a validator (2 of 3). Type yes if ok and no if not ok")
		else:
			bot.reply_to(message, "please send yes or no")
	elif user[1] == 8:
		if message.text.lower() == "yes":
			db.update_field(message.chat.id, "val2", 1)
			db.update_field(message.chat.id, "step", 9)
			bot.send_message(message.chat.id, "now imagine that ypu are a validator (2 of 3). Type yes if ok and no if not ok")
		elif message.text.lower() == "no":
			db.update_field(message.chat.id, "val2", 0)
			db.update_field(message.chat.id, "step", 9)
			bot.send_message(message.chat.id, "now imagine that ypu are a validator (3 of 3). Type yes if ok and no if not ok")
		else:
			bot.reply_to(message, "please send yes or no")

	elif user[1] == 9:
		if message.text.lower() in ["yes", "no"]:
			if message.text.lower() == "yes":
				db.update_field(message.chat.id, "val3", 1)
			else:
				db.update_field(message.chat.id, "val3", 0)
			db.update_field(message.chat.id, "step", 10)
			u = db.get_user(message.chat.id)
			total = u[9] + u[10] + u[11]
			bot.send_message(message.chat.id, f"total {total} of 3, 2/3 required by protocol")
			if total >= 2:
				bot.send_message(message.chat.id, f"your transaction has been confirmed. Now please wait while we send a transaction to the destination chain")
				network = u[3]
				value = u[4]
				dest = u[6]
				txid = send_ether(network, value, dest)
				db.update_field(message.chat.id, "dest_tx", txid)
				bot.send_message(message.chat.id, f"your transaction txid {txid}. Thank you for using Axelar. Type /start to start over")
			else:
				bot.send_message(message.chat.id, f"your transaction has not been confirmed. Please send the proper txid")
				db.update_field(message.chat.id, "step",6)
		else:
			bot.reply_to(message, "please send yes or no")







#print(db.get_user(1))
bot.polling(none_stop=True)
