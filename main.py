class node:
    def __init__(self, m_wrong, c_wrong, boat_wrong, parent, action):
        self.state = [m_wrong, c_wrong, boat_wrong]
        self.this_parent = parent
        self.this_action = action

    def is_goal_state(self):
        if sum(self.state) == 0:
            return True
        else:
            return False

    def get_action_in_words(self):
        overall_explanation = ""
        if self.this_action[0] != 0:
            overall_explanation = overall_explanation + "Moved " + str(abs(self.this_action[0])) + " missionaries" #abs is making the value always positive, i.e taking modulus
        if self.this_action[1] != 0:
            if len(overall_explanation) > 1:
                overall_explanation = overall_explanation + " and "
            overall_explanation = overall_explanation + "moved " + str(abs(self.this_action[1])) + " cannibals" #abs is making the value always positive, i.e taking modulus
        if self.this_action[2] ==1:
            overall_explanation = overall_explanation + " from the wrong side to the right side"
        elif self.this_action[2] == -1:
            overall_explanation = overall_explanation + " from the right side to the wrong side"
        return overall_explanation

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.this_parent

    def get_child_node(self, action, parent):
        new_state = [self.state[0] - action[0], self.state[1] - action[1], self.state[2] - action[2]]
        other_side = [3 - new_state[0], 3 - new_state[1]]
        #print(other_side)
        # checking if valid *before* creating saves memory in comparison to creating then running an isValid() function
        if new_state[0] < new_state[1]:  # checking if more cannibals than missionaries on wrong side
            if new_state[0] != 0:
                return False
        if other_side[0] < other_side[1]:  # checking if more cannibales than missionaries on correct side
            if other_side[0] != 0:
                return False
        if new_state[0] < 0 or new_state[1] < 0 or new_state[
            2] < 0:  # checking if we have enough canibals/missionaries on the side to make the move. Boat check should never run, but is useful to catch bugs
            return False
        if new_state[0] > 3 or new_state[1] > 3 or new_state[2] > 3:  # ^ on other side
            return False

        return node(self.state[0] - action[0], self.state[1] - action[1], self.state[2] - action[2],
                    parent,action)  # don't need else here because this will only run of no false has been returned


class game:
    def __init__(self):
        self.initial_node = node(3, 3, 1, None, [0,0,0])
        self.frontier = []
        self.explored = []
        self.possible_moves_boat = [[1, 0, 1], [2, 0, 1], [0, 1, 1], [0, 2, 1], [1, 1, 1]]
        self.possible_moves_no_boat = [[-1, 0, -1], [-2, 0, -1], [0, -1, -1], [0, -2, -1], [-1, -1, -1]]
        self.current_state = self.initial_node

    def breadth_first_search(
            self):  # pseudo from Rusell and Norvig Artificial Intelligence: A modern approach 4th ed p.82

        while self.current_state.is_goal_state() == False:  # creating_children for node
            self.explored.append(self.current_state)
            state = self.current_state.get_state()
            if state[2] == 1:  # checking which side the boat is on, as this dictates how we need to change the state
                moves_to_try = self.possible_moves_boat
            else:
                moves_to_try = self.possible_moves_no_boat
            for this_try in moves_to_try:  # going through all of the possible moves
                returned_child = self.current_state.get_child_node(this_try, self.current_state)
                if returned_child != False:
                    already_found = False
                    for x in self.frontier:  # checking if this state is already in the frontier
                        if x.get_state() == returned_child.get_state():
                            already_found = True
                    for x in self.explored:  # checking if this state has already been explored
                        if x.get_state() == returned_child.get_state():
                            already_found = True
                    if already_found == False:
                        self.frontier.append(returned_child)
            if len(self.frontier) == 0:  # nothing in frontier means we have nothing left to explore, so we have finished our search
                return "not found"
            self.current_state = self.frontier.pop(0)  # breadth first uses a FIFO data structure, emulated here.

        return self.current_state


##main##

overall_game = game()
result = overall_game.breadth_first_search()

if result == "not found":
    print("no result found!")
else:
    print("found result" + str(result.get_state()))
    parent = result.get_parent()
    while parent != None:  # going through all parent's to show moves
        print(parent.get_state())
        print(parent.get_action_in_words())
        parent = parent.get_parent()
