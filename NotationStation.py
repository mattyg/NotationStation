#!/usr/bin/python
# This is the Notation Station!

# TODO:
# 1. add note
# 2. remove note
# 3. view note (by date, priority)
# 4. edit note
# 5. commandline syntax NotationStation --add, --delete, --edit, --view

# INSTALLATION NOTES
# 1. Download and install CocoaDialog.
# 2. Set USER CONFIG options below:

# USER CONFIG
DEFAULT_PRIORITY = 0
DATABASE_PATH = '/Users/matt/CodingProjects/NotationStation/storage.db'
COCOADIALOG_PATH = '/Applications/CocoaDialog.app/Contents/MacOS/CocoaDialog'

import sqlite3,subprocess,sys,string,datetime,os

class Notes:
	connection = None
	cursor = None
	
	def __init__(self,database=DATABASE_PATH):
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()
	
	def close(self):
		self.cursor.close()
		
	def add(self,text='',priority=DEFAULT_PRIORITY):
		dtnow = datetime.datetime.now().isoformat(' ')
		query = "INSERT INTO notes (text,datetime,priority) VALUES (\"%s\",\"%s\",%i)" %(text,dtnow,priority)
		self.cursor.execute(query)
		self.connection.commit()
		
	def remove(self,id):
		pass
		
	def edit(self,id):
		pass
		
	def view(self,query=""):
		if query == "": # view all
			query = "SELECT * FROM notes ORDER BY datetime DESC"
			self.cursor.execute(query)
		else: # view by parameters
			query = "SELECT * FROM notes WHERE %s ORDER BY datetime DESC" %(query)
			self.cursor.execute(query)
		notes = self.cursor.fetchall()
		# show notes
		tempdate = ""
		tempdt = ""
		for note in notes:
			#read date and time
			date =  str(note[1])[:10]
			time = str(note[1])[11:][:5]
			dt = note[1][:16]
			#get day of week from date
			datedt = datetime.datetime.strptime(date,"%Y-%m-%d")
			weekday = datedt.weekday()
			weekdays = ["Mon","Tues","Wed","Thurs","Fri","Sat","Sun"]
			weekday = weekdays[weekday]
			
			if date != tempdate:
				# echo "\033[1;36mWoot\033[m"    prints blue
				# echo "\033[1;32mWoot\033[m" -- prints green
				os.system("echo \"==================================================================================================================\"")
				weekdate = "+  "+weekday+", "+date[5:]
				os.system("echo \"\033[1;36m%s\033[m\" \"\033[0;38\033[m\"" %(weekdate))
				os.system("echo \"==================================================================================================================\"")
				tempdate = date
				
			if dt != tempdt:
				os.system("echo \"\033[1;36m%s\033[m\" \"\033[0;38\033[m\"" %(time))
				tempdt = dt
			os.system("echo \"%s\"" %(note[2]))
			os.system("echo \"------------------------------------------------------------------------------------------------------------------\"")
			
		pass
	
class NotationStation:
	Notes = None
	
	def __init__(self):
		#inititalize database:
		self.Notes = Notes()
		# read input from command line
		function = sys.argv[1]
		# run function with parameters
		if function == "add":
			self.addnote()
		elif function == "edit":
			self.editnote()
		elif function == "remove":
			self.removenote()
		elif function == "prioritize":
			self.prioritizenote()
		elif function == "view":
			self.Notes.view()
		self.Notes.close()
		
	def addnote(self):
		output=subprocess.Popen([COCOADIALOG_PATH,"textbox","--button1","Save","--button2","Cancel","--editable","-float","--title","New Note"],stdout=subprocess.PIPE).communicate()[0]
		if output[0] == "1":
			# add item to db
			self.Notes.add(string.strip(output[1:]))
		
	def editnote(self):
		pass
	
	def removenote(self):
		pass
	
	def prioritizenote(self):
		pass
		
NotationStation()