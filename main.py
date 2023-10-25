from pynput import keyboard
from map import Map

import time
import os #для очистки экрана
from helicopter import Helicopter as Helico
from clouds import Clouds
import json
TICK_SLEEP=0.5
TREE_UPDATE=50
CLOUDS_UPDATE=50
FIRE_UPDATE=50

Map_w,Map_h=20,10
field=Map(Map_w,Map_h)
global helico
clouds= Clouds(Map_w,Map_h)
tick=1

helico=Helico(Map_w,Map_h)



MOVES={"w":(-1,0),"d":(0,1),"s":(1,0),"a":(0,-1)}
# f-сохранение, g-загрузкаwasdwsaadd
def process_key(key):
    global helico, tick,clouds,field
    c=key.char
  
    if c in MOVES.keys():
        dx,dy=MOVES[c][0],MOVES[c][1]
        helico.move(dx,dy)
    elif c=="f":
        with open('level.json', 'w') as lvl:
            json.dump(data,lvl)
            exit()
    elif c=="g":
        with open('level.json', 'r') as lvl:
            data=json.load(lvl)
            helico.import_data(data["helicopter"])
            tick=data["tick"] or 1
            field.import_data(data["field"])
            clouds.import_data(data["clouds"])

            
#...или неблокирующим способом:
listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()

#def process_key(key):
    #print(key)
    #if key.char=="a" or key.char=="A":
       # print("a")
    #listener=keyboard.Listener(
    #on_press=None,
    #on_release=process_key,)
    #listener.start()

while True:
    os.system("cls")
    
    
    
    helico.print_stats()
    
    field.print_map(helico,clouds)
 

    field.process_helicopter(helico,clouds)
    print(tick)
    tick+=1
    time.sleep(TICK_SLEEP)
    if tick%TREE_UPDATE==0:
        field.generate_tree()
    if tick%FIRE_UPDATE==0:
        field.update_fires(helico)
    if tick%CLOUDS_UPDATE==0:
        clouds.Update()
   