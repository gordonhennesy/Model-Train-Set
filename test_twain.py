import sys, pygame
import math
from pygame.locals import *
grass = (0,255,127)
silver = (158, 176, 206) #(127,127,127)
brown = (151, 84, 20)
dark_brown= (118,55,19)
yellow = (255,255,0)
class Track(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
def next_segid(self, switches, prev_idx, forward, ):
   if self.forward == 1:
      forward = 'forward'
   else:
      forward='reverse'
   
   if self.segidx in switches.keys():
      state = switches[self.segidx][forward]['state']
      print(switches[self.segidx][forward][state])
      print('b4',self.segidx)
      if self.segidx == 853: self.forward = -1
      self.segidx = switches[self.segidx][forward][state]
      print('aft',self.segidx)
      #if self.segidx < 0: self.stop()
   else:
      self.segidx += self.forward
   #print(self.segidx)
   if self.segidx > len(self.segments)-1:
      ##self.stop() 
      segidx = 0
      #print("STOPPPPP")
   elif self.segidx < 0: self.segidx = len(self.segments) - 1
   #print(self.segidx)
class Car(pygame.sprite.Sprite):
    def __init__(self, image, length, segments, currentsegment=0, switches={}, forward = 1):
    #def __init__(self, image, segments, currentsegment=0, forward = 1):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.segments = segments
        self.forward = forward #means travelling "forward"; an arbitrary direction on the track
        self.facing = 1 # means oriented so the front of train image points toward "forward" on the track.
        self.forward = forward
        self.images = []
        self.directions = []
        self.points = []
        self.direction = 0
        self.segidx = currentsegment
        self.initImages()
        self.switches = switches
        self.length = length
        self.speed = 6
        self.status = 'running'
        self.queue = []
        seg = currentsegment - 1
        for i in range(length):
            self.queue.append(seg)
            seg -= 1
    def initImages(self):
        for i in range(0,circle_piece):
            img = rotateItAndScale(self.image, (360/circle_piece)*i + -self.forward * 90)
            self.images.append( img )
            self.directions.append( (360/circle_piece)*i)
        self.rect = img.get_rect()
    def setSegIdx(self, idx):
        self.segidx = idx
    def getSegIdx(self):
        return self.segidx
    def addImage(self, img, direction, point):
        self.directions.append(direction)
        self.images.append(img)
        self.points.append(point)
    def addToQueue(self, idx):
        self.queue.append(idx)
        self.queue = self.queue[1:]

    def toggle_facing(self):
        if self.facing == 1:
            self.facing = -1
        else: self.facing = 1
    def toggle_forward(self):
        if self.forward == 1:
            self.forward = -1
        else: self.forward = 1
    def update(self):
        if self.speed == 0:
            return
        elif self.status == 'slowing':
            self.speed -= 1
            if self.speed < 0: self.speed = 0
            
        current_segment = self.segments[self.segidx]    
        #current_point = current_segment[0]
        current_point = current_segment[1]
        
        # experiment
        #prev_pt_index = self.segidx - 15
        #if prev_pt_index < 0: prev_pt_index = prev_pt_index + len(self.segments) - 1
        #prev_point = self.segments[prev_pt_index][0]
        
        #how_many_backwards = 15
        #prev_pt_index = self.previous_segment(self.segidx, how_many_backwards, self.forward)
        #prev_point = self.segments[prev_pt_index][1]
        
        # Trying something
        #
        prev_point = current_segment[0]
        prev_seg_idx = self.queue[0]
        prev_point = self.segments[prev_seg_idx][0]
        
        #if self.forward < 0:
        if self.facing < 0:
            temp_point = prev_point
            prev_point = current_point
            current_point = temp_point
        
        #prev_point = current_segment[0]

        
        # to here
        self.segidx = self.next_segid(switches, self.segidx, self.forward)

        #print('prev index is',prev_seg_idx, self.segidx,self.queue)
        
        self.addToQueue(self.segidx) # this implements a circular queue
        
        self.orient(degreesToIndex(pointsToDirection(prev_point,current_point )))
        self.rect.center = math.floor(0.5 + (current_point[0]+prev_point[0]) / 2.0), math.floor(0.5 + (current_point[1]+prev_point[1]) / 2.0)
        self.image = self.images[self.direction]
    def next_segid(self, switches, prev_idx, forward):
      segidx = prev_idx = self.segidx
      if self.forward == 1:
         forward = 'forward'
      else:
         forward='reverse'
      
      if self.segidx in switches.keys():
         state = switches[self.segidx][forward]['state']
         #print(switches[prev_idx][forward][state])
         #print('b4',self.segidx)
         #if self.segidx == 853: self.forward = -1
         segidx = switches[prev_idx][forward][state]
         if self.segidx == 853: 
            #if self.facing == 1:
            #   self.facing = -1
            #else:
            #   self.facing = 1
            if self.forward == 1:
               self.forward = -1
            else:
               self.forward = 1
         #print('aft',self.segidx)
         #if self.segidx < 0: self.stop()
      else:
         segidx = self.segidx + self.forward
      #print(self.segidx)
      if self.segidx > len(self.segments)-1:
         ##self.stop() 
         segidx = 0
         #print("STOPPPPP")
      elif self.segidx < 0: segidx = len(self.segments) - 1
      return segidx

    def previous_segment(self, from_seg, how_many_backwards, direction):
        if how_many_backwards == 0:
            return from_seg
        seg = from_seg
        for i in range(how_many_backwards):
            #if direction == 1:
            #    dir = -1
            #else:
            #    dir = 1
            dir = direction
            seg = self.next_segid(self.switches, seg, dir)
        return seg
   
    def stop(self):
        self.speed = 0
    def slow(self):
        self.status = 'slowing'
    def move(self,dx,dy):
        self.rect.move_ip(dx,dy)
    def move_to(self, pt):
        self.rect.center = pt
    def orient(self, direction):
        self.direction = direction
    def orientFromSeg(self, seg):
        self.orient(degreesToIndex(nearestDegrees(pointsToDirection(seg[0],seg[1]))))
    def reverse(self):
        self.toggle_facing()
        if self.forward == 1:
            self.forward = -1
        else:
            self.forward = 1
def rotateItAndScale(source, angle):
    scale = 0.5
    source.set_colorkey()
    newsource = pygame.transform.rotozoom(source,0, scale)
    choprect = pygame.Rect(newsource.get_rect())
    dest = pygame.transform.rotozoom(source, angle, scale)
    choprect.center = dest.get_rect().center
    img = dest.subsurface(choprect)
    replaceColor(img, (0,0,0,255),(255,0,255,255))
    img.set_colorkey((255,0,255,255))
    img.get_rect().center = source.get_rect().center
    img.get_rect().center = source.get_rect().center
    
    return img
def rotateIt(source, angle):
    choprect = pygame.Rect(source.get_rect())
    dest = pygame.transform.rotate(source, angle)
    choprect.center = dest.get_rect().center
    return dest.subsurface(choprect)
def nearestDegrees(someAngle):
    'someAngle 0 -- 355, returns orientation (0 - 355) in 5 degree increments'    
    prevAngle = 0
    orientation = 0
    for i in range(1,circle_piece-1):
        if someAngle >= prevAngle and someAngle < ((360/circle_piece) * i):
            orientation = prevAngle
        prevAngle = (360/circle_piece) * i
    return orientation
def pointsToDirection(pt1, pt2):
    dx = pt2[0] - pt1[0]
    dy = pt1[1] - pt2[1]
    degrees = math.degrees(math.atan2(dy,dx))
    if degrees < 0: degrees = 360 + degrees

    return degrees
def degreesToIndex(deg):
    for i in range(0,  circle_piece):
        if (deg -  (360/circle_piece) * i) <= (360/circle_piece): return i
    return 0
#def loadAnImage(imagename, imgdir ="/Users/gordonh/workingcopy/pyproj/img/atsf/atsf/"):    
def loadAnImage(imagename, imgdir ="img/"):    
    ball = pygame.image.load(imgdir+imagename)
    ball_width,ball_height = ball.get_size()
    ball=pygame.transform.scale(ball, (int(math.floor(ball_width * 0.60)), int(math.floor(ball_height * 0.60))))
    #pygame.transform.scale(Surface, (width, height)
    ball_width,ball_height = ball.get_size()
    ball2 = pygame.Surface((ball_height , ball_height ))
    resize = 3.0
    #resize = 2.0
    ball2.blit(ball, (ball_height / 2.0 - (ball_width / 2.0), 0))
    return ball2

def replaceColor(img,color1, color2):
    x,y = img.get_rect().size
    for i in range(x):
        for j in range(y):
            if img.get_at((i,j)) == color1: img.set_at((i,j),color2)
def near(pt1, pt2):
    if math.sqrt((pt2[0] - pt1[0]) ** 2  + (pt2[0] - pt1[0]) ** 2)<1.0:
        return True
    return False

circle_piece = 72
segs = []
f = open('path_circle.txt','r')
#f = open('path_circle_test.txt','r')
#f = open('/Users/gordonh/path_circle2.txt','r')
lis = f.readlines()
f.close()
line_index = 1
#for li in lis[:720]:
for li in lis:
    s = li[:-1]
    x,y = s[1:-1].split(',')
    segs.append((x,y))
    #if line_index == 1374:
    #  print('seg idx',len(segs))
    line_index +=1
#print('finished', segs[0])
pointlist = []
for seg in segs:
    pointlist.append((int(seg[0]),int(seg[1])))
def distance(point,prevpoint):
   distx = point[0]-prevpoint[0]
   disty = point[1]-prevpoint[1]
   return math.sqrt(distx * distx + disty * disty)
#pygame.init()
segments = []
prevpoint = pointlist[len(pointlist)-1]
for point in pointlist:
   #print(distance(point,prevpoint))
   #if True: #distance(point,prevpoint) <= 5.0:
   if distance(point,prevpoint) <= 7.0:
      segments.append((prevpoint, point))
   prevpoint = point
#print('Segments: ',len(segments))
switches = {}
#switches[720]={'forward':{'0':0, '1': 400,'state':'0'},'reverse':{'0':0, '1': 400,'state':'1'}}
#switches[270]={'forward':{'0':275, '1': 1375,'state':'0'},'reverse':{'0':0, '1': 400,'state':'1'}}
#switches[len(segments)-1]={'forward':{'0':0,'1':0,'state':'0'}}
#switches[len(segments)-1]={'forward':{'0':-1,'1':-1,'state':'0'}}

# This is for path_circle_test.txt
#switches[270]={'forward':{'0':271, '1': 361,'state':'0'},'reverse':{'0':0, '1': 400,'state':'1'}}
#switches[358]={'forward':{'0':0,'1':0,'state':'0'}}

switches[270]={'forward':{'0':271, '1': 721,'state':'0'},'reverse':{'0':269, '1': 269,'state':'0'}}
switches[718]={'forward':{'0':0, '1': 0,'state':'0'},'reverse':{'0':717, '1': 717,'state':'0'}}

#switches[358]={'forward':{'0':0,'1':0,'state':'0'}}
switches[853]={'forward':{'0':628, '1':628,'state':'0'},'reverse':{'0':628, '1': 628,'state':'0'}}
switches[0]={'forward':{'0':1,'1':1,'state':'0'},'reverse':{'0':718, '1': 718,'state':'0'}}
#857
switch_numbers = []
switch_numbers.append(270)
switch_numbers.append(853)

#print(switches.keys())

#reverse_seqments = segments[:]
#reverse_seqments.reverse()

clock = pygame.time.Clock()
quit = 0
pygame.display.init()
size = width, height = pygame.display.list_modes()[0]
#size = width, height = 476, 335
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size) #.convert()
#screen.fill(black)
#pygame.display.flip()

traincars = pygame.sprite.RenderUpdates()
#if False:
if True:
   #traincars.add(Car(loadAnImage("atsff7aright_t.bmp"), reverse_seqments,55,forward=1))
   traincars.add(Car(loadAnImage("atsff7aright_t.bmp"), 13, segments, 255, switches, 1))
   #    def __init__(self, image, length, segments, currentsegment=0, switches, forward = 1):

   #traincars.add(Car(loadAnImage("atsff7aright_t.bmp"), segments,255))
   
   #traincars.add(Car(loadAnImage("atsf40sdbox-2_t.bmp"), segments,35))
   traincars.add(Car(loadAnImage("atsf40sdbox-2_t.bmp"), 10, segments,242, switches, 1))
   traincars.add(Car(loadAnImage("atsf40sdbox-2_t.bmp"), 10, segments,232))
   traincars.add(Car(loadAnImage("atsfbwcaboose_t.bmp"), 10, segments,222))
   
   #traincars.add(Car(loadAnImage("atsff7aright_t.bmp"), segments,forward=-1))
   #traincars.add(Car(loadAnImage("atsf40sdbox-2_t.bmp"), segments,16,forward=-1))
   #traincars.add(Car(loadAnImage("atsf40sdbox-2_t.bmp"), segments,35,forward=-1))
   #traincars.add(Car(loadAnImage("atsfbwcaboose_t.bmp"), segments,55,forward=-1))
speed = 6
viewpointx,viewpointy = 0,0
background = pygame.Surface(screen.get_size()) #.convert()
background.fill((0,255,127)) #black)
color = brown #(255,255,0)
closed = 0
width = 5
#rect = pygame.draw.lines(background, color, closed, pointlist, width) #: return Rect
def track_line(point1, point2):
   color = brown
   width = 20
   rect = pygame.draw.line(background, color, point1, point2, width)
   color = silver
   width = 13
   rect = pygame.draw.line(background, color, point1, point2, width)
   color = brown
   width = 9
   rect = pygame.draw.line(background, color, point1, point2, width)
#index_of_counting = 0
for seg in segments:
   track_line(seg[0],seg[1])
   #if index_of_counting == 10:
   #   continue
   #index_of_counting += 1
   #rect = pygame.draw.line(background, color, seg[0], seg[1], width) #: return Rect

#print(screen.get_size())
   
while 1:
   clock.tick(6 - speed)
   for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                sys.exit(0)
            elif event.key == pygame.locals.K_UP:
                speed += 1
                if speed > 6: speed = 6
            elif event.key == pygame.locals.K_DOWN:
                speed -= 1
                if speed < 0: speed = 0
            elif event.key == pygame.locals.K_LEFT:
                for sprite in traincars.sprites():
                    sprite.reverse()
            elif event.key == pygame.locals.K_1:
               switch_key = switch_numbers[0]
               if switches[switch_key]['forward']['state'] == '0': 
                  switches[switch_key]['forward']['state'] = '1' 
               else:
                  switches[switch_key]['forward']['state'] ='0'
            elif event.key == pygame.locals.K_2:
               switch_key = switch_numbers[1]
               #print(switch_key)
               if switches[switch_key]['forward']['state'] == '0': 
                  switches[switch_key]['forward']['state'] = '1' 
               else:
                  switches[switch_key]['forward']['state'] ='0'
            elif event.key == pygame.locals.K_3:
               switch_key = switch_numbers[2]
               if switches[switch_key]['forward']['state'] == '0': 
                  switches[switch_key]['forward']['state'] = '1' 
               else:
                  switches[switch_key]['forward']['state'] ='0'

   screen.blit(background,(0,0)) #viewpointx,viewpointy))

   color = 255, 0, 0
   for sw in switches.keys():
      if sw == 853:
          color= 0,255,0
      else:
          color = 255, 0, 0
      seg = segments[sw]
      rect = pygame.draw.line(screen, color, seg[0], seg[1], width)
      for i in range(10):
         if sw==853 and i > 2: color = 0,0,255
         state = switches[sw]['forward']['state']
         seg = segments[switches[sw]['forward'][state]+i]
         rect = pygame.draw.line(screen, color, seg[0], seg[1], width)


   traincars.update()

   traincars.draw(screen)
   pygame.display.flip()
