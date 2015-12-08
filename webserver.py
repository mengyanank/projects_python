from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import *
from sqlalchemy.orm import sessionmaker


DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
   

    def do_GET(self):
        try:

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rets=session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create a new Restaurant</a><br><br>"
                output += "<br>"
                for r in rets:
                    output += r.name
                    output+="<br>"
                    output+="<a href='/restaurants/%s/edit'>edit</a><br>" % r.id
                    output+="<a href='/restaurants/%s/delete'>delete</a><br>" % r.id
                    output+="<br><br>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                words=self.path.split('/')
                number=words[2]
                output = ""
                output += "<html><body>"
                output += "<h1>Change the name</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Change'>"
                output += "</form></body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                words=self.path.split('/')
                number=words[2]
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure to delete it?</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data'>"
                output += "<input type='submit' value='delete'>"
                output += "</form></body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                return


            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<br>"
                output += "<form method = 'POST' enctype='multipart/form-data'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

            if self.path.endswith("edit"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    number=self.path.split('/')[2]
                    updatedRestaurant = session.query(Restaurant).filter_by(id=number).one()
                    updatedRestaurant.name=messagecontent[0]
                    session.add(updatedRestaurant)
                    session.commit()

            if self.path.endswith("delete"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    number=self.path.split('/')[2]
                    updatedRestaurant = session.query(Restaurant).filter_by(id=number).one()
                    session.delete(updatedRestaurant)
                    session.commit()
                  

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()