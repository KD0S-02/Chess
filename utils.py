from Move import Move
import colors

class Button():
    def __init__(self, x, y, image, name):
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen, p):
        screen.blit(self.image, (self.rect.x, self.rect.y))



class Utils():

    def __init__(self, p, DIMENSION, SQ_SIZE, IMAGES, player, screen):
        self.p = p
        self.DIMENSION = DIMENSION
        self.SQ_SIZE = SQ_SIZE
        self.IMAGES = IMAGES
        self.player = player
        self.screen = screen
        self.OFFSET = 25

    def drawBoard(self):
        clrs = [colors.darkGreen, colors.lightGreen]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                clr = clrs[((r+c)%2)]
                self.p.draw.rect(self.screen, clr, self.p.Rect(c*self.SQ_SIZE+self.OFFSET,
                    r*self.SQ_SIZE+self.OFFSET, self.SQ_SIZE, self.SQ_SIZE))

    def drawPieces(self, board):
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = board[r][c]
                if piece != "__":
                    self.screen.blit(self.IMAGES[piece],  self.p.Rect(c*self.SQ_SIZE+self.OFFSET,
                            r*self.SQ_SIZE+self.OFFSET, self.SQ_SIZE, self.SQ_SIZE))

    def drawGameState(self, gs, currSq, validMoves, check):
        self.drawBoard()
        if currSq != ():
            cells = gs.displayPossibleMoves(currSq[0], currSq[1], validMoves)
            self.highlight_cells(cells, gs.board, currSq, check, gs)
        self.drawPieces(gs.board)
        self.p.display.update()

    def display_rankFile(self, player):
        font = self.p.font.SysFont(None, 26)
        clrs = [colors.darkGreen, colors.lightGreen]
        ranks = []
        files = []
        for i in range(8):
            ranks.append(Move.rowToRanks[i])
            files.append(Move.colsToFiles[i])
        if player == "b":
            ranks.reverse()
            files.reverse()
        for i in range(8):
            clr = clrs[i%2]
            img = font.render(ranks[i], True, clr)
            self.screen.blit(img, (8, i*64+2*self.OFFSET))
        for i in range(8):
            clr = clrs[(i+7)%2]
            img = font.render(files[i], True, clr)
            self.screen.blit(img, (i*64+2*self.OFFSET, 522.5+self.OFFSET))


    def highlight(self, alpha, color, x, y):
        s = self.p.Surface((self.SQ_SIZE, self.SQ_SIZE))
        s.set_alpha(alpha)
        s.fill(color)
        self.screen.blit(s, (x*self.SQ_SIZE+self.OFFSET, y*self.SQ_SIZE+self.OFFSET))

    def highlightXY(self, alpha, color, x, y):
        s = self.p.Surface((self.SQ_SIZE, self.SQ_SIZE))
        s.set_alpha(alpha)
        s.fill(color)
        self.screen.blit(s, (x, y))

    def highlight_cells(self, cells, board, startSq, check, gs):
        self.drawBoard()
        for cell in cells:
            self.highlight(100, colors.green, cell[1], cell[0])
        self.highlight(100, colors.blue, startSq[1], startSq[0])
        if check == True:
            self.highlight_check(gs)

    def highlight_check(self, gs):
        if gs.playerToMove:
            ally = self.player
        else:
            ally = "b" if self.player=="w" else "w"

        Kr, Kc = gs.getKingLocation(ally)
        self.highlight(150, (255, 0, 0), Kc, Kr)

    def win(self, turn, check):
        if check:
            if turn == "w":
                text = "Black Wins!"
            else:
                text = "White Wins!"
        else:
            text = "StaleMate!"

        textColor = (0 , 0, 0)
        font = self.p.font.SysFont(None, 60)
        img = font.render(text, True, textColor)
        self.screen.blit(img, (256 , 200))
        self.p.display.update()

    def getTurnAlly(self, playerToMove):
        if playerToMove:
                ally = self.player
                turn = self.player
        else:
            ally = "b" if self.player=="w" else "w"
            turn = ally
        return turn, ally

    def GetMouseXY(self):
        location = self.p.mouse.get_pos()
        col = (location[0]-self.OFFSET)//self.SQ_SIZE
        row = (location[1]-self.OFFSET)//self.SQ_SIZE
        if row > 7 or row < 0 or col > 7 or col < 0:
            row, col = -1, -1
            return row, col
        else:
            return row, col

    def pawnPromotionMenu(self, r, c, color, IMAGES):
        x, y = c*self.SQ_SIZE+self.OFFSET, r*self.SQ_SIZE+self.OFFSET
        offset = [64, 128, 192]
        if r == 7:
            for i in range(len(offset)):
                offset[i]*=-1

        Nbutton = Button(x, y, IMAGES[color+"N"], "N")
        self.highlightXY(255, (255, 255, 255), x, y)
        Rbutton = Button(x, y+offset[0], IMAGES[color+"R"], "R")
        self.highlightXY(255, (255, 255, 255), x, y+offset[0])
        Bbutton = Button(x, y+offset[1], IMAGES[color+"B"], "B")
        self.highlightXY(255, (255, 255, 255), x, y+offset[1])
        Qbutton = Button(x, y+offset[2], IMAGES[color+"Q"], "Q")
        self.highlightXY(255, (255, 255, 255), x, y+offset[2])

        piece = color+"p"
        picking = True
        Rbutton.draw(self.screen, self.p)
        Nbutton.draw(self.screen, self.p)
        Bbutton.draw(self.screen, self.p)
        Qbutton.draw(self.screen, self.p)
        self.p.display.update()
        while picking:
            for e in self.p.event.get():
                if e.type == self.p.QUIT:
                    picking = False
                elif e.type == self.p.MOUSEBUTTONDOWN:
                    pos = self.p.mouse.get_pos()
                    if Nbutton.rect.collidepoint(pos):
                        piece = color+"N"
                        picking = False
                    elif Rbutton.rect.collidepoint(pos):
                        piece = color+"R"
                        picking = False
                    elif Bbutton.rect.collidepoint(pos):
                        piece = color+"B"
                        picking = False
                    elif Qbutton.rect.collidepoint(pos):
                        piece = color+"Q"
                        picking = False
                    else:
                        piece = color+"p"
                        picking = False
        return piece
