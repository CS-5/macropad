
from pad import Pad
from host_comm import Comm

pad = Pad()
comm = Comm()

while True:
  for event in pad.event_stream():
      print(event)

  for data in comm.read_stream():
      print(data)