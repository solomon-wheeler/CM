class node():
    def __init__(self, m_wrong, c_wrong, boat_wrong, parent):
        self.state = [m_wrong, c_wrong, boat_wrong]
        self.parent = parent

    def is_goal_state(self):
        if sum(self.state) == 0:
            return True
        else:
            return False

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def get_child_node(self, action, parent):
        new_state = [self.state[0] - action[0], self.state[1] - action[1], self.state[2] - action[2]]
        other_side = [3 - new_state[0], 3 - new_state[1]]
        print(other_side)
        # checking if vaild, saves spaces from creating then calling is valid function
        if new_state[0] < new_state[1]:
            if new_state[0] != 0:
                return False
        if other_side[0] < other_side[1]:
            if other_side[0] != 0:
                return False
        if new_state[0] < 0 or new_state[1] < 0 or new_state[2] < 0:
            return False
        if new_state[0] > 3 or new_state[1] > 3 or new_state[2] > 3:
            return False

        return node(self.state[0] - action[0], self.state[1] - action[1], self.state[2] - action[2],
                    parent)  # don't need else here because this will only run of no false has been returned

    # def is_valid_state(self): #not sure if i need this
    #   if self.state[0] < self.state[1]:
    #      return True
    # if self.state[0] or self.state[1] or self.state[]
    # else:
    #   return False


class game():
    def __init__(self):
        self.initial_node = node(3, 3, 1, None)
        self.frontier = []
        self.explored = []
        self.possible_moves_boat = [[1, 0, 1], [2, 0, 1], [0, 1, 1], [0, 2, 1], [1, 1, 1]]
        self.possible_moves_no_boat = [[-1, 0, -1], [-2, 0, -1], [0, -1, -1], [0, -2, -1], [-1, -1, -1]]

    # def add_children(self):
    #   for this_try in possible_moves:
    #      self.current_state.get_child_node()
    def breadth_first_search(
            self):  # pseudo from Rusell and Norvig Artificial Intelligence: A modern approach 4th ed p.82
        self.current_state = self.initial_node

        while self.current_state.is_goal_state() == False:  # creating_children for node
            self.explored.append(self.current_state)
            # print(str(self.current_state.get_state()[2]) + "h")
            # boat = 0
            state = self.current_state.get_state()
            if state[2] == 1:
                moves_to_try = self.possible_moves_boat
            else:
                moves_to_try = self.possible_moves_no_boat
            # else:
            #   boat = 0
            for this_try in moves_to_try:

                # print(this_try)
                returned_child = self.current_state.get_child_node(this_try, self.current_state)
                if returned_child != False:
                    already_found = False
                    for x in self.frontier:
                        if x.get_state() == returned_child.get_state():
                            already_found = True
                    for x in self.explored:
                        if x.get_state() == returned_child.get_state():
                            already_found = True
                    if already_found == False:
                        self.frontier.append(returned_child)
                        print(str(returned_child.state))
            print(self.frontier)
            if len(self.frontier) == 0:
                return "not found"
            self.current_state = self.frontier.pop(0)

        return self.current_state


##main##
overall_game = game()
result = overall_game.breadth_first_search()
if result == "not found":
    print("no result found!")
else:
    print("found result" + str(result.get_state()))
    parent = result.get_parent()
    while parent != None:
        print(parent.get_state())
        parent = parent.get_parent()
