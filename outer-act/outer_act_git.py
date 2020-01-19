#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TODO: 
# OK do it fullscreen with bigger images
# replicate behavior from scratch script: 
#   OK score, 
#   OK  min time to present, 
#   OK  and reset after no motion detected for x amount of time.
# OK animations x 2. 2nd happens when score > 3
# OK animations with ImageGrid, see performance.
# OK sound
#
# 
##

import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font
from pyglet.window import key 
import time

debug = False

if debug:
    from vision_mock import Vision
else:
    from vision import Vision


###############################################################################
class Projection(window.Window):
    
    def __init__(self, *args, **kwargs):

        #Let all of the arguments pass through
        self.win = window.Window.__init__(self, *args, **kwargs)
        
        clock.schedule_interval(self.update, 1.0/30) # update at FPS of Hz

        
        # load object animations to be drawn
        self.drawableObjects = []
        self.createDrawableObjects (image_frames= ('official/d_1.1_a_01.png', 'official/d_1.1_a_02.png',
                                                   'official/d_1.1_a_03.png', 'official/d_1.1_a_04.png',
                                                   'official/d_1.1_a_05.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png',
                                                   'official/d_1.1_b_02.png', 'official/d_1.1_b_01.png'))
        self.createDrawableObjects (image_frames= ('official/d_1.2_a_01.png', 'official/d_1.2_a_02.png',
                                                   'official/d_1.2_a_03.png', 'official/d_1.2_a_04.png',
                                                   'official/d_1.2_b_01.png', 'official/d_1.2_b_02.png',
                                                   'official/d_1.2_b_03.png', 'official/d_1.2_b_04.png'))

        self.idraw = 0
        
        # instantiating a Vision  object
        self.vision = Vision()

        # loading sounds        
        self.track =  pyglet.media.load('whatsupbro.wav', streaming=False)

        #
        self.drawing = False
        self.prev_drawing = False
        self.timelastdraw = 0
        self.maxlag = 30 # seconds
        
        self.anim_length = 1*11  # in seconds
        
        self.motionstart = None
        self.score = 0
        
    def createDrawableObjects(self, image_frames):


        # Create the list of pyglet images
        images = map(lambda img: pyglet.image.load(img), image_frames)
        
        # Each of the image frames will be displayed for 0.33 seconds
        animation = pyglet.image.Animation.from_image_sequence(images, 0.33, loop = True)
        
        # Create a sprite instance.
        self.animSprite = pyglet.sprite.Sprite(animation)

        # Add these sprites to the list of drawables
        self.drawableObjects.append(self.animSprite)
        
    
    def update(self, dt):

        # ask to vision object to update itself
        self.vision.update()
        
        if self.vision.motion:
            self.motionstart = time.time()
        
        currtime = time.time()
        
        if self.motionstart is not None:
            if currtime  < (self.motionstart + self.anim_length):
                self.drawing = True
            else:
                self.drawing = False

    def update_score(self):
        # update on score behavior
        if self.score < 3:
            self.idraw = 0
            
        elif self.score == 3:
            self.idraw = 1
            
        elif self.score > 3:
            # reset
            self.idraw = 0
            self.score = 0
        
        # if so much time have pass, returns score to zero
        if time.time() > (self.timelastdraw + self.maxlag):
                self.score = 0
                self.idraw = 0
                
        # creates label to show current score
        self.create_label()
        
        
        
    def create_label(self):
        
        self.label = pyglet.text.Label('Score: %d' % self.score,
              font_name='Times New Roman',
              font_size=36,
              x=100, y=100,
              anchor_x='center', anchor_y='center')

        
                    
    def on_draw(self):
        
        self.update_score()
        
        self.clear() # clearing buffer
        #clock.tick() # ticking the clock
            
        if self.drawing:
            
            # draw sprite
            self.drawableObjects[self.idraw].draw()
            
            # 
            self.label.draw()
            
            # if this is the first draw, so previouly it was false
            if not self.prev_drawing:
                self.track.play()
                self.score += 1
            
            # end of if drawing, saves state
            self.prev_drawing = True
            self.timelastdraw = time.time()
            
        else:
            self.prev_drawing = False
            
        # flipping
        self.flip()
    
    
    ## Event handlers
    def on_key_press(self, symbol, modifiers):
        
        if symbol == key.ESCAPE:
            self.dispatch_event('on_close')  
            
        if symbol == key.M:
            self.vision.motion=True
        if symbol == key.N:
            self.vision.motion=False
            


        
###################################################################
  
if __name__ == "__main__":
    #win = Projection(caption="Outer act", width=800, height = 600)
    win = Projection(caption="Outer act", fullscreen = True)

    pyglet.app.run()


