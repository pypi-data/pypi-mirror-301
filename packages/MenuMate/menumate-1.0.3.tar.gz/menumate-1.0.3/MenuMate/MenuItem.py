class MenuItem():
    def __init__(self, text, func, takes_input=False):
        self.text = text
        self.func = func

    def run(self):
        self.func()
        
        # if takes_input:
        #     for each param in self.func
        #         prompt for input
        #         save input

        # try/catch     
        #     call function (with input if applicable)

        # if fail to run function (wrong input type or other)
        #     run some sort of error message and ask if redo or exit
        
        #     if redo, 
        #         call run again, 
        #     else 
        #         let method end and return to menu