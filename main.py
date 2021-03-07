#import pdb
import math
#import mathutils
import random
import itertools
from collections import Counter
import bpy

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ArrayGen:
    def __init__(self):
        #bd - building
        block_size = Vector2(12, 12)
        bd_max_size = block_size
        bd_min_size = Vector2(10, 10)
        bd_size = Vector2(random.randint(bd_min_size.x, bd_max_size.x), random.randint(bd_min_size.y, bd_max_size.y))
        self.bd_map = [[0]*bd_size.x for _ in range(bd_size.y)]
        bd_format = random.choices(population=['B', 'U', 'O', 'L', 'H'], weights=[5, 3, 3, 1, 1])[0] #'B' stands for 'block', a square

        #hl - hollow
        hl_var = Vector2(30, 50)
        hl_proportion = random.randint(hl_var.x, hl_var.y)
        hl_size = Vector2(len(self.bd_map[0])/100*hl_proportion, len(self.bd_map)/100*hl_proportion)

        window_pct = 60

        #bd_format = 'O'
        for y in range(len(self.bd_map)):
            for x in range(len(self.bd_map[y])):
                if bd_format == 'B':
                    pass
                elif bd_format == 'U' and x > len(self.bd_map[y])/2-hl_size.x/2 and x < len(self.bd_map[y])/2+hl_size.x/2-1 and y > hl_size.y:
                    self.bd_map[y][x] = 1
                elif bd_format == 'O' and x > len(self.bd_map[y])/2-hl_size.x/2 and x < len(self.bd_map[y])/2+hl_size.x/2-1 and y > len(self.bd_map)/2-hl_size.y/2-1 and y < len(self.bd_map)/2+hl_size.y/2:
                    self.bd_map[y][x] = 1
                elif bd_format == 'L' and x > len(self.bd_map[y])/2+hl_size.x/2-2 and y > len(self.bd_map)/2+hl_size.y/2-2:
                    self.bd_map[y][x] = 1
                elif bd_format == 'H' and x > len(self.bd_map[y])/2-hl_size.x/2 and x < len(self.bd_map[y])/2+hl_size.x/2-1 and (y < len(self.bd_map)/2-hl_size.y/2 or y > len(self.bd_map)/2+hl_size.y/2-1):
                    self.bd_map[y][x] = 1

        for y in range(len(self.bd_map)):
            for x in range(len(self.bd_map[y])):
                if self.bd_map[y][x] == 0 and (y == 0 or x == 0 or y == len(self.bd_map)-1 or x == len(self.bd_map[0])-1):
                    self.bd_map[y][x] = 2
                elif self.bd_map[y][x] == 0 and (self.bd_map[y-1][x] == 1 or self.bd_map[y+1][x] == 1 or self.bd_map[y][x-1] == 1 or self.bd_map[y][x+1] == 1):
                    self.bd_map[y][x] = 2
            
        window_count = 0
        wall_count = 0
        wall_tiles = []

        #Listar os tiles que contêm paredes e contabilizar
        for k, v in enumerate(list(itertools.chain.from_iterable(self.bd_map))):
            if v == 2:
                wall_tiles.append(divmod(k, len(self.bd_map[0])))
                wall_count += 1

        while window_count/(window_count+wall_count)*100 < window_pct:
            n = random.randint(0, len(wall_tiles)-1)
            y = wall_tiles[n][0]
            x = wall_tiles[n][1]
            mirror = Vector2(int((bd_size.x-1)/2-(x-(bd_size.x-1)/2)), int((bd_size.y-1)/2-(y-(bd_size.y-1)/2)))
            new_windows = [[y, x], [mirror.y, x], [y, mirror.x], [mirror.y, mirror.x]]
            for n in new_windows:
                if self.bd_map[n[0]][n[1]] == 2:
                    self.bd_map[n[0]][n[1]] = 3
            
            window_count = Counter(i for i in list(itertools.chain.from_iterable(self.bd_map)))[3]
            wall_count = Counter(i for i in list(itertools.chain.from_iterable(self.bd_map)))[2]
            
        '''print('Tamanho:', bd_size.x, bd_size.y, 'Format:', bd_format)
        for m in self.bd_map:
            print(m)
        '''
    def getArray(self):
        return self.bd_map

class Building:
    def addObj(self, type, posX, posY, posZ, rotZ):
        obj = bpy.data.objects.new("temp", bpy.data.objects[type].data)
        obj.location = (posX, posY, posZ)
        obj.rotation_euler = (0, 0, math.radians(rotZ))
        bpy.context.collection.objects.link(obj)
        
    def __init__(self, bd_map):
        window = 'Window ' + str(random.randint(1, 4))
        if (random.randint(0, 2) == 0): #sortear de 0 a 2; se for 0...
            window_sec = 'Window ' + str(random.randint(1, 4)) #sortear uma nova window pro floor térreo
        else: #se não...
            window_sec = window #usar a mesma window
        door = 'Door ' + str(random.randint(1, 4)) #escolher modelo de door
        floors = random.choices(population=[2, 3, 4], weights=[1, 3, 4])[0] #número de floors
        material = 'Wall ' + str(random.randint(1, 10)) #material do prédio
        if (random.randint(0, 2) == 0): #sortear de 0 a 2; se for 0...
            material_sec = 'Wall Térreo ' + str(random.randint(1, 3)) #sortear um novo material pro floor térreo
        else: #se não...
            material_sec = material #usar o mesmo material
        objs = ['Nada', 'Caixa dagua', 'Chamine 1', 'Chamine 2', 'Exaustor', 'Saida', 'Planta']
        roof_objs = random.choices(population=objs, weights=[1, 3, 1, 1, 1, 1, 1], k=2)
        while (roof_objs[0] == roof_objs[1]): #se forem iguais, ficar gerando um novo pra substituir o último
            roof_objs[1] = random.choices(population=objs, weights=[1, 3, 1, 1, 1, 1, 1])[0]
        stairs = 'Stairs ' + str(random.randint(0, 3)) #escolher modelo de escada
        toldo = 'Toldo ' + str(random.randint(0, 3)) #escolher modelo de toldo

        #correções pra testes-----------
        window = 'Janela'
        wall = 'Parede'
        #-------------------------------
        
        if len(bpy.context.selected_objects) != 0:
            bpy.ops.object.select_all(action='DESELECT')
        
        f = 2.5 #floor size
        for z in range(0, floors):
            for y in range(0, len(bd_map)):
                for x in range(0, len(bd_map[y])):
                    if x == len(bd_map[y])-1 or bd_map[y][x+1] == 1:
                        r = 90
                        if bd_map[y][x] == 3:
                            self.addObj(window, x, -y, z*f, r)
                        elif bd_map[y][x] == 2:
                            self.addObj(wall, x, -y, z*f, r)
                        #print("adicionar janela virada pra direita")
                    if x == 0 or bd_map[y][x-1] == 1:
                        r = 270
                        if bd_map[y][x] == 3:
                            self.addObj(window, x, -y, z*f, r)
                        elif bd_map[y][x] == 2:
                            self.addObj(wall, x, -y, z*f, r)
                        #print("adicionar janela pra esquerda")
                    if y == 0 or bd_map[y-1][x] == 1:
                        r = 180
                        if bd_map[y][x] == 3:
                            self.addObj(window, x, -y, z*f, r)
                        elif bd_map[y][x] == 2:
                            self.addObj(wall, x, -y, z*f, r)
                        #print("adicionar janela pra cima")
                    if y == len(bd_map)-1 or bd_map[y+1][x] == 1:
                        r = 0
                        if bd_map[y][x] == 3:
                            self.addObj(window, x, -y, z*f, r)
                        elif bd_map[y][x] == 2:
                            self.addObj(wall, x, -y, z*f, r)
                        #print("adicionar janela pra baixo")
                        


b = Building(ArrayGen().getArray())
