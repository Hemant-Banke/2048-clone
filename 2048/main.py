
import pygame, sys, os, math, random
from pygame.locals import *

from colors import *
from definitions import *

import tile


pygame.init()


class Game(object):

    def __init__( self ):
    
        #dictionary to store all tile objects
        #key : (x,y) position
        #value : tile object at (x,y)
        #the tiles in animation space( tiles that should be deleted once they complete animating ) have key (x,y,z)
        self.tile_ins = {}
        
        self.is_valid_move = False


    def initialize( self ):
        """sets all positions in tile_ins to None
        """
        for x in range(0, TILE_ORDER):
            for y in range(0, -TILE_ORDER, -1):
                self.tile_ins[(x,y)] = None

        self.spawn()
        self.spawn()
           

    def draw_bg_tiles( self, SURF):
        """draws background tiles on SURF
        """
        for x in range(0, TILE_ORDER):
            for y in range(0, -TILE_ORDER, -1):
                pos = get_pos( (x,y) )
                rounded_rect( SURF, EMPTY_BOX, ( pos[0], pos[1], TILE_SIZE, TILE_SIZE ), TILE_RADIUS )

    
    def draw( self, SURF) :
        """draws main game on SURF
        """
        SURF.fill( BGCOLOR )
        self.draw_bg_tiles( SURF )
        tile.tile_draw( SURF, self.tile_ins )


    def anim_handler( self ):
        """calls animation handler for all tiles
        """
        tile.tile_anim( game.tile_ins )


    def spawn( self ):
        """spawns a tile at random position in grid
            probability of 2 : 3/4
            probability of 4 : 1/4
        """
        pos = ()
        degree = 1 if ( round(random.random(), 2) <= 0.75) else 2

        #find empty position
        while (True) :
            pos = ( random.randint( 0, TILE_ORDER-1 ), random.randint( 1-TILE_ORDER, 0 ) )
            if not is_tile( pos, self.tile_ins):
                break

        self.tile_ins[pos] = tile.tile( pos, degree )
        

    def move( self, new_pos, curr_pos):
        """moves tile at curr_pos to new_pos
        """
        self.tile_ins[new_pos] = self.tile_ins[curr_pos]
        self.tile_ins[new_pos].set_grid( new_pos )
        del self.tile_ins[curr_pos]
        self.tile_ins[curr_pos] = None

        self.is_valid_move = True


    def merge( self, first_pos, sec_pos):
        """merges tile at sec_pos with tile at first_pos
        """
        degree = self.tile_ins[first_pos].degree

        #tile at sec_pos goes to animation space and will be deleted after it stops animating
        anim_1_pos = list(first_pos)
        anim_1_pos.append(1)
        anim_1_pos = tuple(anim_1_pos)
        
        self.tile_ins[anim_1_pos] = self.tile_ins[sec_pos]
        self.tile_ins[anim_1_pos].set_grid( first_pos )
        
        del self.tile_ins[sec_pos]
        self.tile_ins[sec_pos] = None
        
        del self.tile_ins[first_pos]
        self.tile_ins[first_pos] = tile.tile( first_pos, degree+1)

        self.is_valid_move = True
        

    def is_game_over( self ):
        """returns True if game over
        """
        return is_filled(self.tile_ins) and not find_pairs(self.tile_ins)


    def debug_anim_space( self ):
        print "..."
        for key in self.tile_ins.keys():
            if len(key) == 3:
                print key
        print "..."
    

    def event_handler( self, event ):
        """handles movement of tiles
        """
        #self.debug_anim_space()
        
        #check for game over
        if self.is_game_over():
            print "Game Over!"
            return
        
        #delete all tiles in animation space
        if not tile.tile.is_anim:
            for pos in self.tile_ins.keys():
                if len(pos) == 3:
                    del self.tile_ins[pos]

        #Move only if animation is done
        if event.type == KEYDOWN and not tile.tile.is_anim:
            #UP
            if event.key == K_UP :
                move_up( self )

            #DOWN
            elif event.key == K_DOWN :
                move_down( self )

            #LEFT
            elif event.key == K_LEFT :
                move_left( self )

            #RIGHT
            elif event.key == K_RIGHT :
                move_right( self )

        #spawn a new tile if it is valid move
        if self.is_valid_move:
            self.spawn()
            self.is_valid_move = False
                        

##Restart text
fontObj = pygame.font.Font ( tile.tile.text_font , 19 )
textSurfObj_R = fontObj.render ( "Restart" , True, TEXT_DARK )
textRectObj_R = textSurfObj_R.get_rect()
textRectObj_R.topright = ( WIN_SIZE + TILE_PADDING, TILE_PADDING)

##2048 text
fontObj = pygame.font.Font ( tile.tile.text_font , HEADER_S - 4*TILE_PADDING )
textSurfObj = fontObj.render ( "2048" , True, TEXT_DARK )
textRectObj = textSurfObj.get_rect()
textRectObj.topleft = ( TILE_PADDING, TILE_PADDING)

def draw_header( SURF):
    SURF.fill( BGCOLOR0 )
    
    #writing 2048
    SURF.blit( textSurfObj , textRectObj )

    #writing Restart
    SURF.blit( textSurfObj_R , textRectObj_R )

    #pygame.draw.rect(SURF, BLACK, textRectObj_R, 2)
    #pygame.draw.rect(SURF, BLACK, textRectObj, 2)


##
SURF_2048 = pygame.Surface(( WIN_SIZE, WIN_SIZE))

SURF = pygame.display.set_mode( ( WIN_SIZE + 2*TILE_PADDING, WIN_SIZE + HEADER_S + TILE_PADDING) )
pygame.display.set_caption("2048")
pygame.display.set_icon( pygame.image.load( "2048_icon.png" ))

clock = pygame.time.Clock()

#Start Game
game = Game()
game.initialize()

while True:
    for event in pygame.event.get():
        if (event.type == QUIT ):
            pygame.quit()
            sys.exit()

        #restart if clicked on restart
        if event.type == MOUSEBUTTONDOWN and textRectObj_R.collidepoint(pygame.mouse.get_pos()):
            #initialize game again
            game.initialize()      

        #call event handler
        game.event_handler( event )

    #call animation handler
    game.anim_handler()

    #draw the game
    game.draw( SURF_2048 )
    
    draw_header( SURF)
    SURF.blit( SURF_2048, ( TILE_PADDING, HEADER_S) )
        
    pygame.display.update()
    clock.tick(60)
