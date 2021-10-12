from mario import Block


Mapset = [ 
    
Block(15,5,1),
Block(16,5,1),
Block(17,5,1),
Block(15,6,1),
Block(16,6,1),
Block(17,6,1),
Block(15,7,0),
Block(16,7,0),
Block(17,7,0),
Block(10, 8, 2),
Block(7, 6, 2),
Block(12, 10, 2),
Block(13,10, 3)
]

for i in range(0, 100 + 1): # 맵 기본적인 타일
    Mapset.append(Block(i,4,0))
    Mapset.append(Block(i,3,1))
    Mapset.append(Block(i,2,1))
    Mapset.append(Block(i,1,1))

