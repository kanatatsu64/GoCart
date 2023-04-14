import tkinter as tk

FIELD_WIDTH = 7
FIELD_HEIGHT = 7
BLOCK_SIZE = 40

class Cord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_values(self):
        return (self.x, self.y)

    def to_str(self):
        return f"({self.x}, {self.y})"

    @staticmethod
    def add(a, b):
        return Cord(a.x+b.x, a.y+b.y)

    @staticmethod
    def eq(a, b):
        return ((a.x == b.x) and (a.y == b.y))

# direction = up | down | left | right
class Cart():
    def __init__(self, cord, direction):
        self.cord = cord
        self.direction = direction

    def next(self):
        if self.direction == "up":
            return Cord.add(self.cord, Cord(0, -1))
        elif self.direction == "down":
            return Cord.add(self.cord, Cord(0, 1))
        elif self.direction == "left":
            return Cord.add(self.cord, Cord(-1, 0))
        elif self.direction == "right":
            return Cord.add(self.cord, Cord(1, 0))

    def turnL(self):
        if self.direction == "up":
            self.direction = "left"
        elif self.direction == "down":
            self.direction = "right"
        elif self.direction == "left":
            self.direction = "down"
        elif self.direction == "right":
            self.direction = "up"

    def turnR(self):
        if self.direction == "up":
            self.direction = "right"
        elif self.direction == "down":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "up"
        elif self.direction == "right":
            self.direction = "down"

class Block():
    def __init__(self, cords):
        self.cords = cords

    def hit(self, cord):
        for block_cord in self.cords:
            if Cord.eq(cord, block_cord):
                return True
        else:
            return False

class Goal():
    def __init__(self, cord):
        self.cord = cord

    def fin(self, cord):
        return Cord.eq(cord, self.cord)

# kind = field | block | goal | cart
class Square():
    def __init__(self, cord, kind, param=None):
        self.cord = cord
        self.kind = kind
        self.param = param
        self.shape_id = None

    def get_color(self):
        if self.kind == "field":
            return "gray"
        elif self.kind == "block":
            return "black"
        elif self.kind == "goal":
            return "red"
        elif self.kind == "cart":
            return "green"

    def draw(self, shape_id):
        self.shape_id = shape_id

    def drawn(self):
        return not (self.shape_id is None)

    @staticmethod
    def eq(a, b):
        cord_eq = Cord.eq(a.cord, b.cord)
        kind_eq = a.kind == b.kind
        if a.param is None:
            if b.param is None:
                param_eq = True
            else:
                param_eq = False
        else:
            if b.param is None:
                param_eq = False
            else:
                param_eq = a.param == b.param
        return cord_eq and kind_eq and param_eq

class Grid():
    def __init__(self, squares=[]):
        self.squares = squares

    def exists(self, cord):
        for square in self.squares:
            if Cord.eq(square.cord, cord):
                return True
        else:
            return False

    def upsert(self, cord, kind, param=None):
        for square in self.squares:
            if Cord.eq(square.cord, cord):
                square.kind = kind
                square.param = param
                break
        else:
            self.squares.append(Square(cord, kind, param))

    def get(self, cord):
        for square in self.squares:
            if Cord.eq(square.cord, cord):
                return square
        else:
            return None

class Field():
    def __init__(self, goal, block, width, height):
        self.width = width
        self.height = height
        self.cart = Cart(Cord(0, 0), "right")
        self.goal = goal
        self.block = block

        self.cords = [Cord(x, y)
                        for x in range(self.width)
                        for y in range(self.height)]

    def validate(self):
        if not self.inside(self.cart.cord):
            raise "cart must be inside of the field"

        if self.block.hit(self.cart.cord):
            raise "cart must not be inside of the block"

        if not self.inside(self.goal.cord):
            raise "goal must be inside of the field"

        if self.block.hit(self.goal.cord):
            raise "goal must not be inside of the block"

        for block_cord in self.block.cords:
            if not self.inside(block_cord):
                raise "block must be inside of the field"

    def inside(self, cord):
        for field_cord in self.cords:
            if Cord.eq(cord, field_cord):
                return True
        else:
            return False

    def movable(self):
        cart_cord = self.cart.next()

        if not self.inside(cart_cord):
            return False

        if self.block.hit(cart_cord):
            return False

        return True

    def move(self):
        if not self.movable():
            raise "Invalid move operation"

        self.cart.cord = self.cart.next()

    def fin(self):
        return self.goal.fin(self.cart.cord)

    def get_grid(self):
        self.validate()

        grid = Grid([Square(field_cord, "field")
                        for field_cord in self.cords])
        for block_cord in self.block.cords:
            grid.upsert(block_cord, "block")
        grid.upsert(self.goal.cord, "goal")
        grid.upsert(self.cart.cord, "cart", self.cart.direction)

        return grid

class Canvas(tk.Canvas):
    def __init__(self, master, field):
        self.width = field.width * BLOCK_SIZE
        self.height = field.height * BLOCK_SIZE

        super().__init__(master, width=self.width, height=self.height, bg="white")

        self.place(x=25, y=25)

        self.before_grid = Grid()

    def render_grid(self, grid):
        for square in grid.squares:
            before = self.before_grid.get(square.cord)
            if (not (before is None)) and Square.eq(square, before):
                square.draw(before.shape_id)
                continue

            x = square.cord.x
            y = square.cord.y

            x1 = x * BLOCK_SIZE
            x2 = (x+1) * BLOCK_SIZE
            y1 = y * BLOCK_SIZE
            y2 = (y+1) * BLOCK_SIZE

            if square.kind == "cart":
                if square.param == "up":
                    shape_id = self.create_polygon(
                                (x1+x2)/2, y1, x1, y2, x2, y2,
                                outline="white", width=1,
                                fill=square.get_color())
                elif square.param == "down":
                    shape_id = self.create_polygon(
                                x1, y1, x2, y1, (x1+x2)/2, y2,
                                outline="white", width=1,
                                fill=square.get_color())
                elif square.param == "left":
                    shape_id = self.create_polygon(
                                x1, (y1+y2)/2, x2, y1, x2, y2,
                                outline="white", width=1,
                                fill=square.get_color())
                elif square.param == "right":
                    shape_id = self.create_polygon(
                                x1, y1, x2, (y1+y2)/2, x1, y2,
                                outline="white", width=1,
                                fill=square.get_color())
            else:
                shape_id = self.create_rectangle(
                            x1, y1, x2, y2,
                            outline="white", width=1,
                            fill=square.get_color())

            square.draw(shape_id)

            if (not (before is None)) and before.drawn():
                self.delete(before.shape_id)

        self.before_grid = grid

    def render_fin(self):
        before = self.before_grid
        if not (before is None):
            for square in before.squares:
                if square.drawn():
                    self.delete(square.shape_id)
        
        x1 = self.width / 2
        y1 = self.height / 2
        self.create_text(x1, y1, text="Congratulations!!")

class Game():
    def __init__(self, master, field, policy):
        self.field = field
        self.canvas = Canvas(master, field)
        self.master = master
        self.policy = policy
        self.prev = None

        self.field.validate()

    def render(self):
        self.canvas.render_grid(self.field.get_grid())

    def loop(self):
        if self.field.fin():
            self.fin()
            return

        self.prev = self.policy(
                        self.field.cart.turnL, 
                        self.field.cart.turnR,
                        self.field.movable,
                        self.prev)

        if self.field.movable():
            self.field.move()
        self.render()
        self.master.after(300, self.loop)
    
    def fin(self):
        self.canvas.render_fin()

def main(field, policy):
    app = tk.Tk()
    app.geometry("500x500")
    app.title("Go!! Cart")

    game = Game(app, field, policy)
    game.render()

    app.after(1000, game.loop)

    app.mainloop()

def nop_policy(turnL, turnR, movable, prev):
    pass

if __name__ == "__main__":
    block = Block([])
    goal = Goal(Cord(FIELD_WIDTH-1, FIELD_HEIGHT-1))
    field = Field(goal, block, FIELD_WIDTH, FIELD_HEIGHT)
    main(block, nop_policy)
