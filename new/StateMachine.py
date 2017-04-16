from string import upper

class StateMachine:
    def __init__(self):
        self.handlers = {} # state machnie action map(key-value) , key is state name, value is function
        self.startState = None # start state, start function
        self.endStates = []  # end state list , This list is string list , save state name
        self.currentState = None

    def add(self, name, handler, end_state=0):
        name = upper(name)  # we use upper letter
        self.handlers[name] = handler # add into action list
        if end_state:
            self.endStates.append(name)

    def setStart(self, name):
        self.startState = upper(name)  # set which state should begging
        self.currentState = self.startState

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState] # first, use start state to get the start function
        except:
            raise "InitializationError", "must call setStart() before run()"

        if not self.endStates:
            raise "InitializationError", "at least one state must be an end state"

        while True:
            (newState, cargo) = handler(cargo) # cargo is argument list
            if upper(newState) in self.endStates: # check it is end state
                break
            else:
                handler = self.handlers[upper(newState)]

    # def Step(self, cargo):
    #     if upper(self.currentState) in self.endStates:
    #         return
    #     else:
    #         handler = self.handlers[self.currentState]
    #         (newState, cargo) = handler(cargo)
    #         self.currentState = newState

    def update(self, cargo):
        handler = self.handlers[self.currentState]
        (newState, cargo) = handler(cargo)
        self.currentState = newState

if __name__ == "__main__":

    def one(*agrv):
        print "1"
        return ("2", ())

    def two(*agrv):
        print "2"
        return ("4", ())

    def third(*agrv):
        print "3"
        return ("2", ())

    def four(*agrv):
        print "4"
        return ("5", ())

    def five(*agrv):
        print "5"
        return ("5", ())

    m = StateMachine()
    m.add("1", one)
    m.add("2", two)
    m.add("3", third)
    m.add("4", four)
    m.add("5", five, end_state=1)
    m.setStart("1")
    m.run(())

    # def ones_counter(val):
    #     print "ONES State: "
    #     while True:
    #         if val <= 0 or val >= 30:
    #             newState = "Out_of_Range"
    #             break
    #         elif 20<= val < 30:
    #             newState = "TWENTIES"
    #             break
    #         elif 10<= val < 20:
    #             newState = "TENS"
    #             break
    #         else:
    #             print " @ %2.1f+" % val
    #         val = math_func(val)
    #     print " >>"
    #     return (newState, val)
    #
    #
    # def tens_counter(val):
    #     print "TEHS State: "
    #     while True:
    #         if val <= 0 or val >= 30:
    #             newState = "Out_of_Range"
    #             break
    #         elif 1<= val < 10:
    #             newState = "ONES"
    #             break
    #         elif 20<= val < 30:
    #             newState = "TWENTIES"
    #             break
    #         else:
    #             print " @ %2.1f+" % val
    #         val = math_func(val)
    #     print " >>"
    #     return (newState, val)
    #
    # def twenties_counter(val):
    #     print "TWENTIES State: "
    #     while True:
    #         if val <= 0 or val >= 30:
    #             newState = "Out_of_Range"
    #             break
    #         elif 1<= val < 10:
    #             newState = "ONES"
    #             break
    #         elif 10<= val < 20:
    #             newState = "TENS"
    #             break
    #         else:
    #             print " @ %2.1f+" % val
    #     val = math_func(val)
    #     print " >>"
    #     return (newState, val)
    #
    # def math_func(n):
    #     from math import sin
    #     return abs(sin(n))*31
    #
    # m = StateMachine() # new a state machine, m is a class object
    # m.add("ONES", ones_counter)
    # m.add("TENS", tens_counter)
    # m.add("TWENTIES", twenties_counter)
    # m.add("OUT_OF_RANGE", None, end_state=1)
    # m.setStart("ONES")
    # m.run(1)

