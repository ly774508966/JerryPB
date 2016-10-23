''' 
function	: XMLDeleter 
Author		: tangrui
Date		: 2014/10/09
Description : You can run this script directly, then you will auto-remove lable "[global::System.Xml.Serialization.XmlIgnore]"
			  You can also use XMLDeleter function. it's argument is your target path or filename. Good Luck!!!
'''

import os
import sys

pattern = '[global::System.Xml.Serialization.XmlIgnore]'
target  = '//Here has been replaced by XXMMLLDeleter'


def XMLDeleter(file):
	try:
		if os.path.isfile(file) and file.endswith('.cs'):
			with open(file ,'r') as code:
				text = code.read()
				code.close()

			count = text.count(pattern)
			if count > 0:
				with open(file ,'w') as code:
					text = text.replace(pattern, target)
					code.write(text)
					print ("file: %s \n %d lines modified\n" %(file,count))

		elif os.path.isdir(file):
			list = os.listdir(file)
			print ("Changing in path %s" %file)
			for filename in list:
				fullname = os.path.join(file,filename)
				XMLDeleter(fullname)
	except Exception as ex:
		print('An error as happened when try to change file %s ,please press any key to try again', file)
		print("and contact this script's author")
		print('error: %s', ex)
		os.system('pause');
		XMLDeleter(file)
	finally:
		pass
if __name__ == '__main__':
	if len(sys.argv) > 1:
		for i in range(1, len(sys.argv)):
			XMLDeleter(sys.argv[i])
	else:
		XMLDeleter('../../client/game/client/Assets/Code/Network')