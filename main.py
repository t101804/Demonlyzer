import argparse,os , requests, json
from threading import *
from threading import Thread
from queue import Queue

def print_warning(msg):
    print(f"\033[93m[!] {msg} \033[0m\U000026A0")

def print_success(msg):
    print(f"\033[92m[+] {msg} \033[0m\U00002705")

def print_failure(msg):
    print(f"\033[91m[-] {msg} \033[0m\U0000274C")
    open(f"failure_log.txt", "a" ).write( msg + "\n" )

# Always Put Credits to @CallMeRep :) i happy if i inspired you or if you want copy paste my system 
# always dont forget to put credits

class Worker(Thread):
  def __init__(self, tasks):
      Thread.__init__(self)
      self.tasks = tasks
      self.daemon = True
      self.start()

  def run(self):
      while True:
          func, args, kargs = self.tasks.get()
          try: func(*args, **kargs)
          except Exception as e: print(e)
          self.tasks.task_done()

class ThreadPool:
  def __init__(self, num_threads):
      self.tasks = Queue(num_threads)
      for _ in range(num_threads): Worker(self.tasks)

  def add_task(self, func, *args, **kargs):
      self.tasks.put((func, args, kargs))

  def wait_completion(self):
      self.tasks.join()

class Main():
    def __init__(self):
        self.args = True

    @classmethod
    def Args(cls):
        Banner = r"""
              Demonlyzer | V1.2 | Analyzer Site
                            ,-.                               
       ___,---.__          /'|`\          __,---,___          
    ,-'    \`    `-.____,-'  |  `-.____,-'    //    `-.       
  ,'        |           ~'\     /`~           |        `.      
 /      ___//              `. ,'          ,  , \___      \    
|    ,-'   `-.__   _         |        ,    __,-'   `-.    |    
|   /          /\_  `   .    |    ,      _/\          \   |   
\  |           \ \`-.___ \   |   / ___,-'/ /           |  /  
 \  \           | `._   `\\  |  //'   _,' |           /  /      
  `-.\         /'  _ `---'' , . ``---' _  `\         /,-'     
     ``       /     \    ,='/ \`=.    /     \       ''          
             |__   /|\_,--.,-.--,--._/|\   __|                  
             /  `./  \\`\ |  |  | /,//' \,'  \                  
            /   /     ||--+--|--+-/-|     \   \                 
           |   |     /'\_\_\ | /_/_/`\     |   |                
            \   \__, \_     `~'     _/ .__/   /            
             `-._,-'   `-._______,-'   `-._,-/ 

"""
        cls.Runner(Banner)
        parser = argparse.ArgumentParser()
        parser.add_argument('--site', type=str, help='single web that want to scan')
        parser.add_argument('--lists', type=str, help='input file')
        parser.add_argument('--thread', type=int, default=10, help='number of threads')
        parser.add_argument('--techsave', type=str, help='technology to save e.g ( wordpress,laravel,joomla or just 1 techs like java ) )')
        args = parser.parse_args()
        if args.lists:
            Scrapper(None, args.lists, args.thread, args.techsave).executor()
        elif args.site: 
            Scrapper(args.site, None, None, None).executor()
        else:
            Options = """
\033[1;30mHey this script was a argument script but you run it by directly so i will give you a options 
but you still can use the arguments , need help ? run script.py --help

\033[1;37mDemonlyzer Options:
\033[1;31m1. Mass Scan ( Multiple Scan by a lists of web in files )
2. Single Scan ( Single Scan by a Single web )
3. Exit
            """ 
            print(Options)
            choice = input("Choose an option: ")
            if "1" in choice:
                lists = input("Enter a list filename (e.g : weblists.txt): ")
                threading = input("Enter a thread (default : 10): ")
                special = input("Enter technology to save (leave blank to save all techs): ")
                Scrapper(None, lists, threading, special).executor()
            elif "2" in choice:
                site = input("Enter web to scan ( e.g : https://google.com ) : ")
                Scrapper(site, None, None, None).executor()
            else: 
                exit("Thanks for using my tools. Please visit http://app.repcyber.com or join https://t.me//RepProject")

    @classmethod
    def Runner(cls, text):
        colors = ['\033[1;31m', '\033[1;37m', '\033[1;30m']
        lines = text.splitlines()
        for line in lines:
            color = colors[lines.index(line) % len(colors)]
            print(color + line.rstrip() + '\033[0m')



class Scrapper():
    def __init__(self , site ,lists , thread, special):
        self.multiScan = False
        self.site = site
        self.lists = lists
        self.thread = thread
        self.speciality = special

    def ReadLists(self):
        Pool = ThreadPool(int(self.thread))
        sites = open(self.lists, encoding="utf8" ).read().splitlines()
        for site in sites:
            Pool.add_task(self.Scrapper, site)
        Pool.wait_completion()

    def Scrapper(self, site):
        if not site.startswith('http'): site = "http://" + site
        Data = {"web": site}
        PostData = requests.post("https://app.repcyber.com/api/checktech", data= Data)
        if "Error Getting in API" in PostData.text:
            print_warning(f"Something error when scanning this sites {site} ")
        else:
            try :
                JsonData = json.loads(PostData.text)
                print_success(f"Success Analyse {site} Remaining Quota {JsonData['Quota']}")
                if JsonData['Technology'] != None:
                    for detect in JsonData['Technology']:
                        if self.speciality is not None:
                            if "," in self.speciality:
                                for tech in self.speciality.split(","):
                                    if tech.strip().lower() in detect.lower().strip():
                                        open(f"results/{tech.strip()}.txt", "a").write(site + "\n")
                            else:
                                if self.speciality.lower() in detect.lower().strip():
                                    open(f"results/{self.speciality}.txt", "a").write(site + "\n")
                        else:
                            open(f"results/{detect}.txt", "a").write(site + "\n")
                else:
                    print_warning(f"Not using any technology {site}")


            except Exception as e : print_failure(f"something is error in this response {PostData.text} and giving this error : {e}")

    def executor(self):
        if self.lists is None:
            self.Scrapper(self.site)
        else:
            self.ReadLists()

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    if not os.path.exists('results'): os.mkdir('results')
    Main.Args()