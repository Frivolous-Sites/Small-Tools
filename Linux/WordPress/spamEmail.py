#!/usr/bin/python3

import mysql.connector
import sys
import urllib.request
import re
import argparse

parser = argparse.ArgumentParser(description='SPAM CHECKER')
parser.add_argument('-e','--email', help='Email to be checked', required=False)
args = vars(parser.parse_args())


def testSpam(email, NUM):
        req = urllib.request.Request("https://cleantalk.org/blacklists/" + str(email))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')
        fp = urllib.request.urlopen(req)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")

        WEBSITE = str(re.findall('<body>(.*?)</body>', mystr, re.DOTALL))
        if " reported as spam" in WEBSITE:
                print(email, flush=True)
                NUM += 1
        fp.close()
        del WEBSITE
        return NUM


if args['email']:
        output = testSpam(str(args['email']), 0)
else:
        # open a database connection
        # be sure to change the host IP address, username, password
        # and database name to match your info
        #
        connection = mysql.connector.connect (host = "127.0.0.1", user = "wppps", passwd = "whatever", db = "wp_wp")

        # prepare a cursor object using cursor() method
        cursor = connection.cursor ()

        # execute the SQL query using execute() method.
        cursor.execute ("select user_email from wp_users")

        # fetch all of the rows from the query
        data = cursor.fetchall ()

        output = 0;

        if len(data) > 10:
                numExam = 10
        else:
                numExam = len(data)

        for ni in range(2,12):
                ROW = str(data[ni])[2:-3]
                output = testSpam(ROW, output)

        # close the cursor object
        cursor.close ()

        # close the connection
        connection.close ()

print(output)
sys.exit()

#pip3 install mysql.connector
