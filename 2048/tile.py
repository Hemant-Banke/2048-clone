"""Contains tile class """


import pygame, sys, os, math
from pygame.locals import *

from colors import *
from definitions import *

class tile( object) :

    #animation time factor
    ANIM_MUL = 30

    #checks if any tile is animating currently
    is_anim = False

    assert os.path.isfile ( 'fonts/ClearSans-Bold.ttf') , 'tile : ClearSans-Bold font does not exist'
    text_font = 'fonts/ClearSans-Bold.ttf'
    
    def __init__( self, grid_pos , degree ):
        """grid_pos : position of the tile in grid ( x, y) where x and y are integers, y is -ve
            degree   : power of two which tile represents
        """
        self.grid_pos = list(grid_pos)
        self.degree = degree

        #new grid pos during animation
        self.new_grid_pos = list(grid_pos)

        #set color for tile
        self.color = get_color( D1_COLOR, D7_COLOR, self.degree )
        
        #determine top-left position of tile on screen
        #x_scr = (x+1)*padding + x*size
        self.pos = get_pos( grid_pos )

        #defining font object
        self.fontObj = pygame.font.Font ( tile.text_font , TILE_SIZE - 4*TILE_PADDING )


    def set_grid( self, new_grid_pos ):
        """Moves the tile to new position in grid
        """
        if new_grid_pos != self.grid_pos :
            self.new_grid_pos = new_grid_pos
        
        #determine top-left position of tile on screen
        #x_scr = (x+1)*padding + x*size
        #self.pos = [ TILE_PADDING * (grid_pos[0] + 1) + TILE_SIZE*grid_pos[0],
        #                TILE_PADDING * ( abs(grid_pos[1]) + 1) + TILE_SIZE * abs(grid_pos[1])  ]

    def anim_handler( self):
        """Handles all animations of tiles
            Is called every frame
        """
        if self.new_grid_pos != self.grid_pos :
            self.move_anim()
        

    def move_anim ( self):
        """determines position of tile during animation
        """
        tile.is_anim = True
        
        final_pos = get_pos( self.new_grid_pos)
        
        #to move in y
        if self.grid_pos[0] == self.new_grid_pos[0] :
            
            if self.pos[1] in range( final_pos[1] - tile.ANIM_MUL , final_pos[1] + tile.ANIM_MUL + 1) :
                self.pos = final_pos
                self.grid_pos = self.new_grid_pos
                tile.is_anim = False
            else:
                #moving tile in correct direction
                self.pos[1] += tile.ANIM_MUL * int((self.grid_pos[1] - self.new_grid_pos[1]) / abs(self.grid_pos[1] - self.new_grid_pos[1]))

        #to move in x
        if self.grid_pos[1] == self.new_grid_pos[1] :
            
            if self.pos[0] in range( final_pos[0] - tile.ANIM_MUL , final_pos[0] + tile.ANIM_MUL + 1) :
                self.pos = final_pos
                self.grid_pos = self.new_grid_pos
                tile.is_anim = False
            else:
                #moving tile in correct direction
                self.pos[0] += tile.ANIM_MUL * int((self.new_grid_pos[0] - self.grid_pos[0]) / abs(self.new_grid_pos[0] - self.grid_pos[0]))
            
        

    def draw( self, SURF ):
        """draws tile on screen
        """
        #draws rounded tile
        rect = pygame.Rect( self.pos[0], self.pos[1], TILE_SIZE, TILE_SIZE )
        rounded_rect( SURF, self.color, rect, TILE_RADIUS )

        #writing the number
        textSurfObj = self.fontObj.render ( str( 2**self.degree ) , True, TEXT_DARK )
        textRectObj = textSurfObj.get_rect()
        textRectObj.center = rect.center
        SURF.blit( textSurfObj , textRectObj )


            
def tile_draw( SURF, tile_ins ):
    """draws all tiles in list
        tile_ins : dictionary containing instances of all spawned tiles
    """
    #draw tiles in animation space first so that they are drawn at bottom
    for key in [ x for x in list(tile_ins.keys()) if len(x) == 3 ]  :
        if tile_ins[key]:
            tile_ins[key].draw( SURF )

    for key in [ x for x in list(tile_ins.keys()) if len(x) == 2 ]  :
        if tile_ins[key]:
            tile_ins[key].draw( SURF )

def tile_anim( tile_ins ):
    """calls animation handler of all tiles in tile_ins
        tile_ins : dictionary containing instances of all spawned tiles
    """
    for tile in list(tile_ins.values()) :
        if tile:
            tile.anim_handler()    



if __name__ == '__main__':
    pygame.init()

    SURF = pygame.display.set_mode(( WIN_SIZE, WIN_SIZE))
    pygame.display.set_caption("2048")

    clock = pygame.time.Clock()

    SURF.fill( BGCOLOR)

    t1 = tile ( (0,0) , 1 )
    tile_ins = { (0,0) : t1 }
    t1.set_grid( (2,0))

    while True:
        for event in pygame.event.get():
            if (event.type == QUIT ):
                pygame.quit()
                sys.exit()

        SURF.fill( BGCOLOR)

        #print tile.is_anim
        tile_anim( tile_ins )
        tile_draw( SURF , tile_ins)
            
        pygame.display.update()
        clock.tick(60)
