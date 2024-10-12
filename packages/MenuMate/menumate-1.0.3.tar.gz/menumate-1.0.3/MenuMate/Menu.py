from MenuMate import MenuItem

class Menu():
    def __init__(self, title="Menu"):
        self.menu_items = []
        self.previous_menu_stack = []
        self.title = title
        self.quit_char = 'q'
        self.back_char = 'b'
    
    def add(self, menu_item):
        # TODO: is there a more elegant way to do this?
        if not isinstance(menu_item, MenuItem):
            raise TypeError(f"Expected 'MenuItem', got '{type(menu_item).__name__}'")
        
        if isinstance(menu_item.func, Menu):
            # will check to see if any previous menus are pointing to it already 
            # TODO: define what behavior is/isn't allowed
            #   not allowed to loop to previous menu or itself

            if menu_item.func in self.previous_menu_stack or menu_item.func == self:
                raise ValueError("Menu cannot point to a previous menu or itself!")
            else:
                menu_item.func.previous_menu_stack.append(self)
            
        self.menu_items.append(menu_item)


    def display(self, descrs, options):
        longest_descr = max(len(max(descrs, key=len)), len(self.title))
        longest_opt = len(max(options, key=len)) + 3
        print()
        print(f"{self.title:^{longest_descr+longest_opt}}")

        print("-"*(longest_descr+longest_opt))
        for opt, descr in zip(options, descrs):
            print(f"[{opt}] {descr}")
        print("-"*(longest_descr+longest_opt))
        print()

    def run(self, prev=""):
        descrs = [m.text for m in self.menu_items]
        options = [str(i+1) for i in range(len(self.menu_items))]

        if prev != "":
            descrs.append("Back to " + prev.title)
            options.append(self.back_char)

        descrs.append("Quit")
        options.append(self.quit_char)

        self.display(descrs, options)

        user_selection = input("Select option: ")
        while user_selection not in options:
            user_selection = input("Select option: ")
    
        if user_selection != self.quit_char and user_selection != self.back_char:
            return self.menu_items[int(user_selection)-1]
        else:
            return user_selection

    def run_option(self, option):
        actions = {i:item.func for i,item in enumerate(self.menu_items)}
        actions[option].run()

    def __call__(self):
        self.run()
