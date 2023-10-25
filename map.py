from utils import randbool
from utils import randcell
from utils import randcell2
#1- дерево
# 2-река
# 🚁🟩🌲🌊🚑🛒🟥🚰💛
#3-🚑
#4-🛒
#5-🔥
CELL_TYPES='🟩🌲🌊🚑🛒🔥'
TREE_BONUS=100
UPGRADE_COST=5000
LIFE_COST=10000

class Map:
    def __init__(self, w, h):
        self.w=w
        self.h=h
        self.cells=[[0 for i in range(w)] for j in range(h)]
        self.generate_river(10)
        self.generate_forest(10,50)
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.add_fire()
        self.generate_upgrade_shop()
        self.generate_hospital()
    def generate_river(self,l):
        rc=randcell(self.w,self.h)
        rx,ry=rc[0],rc[1]
       # print(rx,ry)
       # if (self.chek_bounds(rx,ry)):
        self.cells[rx][ry]=2
        while l>0:
            rc2=randcell2(rx,ry,self.w,self.h)
            rx2,ry2=rc2[0],rc2[1]
            if (self.chek_bounds(rx2,ry2)):
                self.cells[rx2][ry2]=2
                rx,ry=rx2,ry2
                l-=1
    def chek_bounds(self,x,y):
        if (x<0 or y<0 or x>=self.h or y>=self.w):
            return False
        return True
    def import_data(self,data):
        self.cels=data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]
    def print_map(self,helico,clouds):
        #print("🟥 "*(self.w+2),end="")
       # print()
       
        #for row in self.cells:
         #   print("🟥",end="")
          #  for cell in row:
           #    if cell>=0 and cell<len(CELL_TYPES):
            #        if cell>0:
             #        print(CELL_TYPES[cell]+' ',end="")
                     
               #     else:
                #     print(CELL_TYPES[cell],end="")
            #print("🟥",end="")
                
            #print()
        #print("🟥 "*(self.w+2),end="")
        
        aa=[]
        i=0
        zz=""
        zz=("🟥"*(self.w+2)+" ")
        
        aa.append(zz)
        
        zz=""
              
       
        for ri in range(self.h):
            
            zz+="🟥"
            for ci in range(self.w):
               cell=self.cells[ri][ci]
               if (clouds.cells[ri][ci]==1):
                  zz+="☁️ "
               elif (clouds.cells[ri][ci]==2):
                   zz+="⚡"
               elif helico.x==ri and helico.y==ci:
                   zz+="🚁"
               elif cell>=0 and cell<len(CELL_TYPES):
                   
                    zz+=(CELL_TYPES[cell])
            zz+="🟥"
                
            aa.append(zz)
           
            zz=""
        zz=("🟥"*(self.w+2))
        aa.append(zz)
        zz=""
        
        for i in (aa) :
         
            if i!=aa[-1] :
              print(i)
            else:
             #   print(i,"\r")

                print(i)
        
        aa=[]

   
    def generate_forest(self,r,mxr):
        for ri  in range(self.h):
           for si  in range(self.w):  
                if randbool(r,mxr):
             
                 self.cells[ri][si]=1
    def generate_tree(self):
        
        c=randcell(self.w,self.h)
        cx,cy=c[0] ,c[1]     
        if self.chek_bounds(cx,cy) and self.cells[cx][cy]==0:
            self.cells[cx][cy]=1

    def export_data(self):
       return{"cells":self.cells}
      
    def new_method(self):
        return CELL_TYPES
    
    def generate_upgrade_shop(self):
        c=randcell(self.w,self.h)
        cx,cy=c[0] ,c[1] 
        self.cells[cx][cy]=4
    def generate_hospital(self):
        c=randcell(self.w,self.h)
        cx,cy=c[0] ,c[1] 
        if self.cells[cx][cy]!=4:
            self.cells[cx][cy]=3
        else: 
            self.generate_hospital()
    def add_fire(self):
        c=randcell(self.w,self.h)
        cx,cy=c[0] ,c[1]  
        if self.cells[cx][cy]==1:
            self.cells[cx][cy]=5
           


    def update_fires(self,helico):
        for ri in range(self.h):
             for ci in range(self.w):
                cell=self.cells[ri][ci]
                if cell==5:
                    self.cells[ri][ci]=0
                    helico.score-=10 
        for i in range(5):
            self.add_fire()
           
    def process_helicopter(self,helico,clouds):
        c=self.cells[helico.x][helico.y]
        d=clouds.cells[helico.x][helico.y]
        if (c==2):
            helico.tank=helico.mxtank
        if c==5 and helico.tank>0:
            helico.score+=TREE_BONUS
            helico.tank-=1
            self.cells[helico.x][helico.y]=1
        
        if c==4 and helico.score>=UPGRADE_COST:
            helico.mxtank+=1
            helico.score-=UPGRADE_COST
        
        if c==3 and helico.score>=LIFE_COST:
            helico.mxlives+=10
            helico.score-=LIFE_COST
        if d==2:
            helico.lives-=1
        if helico.lives<1:
                helico.game_over()
      

