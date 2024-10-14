class progress:
 import os
 from colorama import Fore, Back, Style
 import time
 import asyncio
 def __init__(self):
   pass
 @staticmethod
 async def clear():
   self=progress()
   self.os.system('cls' if self.os.name == 'nt' else 'clear')
 @staticmethod
 def start():
  self=progress()
  self.asyncio.run(self.clear())
  print(f"{self.Fore.WHITE}({self.Fore.BLACK}❚❚❚❚❚❚❚❚❚❚{self.Fore.WHITE}) {self.Fore.BLACK}- {self.Fore.WHITE}0%")
 @staticmethod
 def setprecent(title: str, amo, oof):
  amount=int((amo/oof)*100)
  def prt(proggress, amo, oof):
    self=progress()
    self.asyncio.run(self.clear())
    print(f"{self.Fore.WHITE}{title}{self.Fore.WHITE}("+((f"{self.Fore.WHITE}❚"*int(proggress/10))+f"{self.Fore.BLACK}❚"*int(10-int(proggress/10)))+f"{self.Fore.WHITE}) {self.Fore.BLACK}- "+f"{self.Fore.WHITE}{proggress}%  {amo}/{oof}")
  prt(amount, amo, oof)
