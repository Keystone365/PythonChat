#!/usr/bin/env python3
import csv
    

def CheckLogin():
	
	with open('users.csv', 'rt') as csvfile:
		userReader = csv.reader(csvfile)
		for row in userReader: 
			print (', '.join(row))
	
if __name__ == '__main__':
   
    CheckLogin()   
   
    exit(0)  # return 0 for successful completion