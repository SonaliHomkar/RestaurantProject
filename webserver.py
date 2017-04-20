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
                    output += "<b><a href='/restaurant/%s/Menu'>Menu </a>" % str(i.id) 
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
            # 19 Apr code #
            if self.path.endswith("/Menu"):
                resturantId = self.path.split("/")[2]
                Menuitems = session.query(MenuItem).filter_by(restaurant_id = resturantId).all()
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurant/%s/newMenu'><b> Add a new Menu</b></a><br>" % resturantId
                output += "<a href='/restaurant'><b> Cancel</b></a><br>"
                if Menuitems != []:
                    for i in Menuitems:
                        output += "<b>" + i.name + "</b>" 
                        output += "<br>"
                        output += "<a href='/restaurant/%s/editMenu' >Edit </a>" % str(i.id)
                        output += "<br>"
                        output += "<a href='/restaurant/%s/deleteMenu' >Delete </a>" % str(i.id)
                        output += "<br><br>"
                else:
                    output += "<b> No MenuItems found..please add it</b>" 
                output += "</body></html>"

                self.wfile.write(output)
                print output

            if self.path.endswith("/newMenu"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                resturantid = self.path.split("/")[2]
                output = ""
                output += "<html><body>"
                output += "<form method = 'POST' enctype= 'multipart/form-data' action='/restaurant/%s/newMenu'>" % str(resturantid)
                output += "<table><td colspan =3><b>Menu Item</b></td>"
                output += "<tr><td>Name</td><td>:</td><td><input type='text' name='txtMenuItemName'></td></tr>"
                output += "<tr><td>Description</td><td>:</td><td><input type='text' name='txtDescription'></td></tr>"
                output += "<tr><td>Price</td><td>:</td> <td><input type='text' name='txtPrice'></td></tr>"
                output += "<tr><td>Course</td><td>:</td><td><input type='text' name='txtCourse'></td></tr>"
                output += "<tr><td><a href='/restaurant/%s/Menu'>Cancel</a></td><td><input type='submit' value='submit'></td></tr>" % str(resturantid) 
                output += "</table>"
                output += "</form></html></body>"

                self.wfile.write(output)
            #end 19 Apr code #
            # start 20 apr code #
            if self.path.endswith("/editMenu"):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()

                menuId = self.path.split("/")[2]
                MenuItems = session.query(MenuItem).filter_by(id = menuId).all()
                output = ""
                output += "<html><body>"
                output += "<form method = 'POST' enctype= 'multipart/form-data' action='/restaurant/%s/editMenu'>" % str(menuId)
                if MenuItems != []:
                    for i in MenuItems:
                        output += "<table><td colspan =3><b>Menu Item</b></td>"
                        output += "<tr><td>Name</td><td>:</td><td><input type='text' name='txtMenuItemName' placeholder='%s'></td></tr>" % i.name
                        output += "<tr><td>Description</td><td>:</td><td><input type='text' name='txtDescription' placeholder='%s'></td></tr>" % i.description
                        output += "<tr><td>Price</td><td>:</td> <td><input type='text' name='txtPrice' placeholder='%s'></td></tr>" % i.price
                        output += "<tr><td>Course</td><td>:</td><td><input type='text' name='txtCourse' placeholder='%s'></td></tr>" % i.course
                        output += "<tr><td><a href='/restaurant/%s/Menu'>Cancel</a></td><td><input type='submit' value='submit'></td></tr>" % str(i.restaurant_id)
                else:
                   output += "<b>No details found</b>" 
                output += "</table>"
                output += "</form></html></body>"

                self.wfile.write(output)
                
            # end 20 apr code #
            # start 20 apr code #
            if self.path.endswith("/deleteMenu"):
                menuId = self.path.split("/")[2]
                menuItemquery = session.query(MenuItem).filter_by(id = menuId).one()
                if menuItemquery != []:
                    self.send_response(200)
                    self.send_header('content-type' , 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to Menu item %s</h1>" % menuItemquery.name
                    output += "<form method = 'POST' enctype= 'multipart/form-data' action='/restaurant/%s/deleteMenu'>" % menuId
                    output +=  "<input type='submit' value='Delete'>"
                    output += "<a href='/restaurant/%s/Menu'>Cancel</a>" % menuItemquery.restaurant_id
                    output += "</form></html></body>"

                    self.wfile.write(output)
                
            # end 20 apr code #
                
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
            # 19 Apr code #
            if self.path.endswith("/newMenu"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    fldname = fields.get('txtMenuItemName')
                    flddescription = fields.get('txtDescription')
                    fldprice = fields.get('txtPrice')
                    fldcourse = fields.get('txtCourse')
                    restaurantId = self.path.split("/")[2]

                    NewMenuItemQuery = MenuItem(name = fldname[0], description = flddescription[0],
                                                price = fldprice[0], course = fldcourse[0], restaurant_id = restaurantId )
                    session.add(NewMenuItemQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('content-type','text/html')
                    self.send_header('Location','restaurant/%s/Menu' % str(restaurantId))
                    self.end_headers()
            # end 19 Apr code #
            # start 20 apr code #
            if self.path.endswith("/editMenu"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    fldname = fields.get('txtMenuItemName')
                    flddescription = fields.get('txtDescription')
                    fldprice = fields.get('txtPrice')
                    fldcourse = fields.get('txtCourse')
                    menuItemId = self.path.split("/")[2]
                    editMenuItemQuery = session.query(MenuItem).filter_by(id = menuItemId).one()
                    restaurantId = editMenuItemQuery.restaurant_id
                    if editMenuItemQuery != []:
                        editMenuItemQuery.name = fldname[0]
                        editMenuItemQuery.description = flddescription[0]
                        editMenuItemQuery.price = fldprice[0]
                        editMenuItemQuery.course = fldcourse[0]
                        session.add(editMenuItemQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('content-type','text/html')
                        self.send_header('Location','/restaurant/%s/Menu' % str(restaurantId))
                        self.end_headers()
            # end 20 apr code #
            # start 20 apr code #
            if self.path.endswith("/deleteMenu"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                menuId = self.path.split("/")[2]
                menuDeleteQuery = session.query(MenuItem).filter_by(id = menuId).one()

                if menuDeleteQuery != []:
                    session.delete(menuDeleteQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('content-type','text/html')
                    self.send_header('Location','/restaurant')
                    self.end_headers()
                
            # end 20 apr code #
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
