# prev: counter
def counter_policy(turnL, turnR, movable, prev):
    # first call
    if prev is None:
        prev = 0

    print(prev)
    return prev+1

def turnR_policy(turnL, turnR, movable, prev):
    if not movable():
        turnR()

def zigzag_policy(turnL, turnR, movable, prev):
    if prev is None:
        prev = 0
    
    if prev % 2 == 0:
        turnR()
    else:
        turnL()
    
    return prev+1

def leftmost_policy(turnL, turnR, movable, prev):
    turnL()
    if movable():
        return

    turnR()
    if movable():
        return

    turnR()
    if movable():
        return

    # go back
    turnR()
