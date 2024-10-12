from MenuMate import MenuItem, Menu

class MenuManager():
    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.menu_stack = [main_menu]

    def run(self):
        while self.menu_stack != []:
            cur_menu = self.menu_stack.pop()
            
            prev_menu = ""
            if self.menu_stack != []:
                prev_menu = self.menu_stack[-1]
            action = cur_menu.run(prev_menu)
            
            if action != cur_menu.quit_char:
                if action != cur_menu.back_char:
                    self.menu_stack.append(cur_menu)
                    if isinstance(action.func, Menu):
                        self.menu_stack.append(action.func)
                    else:
                        action.run()
