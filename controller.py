TEAM_CODE = 'qtksg'  # My cops. TODO: clear before distributing.
TIME_BETWEEN_MOVES = 0.5  # seconds. Minimum of 0.3 seconds

# DIRECTIONS
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
STAY = 'stay'


# Helper function
def get_column_row(coordinate):
    col, row = map(int, coordinate.split(':'))
    return (col, row)


class Controller:
    # Game functions
    def on_game_start(self, maze, num_cols, num_rows):
        '''
        This functions is called at the start of the game. It's not very useful.
        Don't feel obliged to use it.
        '''
        self.maze = maze
        print("Rows: ", num_rows)
        print("Columns: ", num_cols)

    def move_cop(cop, rob):
        if cop[0] < rob[0]:
            return RIGHT
        elif cop[0] > rob[0]:
            return LEFT
        elif cop[1] > rob[1]:
            return UP
        elif cop[1] < rob[1]:
            return DOWN

    #add node's kids to queue
    def add_children_to_q(node, queue):
        if node.get_up() is not None:
            queue.append(node.get_up())
        elif node.get_right() is not None:
            queue.append(node.get_right())
        elif node.get_left() is not None:
            queue.append(node.get_left())
        elif node.get_down() is not None:
            queue.append(node.get_down())

    def add_to_q_and_dict(parent, robber, queue, graphdict):
        #add cop's children to queue
        #FIXME: check if found robber!

        if parent.get_up() is not None:
            if parent.get_up() == robber:
                return True
            graphdict[parent.get_up()] = parent
            add_children_to_q(parent.get_up(), queue)

        elif parent.get_right() is not None:
            if parent.get_up() == robber:
                return True
            graphdict[parent.get_right()] = parent
            add_children_to_q(parent.get_up(), queue)

        elif parent.get_left() is not None:
            if parent.get_up() == robber:
                return True
            graphdict[parent.get_left()] = parent
            add_children_to_q(parent.get_up(), queue)

        elif parent.get_down() is not None:
            if parent.get_up() == robber:
                return True
            graphdict[parent.get_down()] = parent
            add_children_to_q(parent.get_up(), queue)


    def find_valid_path(cop, rob):
        copcol, coprow = get_column_row(cop)
        robcol, robrow = get_column_row(rob)
        queue = []
        graphdict = {}

        copnode = maze[copcol][coprow] #get cop's node from maze
        robnode = maze[robcol][robrow]

        current = -1 #copnode
        found = add_to_q_and_dict(copnode, robnode, queue, graphdict)
        while not found:


        if current == -1:




    def on_my_turn(self, maze, player_coordinates, banks):
        '''
        This function is called every time that it is your turn to move your players.
        Using the location of your players, your opponents (both stored in player_coordinates
        dictionary), and the banks (stored in banks), determine each players next move.

        Params:
            maze: [][] -> Node: A two-dimensional list of Nodes.
                See the spec for the Node class at the bottom of this file.

            player_coordinates: { 'ROBBERS': a list of coordinates, 'COPS': a list of coordinates }
                where a coordinate is a string "col:row", e.g. "21:23"

            banks: [] -> a list of coordinates of banks.
                where a coordinate is a string "col:row", e.g. "21:23"
        Return:
            moves: { 'ROBBERS': [A list of directions or None]}
        '''

        # import pdb; pdb.set_trace()  # Uncomment this line to enabe the debugger.

        cops = player_coordinates['COPS']
        robbers = player_coordinates['ROBBERS']
        valid_robs = robbers
        move_list = [None] * len(cops)
        for i in range(len(robbers)):
            if robbers[i] is None:
                del valid_robs[i]
                continue
            col1, row1 = get_column_row(robbers[i])
            robber_node = maze[col1][row1]

        for i in range(len(cops)):
            if cops[i] is None:
                continue  # we skip players that are no longer in the game.
            col, row = get_column_row(cops[i])
            player_node = maze[col][row]

            # Take the first available direction. Don't do this!!!!
            # if player_node.get_up() is not None:
            #     move_list[i] = UP
            # elif player_node.get_right() is not None:
            #     move_list[i] = RIGHT
            # elif player_node.get_left() is not None:
            #     move_list[i] = LEFT
            # elif player_node.get_down() is not None:
            #     move_list[i] = DOWN
            # else:
            #     move_list[i] = STAY



        moves = {
            'COPS': move_list,
        }

        return moves


'''
class Node:

    def __init__(self, col, row):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.col = col
        self.row = row

    def get_up(self):
        return self.up  # Node or None if path is blocked.

    def get_down(self):
        return self.down  # Node or None

    def get_left(self):
        return self.left  # Node or None

    def get_right(self):
        return self.right  # Node or None

    def coordinates(self):
        return str(self.col) + ':' + str(self.row)  # "col:row"

    def __str__(self):
        return "Node(" + str(self.col) + ":" + str(self.row) + "): (\{\}\{\}\{\}\{\})".format(
            'U' if self.up else "",
            'D' if self.down else "",
            'L' if self.left else "",
            "R" if self.right else "")
'''
