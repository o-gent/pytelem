from datalink import Datalink
import time

link = Datalink('client')

while True:
    link.put(2,[0,0,0])
    link.refresh_client()
    print(link.get(1))