"""Size definitions"""

TILE_ORDER         = 4
TILE_PADDING       = 8
TILE_SIZE          = 63
TILE_RADIUS        = int( TILE_SIZE /20 )
WIN_SIZE           = TILE_ORDER*TILE_SIZE + (TILE_ORDER+1)*TILE_PADDING
HEADER_S           = 70


"""Methods definitions"""

import pygame
from pygame import gfxdraw

def rounded_rect( SURF, color, rect, radius) :
    """Draws a rounded rectangle on surface
        rect    : ( x, y, width, height)
        radius : radius of rounded edges
    """
    rect = pygame.Rect(rect)
    pos  = rect.topleft
    size = rect.size
    
    pygame.draw.rect( SURF , color , ( pos[0], pos[1] + radius, size[0], size[1] - 2*radius ) , 0 )

    pygame.draw.rect( SURF , color , ( pos[0] + radius, pos[1], size[0] - 2*radius, size[1] ) , 0 )

    #top-left circle
    pygame.draw.circle( SURF, color, ( pos[0] + radius, pos[1] + radius ), radius, 0 )
    pygame.gfxdraw.aacircle( SURF, pos[0] + radius, pos[1] + radius, radius, color )

    #top-right circle
    pygame.draw.circle( SURF, color, ( pos[0] + size[0] - radius, pos[1] + radius ), radius, 0 )
    pygame.gfxdraw.aacircle( SURF, pos[0] + size[0] - radius -1, pos[1] + radius, radius, color )

    #bottom-left circle
    pygame.draw.circle( SURF, color, ( pos[0] + radius, pos[1] + size[1] - radius ), radius, 0 )
    pygame.gfxdraw.aacircle( SURF, pos[0] + radius, pos[1] + size[1] - radius -1, radius, color )

    #bottom-right circle
    pygame.draw.circle( SURF, color, ( pos[0] + size[0] - radius, pos[1] + size[1] - radius ), radius, 0 )
    pygame.gfxdraw.aacircle( SURF, pos[0] + size[0] - radius -1, pos[1] + size[1] - radius -1, radius, color )



def get_pos( grid_pos ):
    """returns position on screen for given grid position ( x, y )
    """
    return [ TILE_PADDING * (grid_pos[0] + 1) + TILE_SIZE*grid_pos[0],
            TILE_PADDING * ( abs(grid_pos[1]) + 1) + TILE_SIZE * abs(grid_pos[1]) ]



def is_tile( grid_pos, tile_ins ):
    """checks whether a tile is present in a given grid position
    """
    return not tile_ins[grid_pos] == None


def get_color( color1, color2, degree):
    """return a color between color1 and color2 based on degree of tile
    """
    #factor between [0,1] based on degree
    factor = 1.0 if (degree > 7) else (degree-1)/6.0
    
    color = []
    for i in range(3):
        #linear interpolation
        color.append( int( color1[i] + factor*( color2[i] - color1[i] )) )
    return tuple(color)


def find_pairs( tile_ins ):
    """returns True if any pairs exist in board
    """
    for x in range(0, TILE_ORDER ):
        for y in range(0, -TILE_ORDER, -1):

            #if pair exists in x or y
            if tile_ins[( x, y)]:
                #check pair in x
                if ( x+1, y) in tile_ins.keys() and tile_ins[( x+1, y)] :
                    if tile_ins[( x, y)].degree == tile_ins[( x+1, y)].degree :
                        return True

                #check pair in y
                if ( x, y-1) in tile_ins.keys() and tile_ins[( x, y-1)] :
                    if tile_ins[( x, y)].degree == tile_ins[( x, y-1)].degree :
                        return True
    return False
 

def is_filled( tile_ins ):
    """returns True if board is filled
    """
    for tile in tile_ins.values():
        if tile == None:
            return False
    return True


#Movement Methods

#Need to find a way to merge all four in one function without making it complicated

def move_up( game_obj ):
    """moves tiles UP
    """
    #move top to bottom
    for x in range(0, TILE_ORDER):
        for y in range(0, -TILE_ORDER, -1):

            #continue if not a tile
            if not is_tile( (x,y), game_obj.tile_ins ) :
                continue

            #search for a tile to merge or move below it
            for srh_y in range(y+1, 1):
                
                if is_tile( ( x, srh_y), game_obj.tile_ins ):

                    #merge if degree is same
                    if game_obj.tile_ins[( x, srh_y)].degree == game_obj.tile_ins[( x, y)].degree :
                        game_obj.merge( (x, srh_y), ( x, y) )

                    #or move if found tile isn't adjacent
                    elif not srh_y-1 == y :
                        game_obj.move( (x, srh_y-1), (x, y) )
                    break

                #move to top if empty
                if srh_y == 0 and not is_tile( (x, srh_y), game_obj.tile_ins ):
                    game_obj.move( (x, srh_y), (x, y) )
                    break


def move_down( game_obj ):
    """moves tiles DOWN
    """
    #move bottom to top
    for x in range(0, TILE_ORDER):
        for y in range( 1-TILE_ORDER, 1):
            
            #continue if not a tile
            if not is_tile( (x,y), game_obj.tile_ins ) :
                continue

            #search for a tile to merge or move above it
            for srh_y in range(y-1, -TILE_ORDER, -1):
                
                if is_tile( ( x, srh_y), game_obj.tile_ins ):

                    #merge if degree is same
                    if game_obj.tile_ins[( x, srh_y)].degree == game_obj.tile_ins[( x, y)].degree :
                        game_obj.merge( (x, srh_y), ( x, y) )

                    #or move if found tile isn't adjacent
                    elif not srh_y+1 == y :
                        game_obj.move( (x, srh_y+1), (x, y) )
                    break

                #move to bottom if empty
                if srh_y == 1-TILE_ORDER and not is_tile( (x, srh_y), game_obj.tile_ins ):
                    game_obj.move( (x, srh_y), (x, y) )
                    break


def move_left( game_obj ):
    """moves tiles LEFT
    """
    #move left to right
    for y in range(0, -TILE_ORDER, -1):
        for x in range(0, TILE_ORDER):

            #continue if not a tile
            if not is_tile( (x,y), game_obj.tile_ins ) :
                continue

            #search for a tile to merge or move to its right
            for srh_x in range(x-1, -1, -1):
                
                if is_tile( ( srh_x, y), game_obj.tile_ins ):

                    #merge if degree is same
                    if game_obj.tile_ins[( srh_x, y)].degree == game_obj.tile_ins[( x, y)].degree :
                        game_obj.merge( (srh_x, y), ( x, y) )

                    #or move if found tile isn't adjacent
                    elif not srh_x+1 == x :
                        game_obj.move( (srh_x +1, y), (x, y) )
                    break

                #move to left most position if empty
                if srh_x == 0 and not is_tile( (srh_x, y), game_obj.tile_ins ):
                    game_obj.move( (srh_x, y), (x, y) )
                    break


def move_right( game_obj ):
    """moves tiles RIGHT
    """
    #move right to left
    for y in range(0, -TILE_ORDER, -1):
        for x in range( TILE_ORDER-1, -1, -1):

            #continue if not a tile
            if not is_tile( (x,y), game_obj.tile_ins ) :
                continue

            #search for a tile to merge or move to its left
            for srh_x in range(x+1, TILE_ORDER ):
                
                if is_tile( ( srh_x, y), game_obj.tile_ins ):

                    #merge if degree is same
                    if game_obj.tile_ins[( srh_x, y)].degree == game_obj.tile_ins[( x, y)].degree :
                        game_obj.merge( (srh_x, y), ( x, y) )

                    #or move if found tile isn't adjacent
                    elif not srh_x-1 == x :
                        game_obj.move( (srh_x -1, y), (x, y) )
                    break

                #move to right most position if empty
                if srh_x == TILE_ORDER-1 and not is_tile( (srh_x, y), game_obj.tile_ins ):
                    game_obj.move( (srh_x, y), (x, y) )
                    break








        
    

