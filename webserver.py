#
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import csv
import re

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            namepattern = '[/](\d*\.\d*)x(\d*\.\d*)x(\d*\.\d*)x(\d*)\.json'
            regexpattern = re.compile(namepattern)
            params = regexpattern.search(self.path)
            if params != None:
                params = params.groups()
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                sqlDB = sqlite3.connect('lidardb.sq3')
                me_x = float(params[0])
                me_y = float(params[1])
                me_z = float(params[2])
                n_points = int(params[3])
                c = sqlDB.cursor()
                sqlquery = 'select pos_x,pos_y,pos_z, ((pos_x-%f)*(pos_x-%f)+(pos_y-%f)*(pos_y-%f)+(pos_z-%f)*(pos_z-%f)) as dst from points LIMIT %d'%(me_x,me_x,me_y,me_y,me_z,me_z,n_points)
                c.execute(sqlquery)
                self.wfile.write(sqlquery)
                self.wfile.write('[')
                for row in c:
                    self.wfile.write('%f,%f,%f\n'%(row[0:3]))
                self.wfile.write(']')
                return
            else:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            self.send_response(200)
            self.end_headers()
            self.wfile.write("<HTML>POST OK.<BR><BR>");           
        except :
            pass

def loadPoints():
    sqlDB = sqlite3.connect('lidardb.sq3')
    c = sqlDB.cursor()
    c.execute('DROP TABLE IF EXISTS points')
    c.execute('''create table points (pos_x real, pos_y real, pos_z real)''')
    dr = csv.reader(open('lidarfile.txt'), delimiter=' ')
    for i in dr:
        try:
            rowinfo = (float(i[0]), float(i[1]), float(i[2]))
            c.execute("insert into points (pos_x, pos_y,pos_z) values (?, ?,?);", rowinfo)
        except:
            pass
    c.execute('select count(*) from points')
    print '%d Datapoints availible'%(c.fetchone()[0])
    sqlDB.commit()
    c.close()

def main():
    #loadPoints()    
    try:
        server = HTTPServer(('', 1642), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

