import xmltodict
import pygame
import myvector

class Map:

    def __init__(self, file_name):

        # sets values to their defaults or empty structures
        self.mMapWidth = 0          # width of map (in tiles)
        self.mMapHeight = 0         # height of map (in tiles)
        self.mTileWidth = 0         # width of a single tile
        self.mTileHeight = 0        # height of a single tile
        self.mTileOffsetX = 0       # number of pixels between each tile horizontally
        self.mTileOffsetY = 0       # number of pixels between each tile vertically
        self.mOrientation = ""      # orientation of camera
        self.mTileSet = ""          # tile set filename
        self.mTileImage = None      # pygame surface containing tile image
        self.mTileImageNumX = 0     # number of tiles horizontally
        self.mTileImageNumY = 0     # number of tiles vertically
        self.mData = []             # tile codes
        self.mCamX = 0              # camera x coordinate
        self.mCamY = 0              # camera y coordinate
        self.mInitialPlayerPositionVector = myvector.Vector2(0, 0) # initial player vector
        self.mNewLevelLoaded = False    # boolean that signals the main program when a new level has been loaded
        self.mJoystickEnabled = False   # boolean that keeps track if we have a joystick available
        self.mWallCodes = []
        self.mHitDetectionExceptionCodes = []
        self.mDarkeningTiles = []
        self.mLastTileLocation = myvector.Vector2(0, 0)
        self.mCurrentTileLocation = myvector.Vector2(0, 0)

        # process TMX file w/ CSV data
        Map.parse_tmx(self, file_name)
        for i in range(10,0,-1):
            darken_percent = i * .1
            dark = pygame.Surface((self.mTileWidth, self.mTileHeight)).convert_alpha()
            dark.fill((0, 0, 0, darken_percent * 255))
            self.mDarkeningTiles.append(dark)

        self.mLightMap = []
        for i in range (self.mMapHeight):
            row=[]
            for j in range (self.mMapWidth):
                row.append(0)
            self.mLightMap.append(row)

    def parse_tmx(self, file_name):
        with open(file_name) as parser:
            map_dict = xmltodict.parse(parser.read())   # xmltodict needs a bytes-type object, so we feed it the file parser

        parser.close()

        #pprint.pprint(map_dict)

        # The standard attributes are easily pulled out from the newly created dictionary
        self.mOrientation = map_dict['map']['@orientation']
        self.mMapWidth = int(map_dict['map']['@width'])
        self.mMapHeight = int(map_dict['map']['@height'])
        self.mTileWidth = int(map_dict['map']['@tilewidth'])
        self.mTileHeight = int(map_dict['map']['@tileheight'])
        if  isinstance(map_dict['map']['tileset'], list):
            self.mTileSet = map_dict['map']['tileset'][0]['image']['@source']
        else:
            self.mTileSet = map_dict['map']['tileset']['image']['@source']

        if isinstance(map_dict['map']['layer'], dict):
            if map_dict['map']['layer']['data']['@encoding'] == 'csv':
                layer=[]
                map_text=map_dict['map']['layer']['data']['#text']
                map_text_lines=map_text.split("\n")     # data in XML is stored as one giant string with newline characters
                                                        # so it is broken up into separate line by splitting with those characters
                for line in map_text_lines:
                    lineData = line.split(",")
                    if lineData[-1] == '':              # on the last line, there's no space, so only
                        lineData = lineData[:-1]        # trim off the last item if it's a space
                    layer.append(lineData)              # gather the list for this line of the map and append it to the layer

                self.mData.append(layer)                # add this layer to the map data list
                    # Throws an exception if TMX file map data is encoded in any way other than CSV
            else:
                raise IOError("TMX File MUST contain map data in CSV format")
        else:
            for tile_layer in map_dict['map']['layer']:
                # check that the data is encoded in CSV
                if tile_layer['data']['@encoding'] == 'csv':
                    layer=[]
                    map_text=tile_layer['data']['#text']
                    map_text_lines=map_text.split("\n")     # data in XML is stored as one giant string with newline characters
                                                            # so it is broken up into separate line by splitting with those characters
                    for line in map_text_lines:
                        lineData = line.split(",")
                        if lineData[-1] == '':              # on the last line, there's no space, so only
                            lineData = lineData[:-1]        # trim off the last item if it's a space
                        layer.append(lineData)              # gather the list for this line of the map and append it to the layer

                    self.mData.append(layer)                # add this layer to the map data list
                        # Throws an exception if TMX file map data is encoded in any way other than CSV
                else:
                    raise IOError("TMX File MUST contain map data in CSV format")

        self.mTileImage = pygame.image.load(self.mTileSet)
        self.mTileImage.convert()
        self.mTileImage.convert_alpha()
        self.mTileImageNumX = self.mTileImage.get_width() // self.mTileWidth
        self.mTileImageNumY = self.mTileImage.get_height() // self.mTileHeight

    def draw(self, dest_surf, player_pos_vector):
        tile_col = (player_pos_vector.x // (self.mTileWidth + self.mTileOffsetX)) # tile column for upper left corner of rectangle
        tile_row = (player_pos_vector.y // (self.mTileHeight + self.mTileOffsetY)) # tile row for upper left corner of rectangle
        self.mCurrentTileLocation = myvector.Vector2(tile_col, tile_row)
        if (int(self.mLastTileLocation.x) != int(self.mCurrentTileLocation.x)) or (int(self.mLastTileLocation.y) != int(self.mCurrentTileLocation.y)):
            self.update_light_map()
            self.mLastTileLocation = self.mCurrentTileLocation.copy()

        src_surf = self.mTileImage
        start_col = self.mCamX // (self.mTileWidth + self.mTileOffsetX)
        start_row = self.mCamY // (self.mTileHeight + self.mTileOffsetY)

        for layer_num in range(0, len(self.mData)):
            row_num=int(start_row)
            col_num=int(start_col)
            dest_y = 0 - (self.mCamY % self.mTileWidth)

            while dest_y < dest_surf.get_height():
                dest_x = 0 -(self.mCamX % self.mTileWidth)
                while dest_x < dest_surf.get_width():
                    if row_num < self.mMapHeight and col_num < self.mMapWidth:
                        tile_code = int(self.mData[int(layer_num)][int(row_num)][int(col_num)])
                        diagonal_flipped = False
                        vertical_flipped = False
                        horizontal_flipped = False

                        if tile_code < 0:               # We know bit 32 is 1 since it's negative
                            horizontal_flipped = True   # if it is, the tile is horizontally flipped
                            tile_code += 2147483648     # add 2^31 to shift it back to the positive

                        if tile_code > 1073741824:    # check if bit 31 is set
                            vertical_flipped = True     # if it is, the tile is vertically flipped
                            tile_code -= 1073741824     # and subtract 2^30 from the final tile code

                        if tile_code > 536870912:       # next check if bit 30 is set
                            diagonal_flipped = True     # if it is, the tile is diagonally flipped
                            tile_code -= 536870912      # and subtract 2^29 from the final tile code

                        light_strength = self.mLightMap[row_num][col_num]

                        if tile_code != 0 and tile_code != 1 and light_strength > 0:
                            image_row = (tile_code - 1) // self.mTileImageNumX
                            image_col = (tile_code - 1) % self.mTileImageNumX
                            src_x = image_col * (self.mTileWidth + self.mTileOffsetX)   # top left corner of tile (x)
                            src_y = image_row * (self.mTileHeight + self.mTileOffsetY)  # top left corner of tile (y)

                            # create surface to fill with tile image
                            tile_image = pygame.Surface((self.mTileWidth, self.mTileHeight))
                            tile_image.convert()
                            tile_image.convert_alpha()

                            # blit image from tileset to tile image surface
                            tile_image.blit(src_surf, (0, 0), (src_x, src_y, self.mTileWidth, self.mTileHeight))

                            if light_strength < 10:
                                tile_image.blit(self.mDarkeningTiles[light_strength], (0,0))

                            if diagonal_flipped == True:
                                tile_image = pygame.transform.rotate(tile_image, 90)    # rotates 90 degrees counterclockwise
                                tile_image = pygame.transform.flip(tile_image, False, True) # flips vertically
                            if horizontal_flipped == True or vertical_flipped == True:
                                tile_image = pygame.transform.flip(tile_image, horizontal_flipped, vertical_flipped)    # uses boolean values of horizontal/vertical flipping

                            dest_surf.blit(tile_image, (dest_x, dest_y))
                    col_num += 1
                    dest_x += self.mTileWidth
                col_num = start_col
                row_num += 1
                dest_y += self.mTileHeight

    def update_light_map(self):
        light_range = 6
        player_col = int(self.mCurrentTileLocation.x)
        player_row = int(self.mCurrentTileLocation.y)
        start_col = max(0, (player_col - light_range))
        start_row = max(0, (player_row - light_range))
        end_col = min(player_col + light_range, self.mMapWidth)
        end_row = min(player_row + light_range, self.mMapHeight)
        for i in range(start_row, end_row):
            for j in range(start_col, end_col):
                light_strength = 13 - (abs(player_row - i) + abs(player_col - j))
                # awprint("i:",i,"j",j)
                if self.mLightMap[i][j] < light_strength:
                    self.mLightMap[i][j] = light_strength

    def clear_for_new_map(self, file_name):
        self.__init__(file_name)
        self.mNewLevelLoaded = True

    def is_tile_empty(self, tile_surf):
        color_at_last_pixel = tile_surf.get_at((0,0))
        for y in range(tile_surf.get_height()):
            for x in range (tile_surf.get_width()):
                color_at_pixel = tile_surf.get_at((x,y))
                if (color_at_last_pixel.r != color_at_pixel.r) or (color_at_last_pixel.g != color_at_pixel.g) or (color_at_last_pixel.b != color_at_pixel.b):
                    return False
        return True

    def test_tiles(self, image_file):
        thisTileImage = pygame.image.load(image_file)
        thisTileImage.convert()
        thisTileImage.convert_alpha()
        thisTileImageNumX = thisTileImage.get_width() // self.mTileWidth
        thisTileImageNumY = thisTileImage.get_height() // self.mTileHeight
        for row in range (thisTileImageNumX+1):
            for col in range (thisTileImageNumY+1):
                src_x = col * (self.mTileWidth + self.mTileOffsetX)  # top left corner of tile (x)
                src_y = row * (self.mTileHeight + self.mTileOffsetY)  # top left corner of tile (y)

                # create surface to fill with tile image
                tile_image = pygame.Surface((self.mTileWidth, self.mTileHeight))
                tile_image.convert()
                tile_image.convert_alpha()
                tile_image.fill((0,0,0,0))

                # blit image from tileset to tile image surface
                tile_image.blit(thisTileImage, (0, 0), (src_x, src_y, self.mTileWidth, self.mTileHeight))
                is_empty = self.is_tile_empty(tile_image)
                if is_empty:
                    is_empty_text = "O"
                else:
                    is_empty_text = "X"

                print("(", row, ",", col, ") ", is_empty_text, sep="", end=" ")
            print("")

    # This checks every tile inside of a given rectangle on the map (given in pixel location) to see if it matches any of the given list of tile codes
    def overlaps(self, rectangle, code_list):
        min_x_tile = (rectangle[0]) // (self.mTileWidth + self.mTileOffsetX)  # tile column for upper left corner of rectangle
        max_x_tile = (rectangle[0] + rectangle[2]) // (self.mTileWidth + self.mTileOffsetX) # tile column for bottom right corner of rectangle
        min_y_tile = (rectangle[1]) // (self.mTileHeight + self.mTileOffsetY) # tile row for upper left corner of rectangle
        max_y_tile = (rectangle[1] + rectangle[3]) // (self.mTileWidth + self.mTileOffsetX) # tile row for bottom right corner of rectangle
        for layer_num in range(0, len(self.mData)):                     # QUADRUPLE
            for column in range(int(min_x_tile), int(max_x_tile) + 1):            # NESTED
                if column >= 0 and column < self.mMapWidth:            # no need to check negative or off-the-map columnn
                    for row in range(int(min_y_tile), int(max_y_tile) + 1):           # FOOOOOOOOR
                        if row >= 0 and row < self.mMapHeight:             # no need to check negative or off-the-map row
                            for tile_code in code_list:                         # LOOOOOOOOP
                                if tile_code < 0:  # We know bit 32 is 1 since it's negative
                                    tile_code += 2147483648  # add 2^31 to shift it back to the positive
                                if tile_code > 1073741824:  # check if bit 31 is set
                                    tile_code -= 1073741824  # and subtract 2^30 from the final tile code
                                if tile_code > 536870912:  # next check if bit 30 is set
                                    tile_code -= 536870912  # and subtract 2^29 from the final tile code
                                if int(self.mData[layer_num][row][column]) == int(tile_code):
                                    return True
        return False