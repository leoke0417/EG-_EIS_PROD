import socket 
import sys
from thread import *
# demo commit  #

class Automan_agent(object):
    """
    docstring for Automan_Client
    """
    def __init__(self):
        '''
        constructor
        '''
    
        pass
    def socket_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.bind((Host,Port))
        #sock.bind(('10.90.1.132', 54321))
        myip=([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
        sock.bind((myip, 10000))
        sock.listen(5)
        #print "Socket create succeed!!"
        print ("Server is Listening :ip %s port %s" % (myip,"10000"))
        while True:
            print "Waiting for new connection !!!"
            (csock, adr) = sock.accept()
            print "Client Info: ", csock, adr 
            #start_new_thread(automan.threadwork, (csock,))
            msg = csock.recv(1024)
            if not msg:
                pass
            else:
                print "Client send: " + msg    
                result = automan.call_function(msg)
                csock.sendall(result)
        sock.close()
                
    def threadwork(self, client):
        #Sending message to connected client
        #client.send("Welcome to the server.\n") 
        #infinite loop so that function do not terminate and thread do not end.
        msg = client.recv(1024)
        if not msg:
            pass
        else:
            print "Client send: " + msg    
            result = automan.call_function(msg)
            client.sendall(result)
            
        client.close()
    
    #add abby code
    def call_function(self, msg):        
        keys = msg
        items = keys.split(',')     # items[0]=.py file name, items[1]=.py class name, items[2]=.py function name
        parameter = str(','.join(items[3:]))
        exec('from automan.util.' + items[0] + ' import ' + items[1]) 
        ob = eval(items[1]+'()')
        defname = items[2] + '("' + parameter + '")'
        def_result = eval('ob.'+ defname)
        print "Return result : ",def_result
        return def_result


if __name__ == '__main__':

    automan = Automan_agent()
    automan.socket_server()