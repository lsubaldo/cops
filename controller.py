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

    ''' Walk through the queue and pass in (Node parent) to find
    specific (Node robber). If we find the robber, return (Node robber)
    to walk back up graphdict. Otherwise, add children to (List queue)
    and (dictionary graphdict)
    '''
    def add_to_q_and_dict(parent, robber, queue, graphdict):
        if parent.get_up() is not None:
            graphdict[parent.get_up()] = parent
            if parent.get_up() == robber:
                return parent.get_up()
            add_children_to_q(parent.get_up(), queue)

        elif parent.get_right() is not None:
            graphdict[parent.get_right()] = parent
            if parent.get_right() == robber:
                return parent.get_right()
            add_children_to_q(parent.get_right(), queue)

        elif parent.get_left() is not None:
            graphdict[parent.get_left()] = parent
            if parent.get_left() == robber:
                return parent.get_left()
            add_children_to_q(parent.get_left(), queue)

        elif parent.get_down() is not None:
            graphdict[parent.get_down()] = parent
            if parent.get_down() == robber:
                return parent.get_down()
            add_children_to_q(parent.get_down(), queue)

        else: return None

    def get_direction(parent, child):
        if parent.get_up() == child:
            return UP
        if parent.get_right() == child:
            return RIGHT
        if parent.get_left() == child:
            return LEFT
        if parent.get_down() == child:
            return DOWN

    ''' (str, str) -> str
    Finds the shortest valid path to a specific robber via a breadth-first
    search. Returns the direction the cop should move.
    '''
    def find_valid_path(cop, rob):
        copcol, coprow = get_column_row(cop) #pull coordinates (int) out of string
        robcol, robrow = get_column_row(rob)
        copnode = maze[copcol][coprow] #get nodes from maze
        robnode = maze[robcol][robrow]

        queue = []
        graphdict = {}

        # loop through queue until find robber; robber will be entered into
        # graphdict
        robkey = add_to_q_and_dict(copnode, robnode, queue, graphdict)
        qidx = 0;
        while robkey is None:
            suspect = queue[qidx]
            robkey = add_to_q_and_dict(suspect, robnode, queue, graphdict)
            qidx += 1

        #loop through dictionary to find the direction cop should go
        temp = robkey
        while graphdict[temp] is not copnode:
            temp = graphdict[temp]

        direction = get_direction(graphdict[temp], temp)
        return direction

    #TODO: write a function that matches a cop to the closest robber with simple coordinate geometry

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

        # import pdb; pdb.set_trace()  # Uncomment this line to enable the debugger.

        cops = player_coordinates['COPS']
        robbers = player_coordinates['ROBBERS']
        valid_robs = robbers
        move_list = [None] * len(cops)

        '''
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
            copnode = maze[col][row]
        '''
        for i in range(len(cops)):
            move_list[i] = find_valid_path(cops[i], robbers[i])


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
