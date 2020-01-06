import pygame
import myvector
import os
import random
import numpy
import pprint

class RandomMap:
    def __init__(self):
        self.mRandomMapTemplateList = []
        self.mTileWidth = 64
        self.mTileHeight = 64
        self.mData = []
        self.mNMap = numpy.array([0,0,0])
        self.mMapHeight = 0
        self.mMapWidth = 0
        self.mCamX = 0
        self.mCamY = 0
        self.mCurrentMapNumber = 0
        self.mCurrentTemplateNumber = 0
        self.mExitLocation = myvector.MyVector2(0, 0)
        self.mEntranceLocation = myvector.MyVector2(0, 0)
        self.mExitTriggered = False
        self.mDarkeningTiles = []
        self.mLightMap = []
        self.mRoomList = []
        self.mEnemyList = []
        self.mCorridorList = []
        self.mLastTileLocation = myvector.MyVector2(0, 0)
        self.mCurrentTileLocation = myvector.MyVector2(0, 0)
        self.mPlayerStartVector = myvector.MyVector2(0, 0)
        self.mTileImageNumX = 0     # number of tiles horizontally
        self.mTileImageNumY = 0     # number of tiles vertically
        self.mTileImage = None
        self.mMiniMapUpdateTimer = 0
        for i in range(10,0,-1):
            darken_percent = (i * .1) - .05
            dark = pygame.Surface((self.mTileWidth, self.mTileHeight)).convert_alpha()
            dark.fill((0, 0, 0, darken_percent * 255))
            self.mDarkeningTiles.append(dark)

        for file in os.listdir("templates"):
            if file.endswith(".png"):
                file_location = os.path.join("templates", file)
                self.mRandomMapTemplateList.append(RandomMapTemplate(file_location))

        self.generate_new_map()



    def generate_mini_map(self):
        lazy_update_timer_count = 0.03
        self.mMiniMapUpdateTimer += lazy_update_timer_count
        if self.mMiniMapUpdateTimer >= 1.0:
            self.mMiniMapUpdateTimer = 0
            self.mMinimap.fill((0,0,0,255))
            for row in range(0, self.mMapHeight):
                for col in range(0, self.mMapWidth):
                    light_strength = min(self.mLightMap[row][col], 10)
                    light_strength *= 0.1
                    color = myvector.MyVector3(light_strength,light_strength,light_strength)
                    self.mMinimap.set_at((col, row), color.colorTuple)

    def generate_new_map(self):
        self.mData=[]
        self.mEnemyList=[]
        self.mCurrentMapNumber += 1
        self.mRoomList = []

        map_template = self.mCurrentTemplateNumber
        while(map_template == self.mCurrentTemplateNumber):
            map_template = random.randint(0, len(self.mRandomMapTemplateList) - 1)

        self.mCurrentTemplateNumber = map_template

        self.mTileImage = self.mRandomMapTemplateList[self.mCurrentTemplateNumber].mTileImage
        self.mTileImageNumX = self.mRandomMapTemplateList[self.mCurrentTemplateNumber].mTileImageNumX     # number of tiles horizontally
        self.mTileImageNumY = self.mRandomMapTemplateList[self.mCurrentTemplateNumber].mTileImageNumY     # number of tiles vertically

        # figure out map size
        self.mMapWidth = 50 + random.randint(self.mCurrentMapNumber, int(1.5*self.mCurrentMapNumber))
        self.mMapHeight = 50 + random.randint(self.mCurrentMapNumber, int(1.5*self.mCurrentMapNumber))
        self.mMinimap = pygame.Surface((self.mMapWidth, self.mMapHeight))


        self.load_with_ground()

        room_count = 3 + random.randint(self.mCurrentMapNumber//20, self.mCurrentMapNumber//10)
        # bonus_rooms_count= 4 + random.randint(self.mCurrentMapNumber//3, self.mCurrentMapNumber//2)
        large_room_count =  (room_count) + random.randint(0,3)
        large_room_count_copy = large_room_count

        print("RC:",room_count, large_room_count)

        while (room_count > 0):
            try_again = False
            while (large_room_count > 0):
                try_again = False
                new_room = Room(True, False, self)
                for room in self.mRoomList:
                    if room.collides(new_room):
                        try_again = True
                if not try_again:
                    self.mRoomList.append(new_room)
                    large_room_count-= 1
            start_room = random.choice(self.mRoomList)

            try_again = False
            new_room = Room(False, False, self)
            for room in self.mRoomList:
                if room.collides(new_room):
                    try_again = True
                    new_room.mRoomTemplate = room.mRoomTemplate
            if not try_again:
                self.mRoomList.append(new_room)
                room_count -= 1

        i=0
        for j in range(1, large_room_count_copy):
            longest_distance = 0
            exit_room = 0
            dist = myvector.distance(self.mRoomList[i].mCenter, self.mRoomList[j].mCenter)
            if dist > longest_distance:
                longest_distance = dist
                exit_room = j

        self.mPlayerStartVector=self.place_entrance(0)
        self.place_exit(j)

        i=0
        for j in range(1, len(self.mRoomList)):
                # if self.mRoomList[i].collides(self.mRoomList[j]):
                #     self.mRoomList[j].mRoomTemplate = self.mRoomList[i].mRoomTemplate
                cor = [Corridor(self, self.mRoomList[i].mCenter, self.mRoomList[j].mCenter)]
                cor += [Corridor(self, self.mRoomList[j].mCenter, self.mRoomList[i].mCenter, True)]

                cor = [Corridor(self, self.mRoomList[j].mCenter, self.mRoomList[i].mCenter)]
                cor += [Corridor(self, self.mRoomList[i].mCenter, self.mRoomList[j].mCenter, True)]

                self.mRoomList[j].mNumConnections += 1
                self.mCorridorList += cor

        total_connections = 0
        connection_goal = int(len(self.mRoomList) - 2)
        while total_connections < connection_goal:
            i = random.randint(1, len(self.mRoomList)-1)
            j = random.randint(1, len(self.mRoomList)-1)
            if (i != j):
                if self.mRoomList[i].mNumConnections < 3:
                    cor = [Corridor(self, self.mRoomList[i].mCenter, self.mRoomList[j].mCenter)]
                    cor += [Corridor(self, self.mRoomList[j].mCenter, self.mRoomList[i].mCenter, True)]
                    self.mRoomList[j].mNumConnections += 1
                    self.mCorridorList += cor
                    total_connections += 1

        for i in range (0, len(self.mCorridorList)):
            for j in range(i, len(self.mCorridorList)):
                if self.mCorridorList[i].collides(self.mCorridorList[j]):
                    self.mCorridorList[j].mCorridorTemplate = self.mCorridorList[i].mCorridorTemplate

        for corridor in self.mCorridorList:
            self.carve_out_corridor(corridor)

        self.mRoomList[0].isEntrance = True

        #self.mPlayerStartVector = myvector.MyVector2(self.mRoomList[0].mCenter.x * self.mTileWidth, self.mRoomList[0].mCenter.y * self.mTileHeight)

        for room in self.mRoomList:
            self.carve_out_room(room)

        self.mLightMap = []
        self.generate_light_map()
        self.generate_nmap()
        self.mExitTriggered = False

    def generate_nmap(self):
        rows_list = []
        for row_num in range(self.mMapHeight):
            row_code_list = []
            for col_num in range(self.mMapWidth):
                tile_code = self.mData[0][row_num][col_num]
                if tile_code == 2:
                    row_code_list += [1]
                elif tile_code == 1:
                    row_code_list += [0]
                else:
                    raise ValueError("Number Not Expected!")
            rows_list.append(row_code_list)
        self.mNMap = numpy.array(rows_list)

    def generate_light_map(self):
        self.mLightMap = []
        for i in range (self.mMapHeight):
            row=[]
            for j in range (self.mMapWidth):
                row.append(0)
            self.mLightMap.append(row)

    def load_with_ground(self):
        self.mData = []
        for layer_num in range(0, 2):
            this_layer = []
            for row in range(0, self.mMapHeight):
                this_row=[]
                for col in range(0, self.mMapWidth):
                    if layer_num == 0:
                        # this_row.append(2)
                       this_row.append(self.mRandomMapTemplateList[self.mCurrentTemplateNumber].mBaseWallCode)
                    elif layer_num == 1:
                        this_row.append(0)
                this_layer.append(this_row)
            self.mData.append(this_layer)

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

    def overlaps(self, rectangle):
        min_x_tile = (rectangle[0]) // self.mTileWidth  # tile column for upper left corner of rectangle
        max_x_tile = (rectangle[0] + rectangle[2]) // self.mTileWidth # tile column for bottom right corner of rectangle
        min_y_tile = (rectangle[1]) // self.mTileHeight # tile row for upper left corner of rectangle
        max_y_tile = (rectangle[1] + rectangle[3]) // self.mTileWidth # tile row for bottom right corner of rectangle
        #for layer_num in range(0, len(self.mData)):                     # QUADRUPLE
        layer_num = 0
        for column in range(int(min_x_tile), int(max_x_tile) + 1):            # ONLY DOUBLE NESTED
            if column >= 0 and column < self.mMapWidth:            # no need to check negative or off-the-map columnn
                for row in range(int(min_y_tile), int(max_y_tile) + 1):           # FOOOOOOOOR LOOOOOPS
                    if row >= 0 and row < self.mMapHeight:             # no need to check negative or off-the-map row
                        tile_code = self.mData[layer_num][row][column]
                        tile_code2 = self.mData[1][row][column]
                        tileset_row = tile_code // self.mTileImageNumX
                        if (tile_code2 == 4):
                            self.mExitTriggered = True
                        if (tile_code == 1) or (tileset_row % 2 == 1):
                            return True
                        elif (tile_code == 4):
                            self.mExitTriggered = True
        return False

    def draw(self, dest_surf, player_pos_vector):
        tile_col = (player_pos_vector.x // self.mTileWidth) # tile column for upper left corner of rectangle
        tile_row = (player_pos_vector.y // self.mTileHeight) # tile row for upper left corner of rectangle
        self.mCurrentTileLocation = myvector.MyVector2(tile_col, tile_row)
        if (int(self.mLastTileLocation.x) != int(self.mCurrentTileLocation.x)) or (int(self.mLastTileLocation.y) != int(self.mCurrentTileLocation.y)):
            self.update_light_map()
            self.mLastTileLocation = self.mCurrentTileLocation.copy()

        src_surf = self.mTileImage
        start_col = self.mCamX // self.mTileWidth
        start_row = self.mCamY // self.mTileHeight

        for layer_num in range(0, len(self.mData)):
            row_num=int(start_row)
            col_num=int(start_col)
            dest_y = 0 - (self.mCamY % self.mTileWidth)

            while dest_y < dest_surf.get_height():
                dest_x = 0 -(self.mCamX % self.mTileWidth)
                while dest_x < dest_surf.get_width():
                    if row_num < self.mMapHeight and col_num < self.mMapWidth:
                        tile_code = int(self.mData[int(layer_num)][int(row_num)][int(col_num)])

                        light_strength = self.mLightMap[row_num][col_num]

                        if tile_code != 0:
                            image_row = tile_code // self.mTileImageNumX
                            image_col = tile_code % self.mTileImageNumX
                            src_x = image_col * self.mTileWidth   # top left corner of tile (x)
                            src_y = image_row * self.mTileHeight  # top left corner of tile (y)

                            # create surface to fill with tile image
                            tile_image = pygame.Surface((self.mTileWidth, self.mTileHeight))
                            tile_image.convert()
                            tile_image.convert_alpha()

                            # blit image from tileset to tile image surface
                            tile_image.blit(src_surf, (0, 0), (src_x, src_y, self.mTileWidth, self.mTileHeight))

                            if light_strength < 10:
                                tile_image.blit(self.mDarkeningTiles[light_strength], (0,0))

                            dest_surf.blit(tile_image, (dest_x, dest_y))
                    col_num += 1
                    dest_x += self.mTileWidth
                col_num = start_col
                row_num += 1
                dest_y += self.mTileHeight

        self.generate_mini_map()
        dest_surf.blit(self.mMinimap, ((1024-self.mMinimap.get_width()-16),(768-self.mMinimap.get_height()-16)))

        if self.mExitTriggered:
            self.generate_new_map()
            return self.mPlayerStartVector

    def carve_out_room(self, room):
        for row in range (room.mStartRow, room.mStartRow+room.mHeight):
            for col in range(room.mStartCol, room.mStartCol+room.mWidth):
                tile_code = self.mData[0][row][col]
                if (row == room.mStartRow) or (row==(room.mStartRow+room.mHeight-1)):
                    pass
                    #if  tile_code == 1:
                        #self.mData[0][row][col] = random.choice(room.mRoomTemplate.mWallCodesList)
                    #    self.mData[0][row][col] = 1
                elif (col == room.mStartCol) or (col == (room.mStartCol+room.mWidth-1)):
                    pass
                    #if tile_code == 1 or (self.is_corridor(tile_code) and self.is_wall(tile_code)):
                        #self.mData[0][row][col] = random.choice(room.mRoomTemplate.mWallCodesList)
                     #   self.mData[0][row][col] = 1
                else:
                    if tile_code == 1 or self.is_wall(tile_code) or self.is_corridor(tile_code):
                        #self.mData[0][row][col] = random.choice(room.mRoomTemplate.mFloorCodesList)
                        self.mData[0][row][col] = 2

    def carve_out_corridor(self, corridor):
        if corridor.mVertical:
            #print("V: start_col =", corridor.mStartCol, "start_row =", corridor.mStartRow, "end_col=", corridor.mEndCol, "end_row=", corridor.mEndRow)
            for col in range(corridor.mStartCol, corridor.mEndCol):
                for row in range(corridor.mStartRow, corridor.mEndRow):
                    if (row < len(self.mData[0])) and (col < len(self.mData[0][row])):
                        tile_code = self.mData[0][row][col]
                        if col == corridor.mStartCol or col == corridor.mEndCol:
                            pass
                            #if tile_code == 1 or self.is_wall(tile_code):
                            #    #self.mData[0][row][col] = random.choice(corridor.mCorridorTemplate.mWallCodesList)
                            #    self.mData[0][row][col] = 1
                        else:
                            #self.mData[0][row][col] = random.choice(corridor.mCorridorTemplate.mFloorCodesList)
                            self.mData[0][row][col] = 2
        if corridor.mHorizontal:
            #print("H: start_col =", corridor.mStartCol, "start_row =", corridor.mStartRow, "end_col=", corridor.mEndCol,
                  #"end_row=", corridor.mEndRow)
            for col in range(corridor.mStartCol, corridor.mEndCol):
                for row in range(corridor.mStartRow, corridor.mEndRow):
                    if (row < len(self.mData[0])) and (col < len(self.mData[0][row])):
                        tile_code = self.mData[0][row][col]
                        if row == corridor.mStartRow or col == corridor.mEndRow:
                            pass
                            #if tile_code == 1 or self.is_wall(tile_code):
                                #self.mData[0][row][col] = random.choice(corridor.mCorridorTemplate.mWallCodesList)
                            #    self.mData[0][row][col] = 1
                        else:
                            #self.mData[0][row][col] = random.choice(corridor.mCorridorTemplate.mFloorCodesList)
                            self.mData[0][row][col] = 2

    def is_wall(self, tile_code):
        tileset_row = tile_code // self.mTileImageNumX
        if (tile_code == 1) or (tileset_row % 2 == 1):
            return True
        return False

    def is_floor(self, tile_code):
        tileset_row = tile_code // self.mTileImageNumX
        if (tile_code == 2):
            return True
        if (tileset_row > 0) and (tileset_row % 2 == 2):
            return True
        return False

    def is_corridor(self, tile_code):
        current_corridor_template_list = self.mRandomMapTemplateList[self.mCurrentTemplateNumber].mCorridoorTemplateList
        for template in current_corridor_template_list:
            if template.mWallCodesList.count(tile_code) > 0:
                return True
            if template.mFloorCodesList.count(tile_code) > 0:
                return True
        return False

    def place_exit(self, room):
        spot_col = random.randint(self.mRoomList[room].mStartCol+2, self.mRoomList[room].mEndCol-2)
        spot_row = random.randint(self.mRoomList[room].mStartRow+2, self.mRoomList[room].mEndRow-2)
        # flip_h_or_v = random.randint(0,1)
        # flip_end_or_beg = random.randint(0,1)
        # if flip_h_or_v == 1:
        #     if flip_end_or_beg == 1:
        #        # vertical and beginning
        #         spot_col = self.mRoomList[room].mStartCol
        #         spot_row = random.randint(self.mRoomList[room].mStartRow + 1,self.mRoomList[room].mEndRow - 1 )
        #     else:
        #         # vertical and end
        #         spot_col = self.mRoomList[room].mEndCol
        #         spot_row = random.randint(self.mRoomList[room].mStartRow + 1, self.mRoomList[room].mEndRow - 1)
        # else:
        #     if flip_end_or_beg == 1:
        #        # horizontal and beginning
        #         spot_row = self.mRoomList[room].mStartRow
        #         spot_col = random.randint(self.mRoomList[room].mStartCol + 1,self.mRoomList[room].mEndCol - 1 )
        #     else:
        #         # vertical and end
        #         spot_row = self.mRoomList[room].mEndRow
        #         spot_col = random.randint(self.mRoomList[room].mStartCol + 1, self.mRoomList[room].mEndCol - 1)
        self.mData[1][spot_row][spot_col] = 4


    def place_entrance(self, room):

        spot_col = random.randint(self.mRoomList[room].mStartCol+2, self.mRoomList[room].mEndCol-2)
        spot_row = random.randint(self.mRoomList[room].mStartRow+2, self.mRoomList[room].mEndRow-2)

        # flip_h_or_v = random.randint(0,1)
        # flip_end_or_beg = random.randint(0,1)
        # if flip_h_or_v == 1:
        #     if flip_end_or_beg == 1:
        #        # vertical and beginning
        #         spot_col = self.mRoomList[room].mStartCol
        #         spot_row = random.randint(self.mRoomList[room].mStartRow + 1,self.mRoomList[room].mEndRow - 1 )
        #     else:
        #         # vertical and end
        #         spot_col = self.mRoomList[room].mEndCol
        #         spot_row = random.randint(self.mRoomList[room].mStartRow + 1, self.mRoomList[room].mEndRow - 1)
        # else:
        #     if flip_end_or_beg == 1:
        #        # horizontal and beginning
        #         spot_row = self.mRoomList[room].mStartRow
        #         spot_col = random.randint(self.mRoomList[room].mStartCol + 1,self.mRoomList[room].mEndCol - 1 )
        #     else:
        #         # vertical and end
        #         spot_row = self.mRoomList[room].mEndRow
        #         spot_col = random.randint(self.mRoomList[room].mStartCol + 1, self.mRoomList[room].mEndCol - 1)
        self.mData[1][spot_row][spot_col] = 3
        return myvector.MyVector2(spot_col*self.mTileHeight, spot_row*self.mTileWidth)

class Room():
    def __init__(self, is_big, is_very_big, rm_base):
        self.mWidth = 0
        self.mHeight = 0
        self.mStartRow = 0
        self.mStartCol = 0
        roll = random.randint(1, 3)
        if is_big:
            if roll == 1:
                self.mWidth = random.randint(10, 13)
                self.mHeight = random.randint(10, 13)
            elif roll == 2:
                self.mWidth = random.randint(7, 9)
                self.mHeight = random.randint(12, 15)
            else:
                self.mWidth = random.randint(12, 15)
                self.mHeight = random.randint(7, 9)
        elif is_very_big:
            if roll == 1:
                self.mWidth = random.randint(14, 16)
                self.mHeight = random.randint(14, 16)
            elif roll == 2:
                self.mWidth = random.randint(10, 12)
                self.mHeight = random.randint(16, 19)
            else:
                self.mWidth = random.randint(16, 19)
                self.mHeight = random.randint(10, 12)
        else:
            if roll == 1:
                self.mWidth = random.randint(6, 8)
                self.mHeight = random.randint(6, 8)
            elif roll == 2:
                self.mWidth = random.randint(5, 7)
                self.mHeight = random.randint(9, 11)
            else:
                self.mWidth = random.randint(9, 11)
                self.mHeight = random.randint(5, 7)
        self.mStartRow = random.randint(1, rm_base.mMapHeight-self.mHeight-2)
        self.mStartCol = random.randint(1, rm_base.mMapWidth-self.mWidth-2)
        self.mEndCol = self.mStartCol + self.mWidth
        self.mEndRow = self.mStartRow + self.mHeight
        self.mConnectWithCorridor = True
        self.mIsNowConnected = False
        self.mNumConnections = 0
        self.mIsEntrance = False
        self.mIsExit = False

        self.mRoomTemplate = random.choice(rm_base.mRandomMapTemplateList[rm_base.mCurrentTemplateNumber].mRoomTemplateList)

        self.mCenter = myvector.MyVector2(self.mStartCol + (self.mWidth // 2), self.mStartRow + (self.mHeight // 2))

        #print("self.mStartCol =", self.mStartCol, "self.mStartRow =", self.mStartRow, "self.mEndCol =", self.mEndCol, "self.mEndRow =", self.mEndRow, "self.mCenter =", self.mCenter)

    def collides(self, other_room):
        if (self.mStartCol > other_room.mEndCol) or (other_room.mStartCol > self.mEndCol):
            return False
        if (self.mStartRow > other_room.mEndRow) or (other_room.mStartRow > self.mEndRow):
            return False
        return True

class Corridor():
    def __init__(self, rm_base, center_1, center_2, flip_dir=False):
        self.mStartRow = 0
        self.mEndRow = 0
        self.mStartCol = 0
        self.mEndCol = 0
        self.mVertical = False
        self.mHorizontal = False

        direction_test = center_1 - center_2
        if abs((center_1.y - center_2.y)) > abs((center_1.x - center_2.x)):
            self.mVertical = True
        if flip_dir:
            self.mVertical = not self.mVertical

        self.mHorizontal = not self.mVertical

        #print("C1: ", center_1,"C2: ",center_2)

        if self.mHorizontal:
            self.mStartRow = max(1, int(center_1.y) - 2)
            self.mEndRow = min(self.mStartRow + 3, rm_base.mMapHeight-2)
            smallest_x = min(int(center_1.x), int(center_2.x))
            largest_x = max(int(center_1.x), int(center_2.x))
            smallest_x -= 2
            largest_x += 2
            self.mStartCol = max(1, smallest_x)
            self.mEndCol = min(rm_base.mMapWidth-2, largest_x)
        else:
            self.mStartCol = max(1, int(center_1.x) - 2)
            self.mEndCol = min(self.mStartCol + 3, rm_base.mMapWidth-2)
            smallest_y = min(int(center_1.y), int(center_2.y))
            largest_y = max(int(center_1.y), int(center_2.y))
            smallest_y -= 2
            largest_y += 2
            self.mStartRow = max(1, smallest_y)
            self.mEndRow = min(rm_base.mMapHeight-2, largest_y)

        self.mStartRow = max(min(self.mStartRow, rm_base.mMapHeight-1), 1)
        self.mEndRow = max(min(self.mEndRow, rm_base.mMapHeight - 1), 1)

        self.mStartCol = max(min(self.mStartCol, rm_base.mMapWidth-1), 1)
        self.mEndCol = max(min(self.mEndCol, rm_base.mMapWidth - 1), 1)

        self.mHeight = self.mEndRow - self.mStartRow
        self.mWidth = self.mEndCol - self.mStartCol

        self.mCorridorTemplate = random.choice(
            rm_base.mRandomMapTemplateList[rm_base.mCurrentTemplateNumber].mCorridoorTemplateList)

    def collides(self, other_corridor):
        if (self.mStartCol > other_corridor.mEndCol) or (other_corridor.mStartCol > self.mEndCol):
            return False
        if (self.mStartRow > other_corridor.mEndRow) or (other_corridor.mStartRow > self.mEndRow):
            return False
        return True

    def connects(self, room):
        if self.mHorizontal:
            if (self.mStartRow+1 > room.mEndRow-1) or (room.mStartRow+1 > self.mEndRow-1):
                return False
        else:
            if (self.mStartCol+1 > room.mEndCol-1) or (room.mStartCol+1 > self.mEndCol-1):
                return False


class RandomMapTemplate:
    def __init__(self, filename):
        self.mFilename = filename
        self.mTileImage = pygame.image.load(filename)
        self.mTileImage.convert()
        self.mTileImage.convert_alpha()
        self.mRoomTemplateList = []
        self.mCorridoorTemplateList = []
        self.mBaseFloorCode = 2
        self.mBaseWallCode = 1
        self.mEntranceCode = 3
        self.mExitCode = 4
        self.mTileWidth = 64
        self.mTileHeight = 64

        self.mTileImageNumX = self.mTileImage.get_width() // self.mTileWidth     # number of tiles horizontally
        self.mTileImageNumY = self.mTileImage.get_height() // self.mTileHeight     # number of tiles vertically

        self.load_template()

    def load_template(self):
        loading_rooms = True
        loading_corridors = False
        row = 1

        these_walls = []
        these_floors = []
        while (row < (self.mTileImageNumY+1)):
            col = 0
            while (col < (self.mTileImageNumX+1)):
                loading_walls = (row % 2) == 1
                loading_floors = (row % 2) == 0
                load_er_up = False
                src_x = col * self.mTileWidth  # top left corner of tile (x)
                src_y = row * self.mTileHeight  # top left corner of tile (y)

                # create surface to fill with tile image
                tile_image = pygame.Surface((self.mTileWidth, self.mTileHeight))
                tile_image.convert()
                tile_image.convert_alpha()
                tile_image.fill((0,0,0,0))

                # blit image from tileset to tile image surface
                tile_image.blit(self.mTileImage, (0, 0), (src_x, src_y, self.mTileWidth, self.mTileHeight))
                is_empty = self.is_tile_empty(tile_image)
                if not is_empty:
                    tile_code = (row * self.mTileImageNumX + col)
                    if loading_walls:
                        these_walls.append(tile_code)
                    else:
                        these_floors.append(tile_code)
                    if col == self.mTileImageNumX:
                        load_er_up = True
                else:
                    if col == 0:
                        if loading_rooms:
                            loading_rooms = False
                            loading_corridors = True
                            row+=1
                        else:
                            ValueError("Empty Row Not Expected in", self.mFilename,"at row #",row)
                    else:
                        load_er_up = True
                    col = self.mTileImageNumX + 1
                if load_er_up:
                    if loading_floors:
                        if loading_rooms:
                            self.mRoomTemplateList.append(RoomTemplate(these_floors, these_walls))
                        else:
                            self.mCorridoorTemplateList.append(CorridorTemplate(these_floors, these_walls))
                        these_floors = []
                        these_walls = []
                col += 1
            row += 1
        if len(these_walls) > 0:
            ValueError("Final Row Appears To Be Walls in", self.mFilename)

    def is_tile_empty(self, tile_surf):
        color_at_last_pixel = tile_surf.get_at((0,0))
        for y in range(tile_surf.get_height()):
            for x in range (tile_surf.get_width()):
                color_at_pixel = tile_surf.get_at((x,y))
                if (color_at_last_pixel.r != color_at_pixel.r) or (color_at_last_pixel.g != color_at_pixel.g) or (color_at_last_pixel.b != color_at_pixel.b):
                    return False
        return True

    def test_tiles(self):
        thisTileImageNumX = self.mTileImage.get_width() // self.mTileWidth
        thisTileImageNumY = self.mTileImage.get_height() // self.mTileHeight
        for row in range (thisTileImageNumX+1):
            for col in range (thisTileImageNumY+1):
                src_x = col * self.mTileWidth  # top left corner of tile (x)
                src_y = row * self.mTileHeight  # top left corner of tile (y)

                # create surface to fill with tile image
                tile_image = pygame.Surface((self.mTileWidth, self.mTileHeight))
                tile_image.convert()
                tile_image.convert_alpha()
                tile_image.fill((0,0,0,0))

                # blit image from tileset to tile image surface
                tile_image.blit(self.mTileImage, (0, 0), (src_x, src_y, self.mTileWidth, self.mTileHeight))
                is_empty = self.is_tile_empty(tile_image)


class RoomTemplate:
    def __init__(self, floor_codes_list, wall_codes_list):
        self.mFloorCodesList = floor_codes_list
        self.mWallCodesList = wall_codes_list

class CorridorTemplate:
    def __init__(self, floor_codes_list, wall_codes_list):
        self.mWallCodesList = wall_codes_list
        self.mEntryBlockCode = self.mWallCodesList.pop(0)
        self.mFloorCodesList = floor_codes_list