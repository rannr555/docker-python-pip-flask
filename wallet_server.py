from threading import Thread
import socket
from wallet import Wallet

wallet = Wallet() # the only global variable you should use

def message_handling(c):
    # helper function to allow for threading
    # reads and responds to requests
    try:
        while True:
            message = c.recv(1024).decode('utf-8')
            message = message.split()

            if(message[0] == 'GET'):
                resource = message[1]
                response = str(wallet.get(resource)) + '\n'
            elif(message[0] == 'MOD'):
                resource = message[1]
                delta = int(message[2])
                response = str(wallet.change(resource, delta)) + '\n'
            elif(message[0] == 'TRY'):
                resource = message[1]
                delta = int(message[2])
                response = str(wallet.try_change(resource, delta)) + '\n'
            elif(message[0] == 'TRAN'):
                delta = {}
                for i in range(1, len(message), 2):
                    delta[message[i]] = int(message[i+1])
                response = str(wallet.transaction(**delta)) + '\n'
            else:
                c.close()
                return

            c.sendall(response.encode('utf-8'))

    finally:
        c.close()

def create_wallet_server(local_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      

    try: 
        s.bind(('0.0.0.0', local_port))         
        
        s.listen(100)    

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        s.close()

if __name__ == '__main__':
    # parses command-line arguments, ensuring all implementations are invoked the same way
    import getopt
    import sys

    local_port = 34000
    optlist, args = getopt.getopt(sys.argv[1:], 'p:')
    for arg in optlist:
        if arg[0] == '-p': local_port = int(arg[1])
    print("Launching wallet server on :"+str(local_port))
    create_wallet_server(local_port)