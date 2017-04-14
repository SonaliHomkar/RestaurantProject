from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi

## import database and sqlalchemy for CRUD operations ##
from database_setup import Base,Restaurant,MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## create session and connect to database ##
engine = create_engine('sqlite:///restaurantNew.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type' , 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s</h1>" % myRestaurantQuery.name
                    output += "<form method = 'POST' enctype= 'multipart/form-data' action='/restaurant/%s/delete'>" % restaurantIDPath
                    output +=  "<input type='submit' value='Delete'>"
                    output += "<a href='/restaurant'>Cancel</a>"
                    output += "</form></html></body>"

                    self.wfile.write(output)
                
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type' , 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>"+ myRestaurantQuery.name +"</h1>"
                    output += "<form method = 'POST' enctype= 'multipart/form-data' action='/restaurant/%s/edit'>" % restaurantIDPath
                    output += "<input type='text' name='txtRestaurantName' placeholder = '%s'>" % myRestaurantQuery.name
                    output +=  "<input type='submit' value='Rename'>"
                    output += "<a href='/restaurant'>Cancel</a>"
                    output += "</form></html></body>"

                    self.wfile.write(output)
                    print(output)
                
            if self.path.endswith("/restaurant"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurant/new'><b>Make a new Restaurant</b></a><br>"
                for i in restaurants:
                    output += "<b>" + i.name + "</b>"
                    output += "<br>"
                    output += "<a href='/restaurant/%s/edit' >Edit </a>" % str(i.id)
                    output += "<br>"
                    output += "<a href='/restaurant/%s/delete' >Delete </a>" % str(i.id)
                    output += "<br><br>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<form method = 'POST' enctype= 'multipart/form-data' action='/restaurant/new'>"
                output += "<input type='text' name='txtRestaurantName'><input type='submit' value='submit'>"
                output += "<br><a href='/restaurant'>Cancel</a>"
                output += "</form></html></body>"

                self.wfile.write(output)
                print output
                
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2><input name='message'"
                output += " type='text'><input type='submit' value='submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hola!<a href='/hello'>Back to Hello page</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2><input name='message'"
                output += " type='text'><input type='submit' value='submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except IOError:
                self.send_error(404,"File not found error %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                restaurantIdPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('content-type','text/html')
                    self.send_header('Location','/restaurant')
                    self.end_headers()
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('txtRestaurantName')

                newrestaurant = Restaurant(name = messagecontent[0])
                session.add(newrestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('content-type','text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('txtRestaurantName')
                    
                restaurantIdPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()

                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('content-type','text/html')
                    self.send_header('Location','/restaurant')
                    self.end_headers()
                
            if self.path.endswith("\hello") or self.path.endswith("\hola"):
                self.send_response(301)
                self.send_header('content-type','text/html')
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('message')

                output =  ""
                output += "<html><body"
                output += " <h2> ok ....how about this</h2>"
                output += "<h1> %s <h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2><input name='message'"
                output += " type='text'><input type='submit' value='submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)   
        except:
            pass
    
                


def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    
    except KeyboardInterrupt:
        print "^C entered, stopping web server"
        server.socket.close()
if __name__ == '__main__':
    main()
