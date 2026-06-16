import socket
import sys
from automan.util.tool import Tool
class Automan_server(object):

    '''
    classdocs
    '''
    def __init__(self):
       '''
       Constructor
       '''
    def result_get(self,value_dict):
        try:
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failes to create socket'
            sys.exit()
        print 'Socket Created'

        local_dict=dict(value_dict)
        host=(local_dict["ip"])
        port=int(local_dict["port"])

        # Connect the socket to the port where the server is listening
        server_address = (host, port)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        try:   
            # Send data
            action=(local_dict["action"])
            print >>sys.stderr, 'sending action "%s" to server' % action
            sock.sendall(action)

            # Look for the response
            amount_received = 0
            amount_expected = len(action)
            
            while amount_received < amount_expected:
                data = sock.recv(1024)
                amount_received += len(data)
                print >>sys.stderr, 'received from server "%s"' % data
                return data

        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()


    def result_verify(self,verity_info):
        print verity_info
        Tool().dir_verify(verity_info)


