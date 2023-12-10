class Tile:
    def __init__(self, type, value):
        self.type = type
        '''
        Type is an integer.
        - -2 for obstacle cell
        - -1 for door cell
        - 0 for starting empty tile
        - 1 for other empty tiles
        - 2 for key cell
        - 3 for finish cell (Mr. Thanh)
        - 4 for empty up/down stairs
        '''
        self.value = value
        '''
        Value is only relevant if the cell is a key, a door or stairs.
        Each key cell, door cell and stairs cell has an integer value attached to it.
        The agent can only walk through the door with a value
        if it has the key of the same value.
        Value is set to 0 for all other spaces except keys and doors.
        
        Up stairs have a value of 1.
        Down stairs have a value of -1.
        '''