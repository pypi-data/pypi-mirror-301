# MenuMate
Tired of spending way too much time setting up terminal menu's instead of just getting into making the code? Well I was, so I took all my old code used for making menu's in my college courses and made this python library. 


Feel free to check out the [Github Repo](https://github.com/bethChris/MenuMate) for a better documentation experience until I can get ReadTheDocs setup!

# Table O' Contents
- [Installation](#installation)
- [Feature Summary](#feature-summary)
- [How to Use](#how-to-use)
  - [Creating a Menu](#creating-a-menu)
  - [Creating a Menu Item](#creating-a-menu-item)
  - [Adding a Menu Item](#adding-a-menu-item)
  - [Running a Menu](#running-a-menu)
- [Example Code](#but-do-you-have-an-example-i-can-just-copy)
- [Advanced Functionality](#advanced-funtionality-for-those-that-read-this-far)
  - [Chaining Menus](#chaining-menus)



# Installation
Assuming you have Python 3.x+ you should be able to install using pip:

```bash
$ pip install MenuMate
```

# Feature Summary
This first version is all pretty standard menu functionality, but I do have plans to add more in the future!

- **Modular Design**: 2 modular classes and 1 driver class can be pieced together to build menus that fit your needs. 
- **Input Validation**: Simple input validation ensures the user cannot select a non-existant menu option.
- **Clean Layout**: We love it when everything is centered and justified dynamically.
- **Chaining Menus**: Allows you to pass another Menu object as an option for a different Menu object. 
- **Back Button**: Built in option on all menus that will allow users to go back to the previous menu.


# How to Use
## Creating a Menu
To create a menu you need to create a Menu object. This object starts out super simple but will eventually hold all of our menu options called MenuItems. You can instantiate a Menu object and pass in an optional custom title.

```python
plain_generic_menu = Menu() # default title is "Menu"
fancy_menu = Menu(title="The Fanciest of Menus Menu")
```

## Creating a Menu Item
A menu isn't much help without something to select. To create a menu item you create a MenuItem object. This object is comprised of two parts:

- **Text**: the flavor text you'd like to list on the menu for that option 
- **Function**: the runnable function associated with your option. 

>**NOTE**: Currently, runnable functions have to be paramater-less (or have all defaults set) in order to work. MenuItems that can take input will ideally be a later feature.

```python
option_1 = MenuItem(text="Golly, Pick Me!", func=my_cool_func)
```

Menu's are runnable! So you can create [**Chaining Menus**](#chaining-menus) by creating a MenuItem that has a Menu object as the function and then [adding that MenuItem](#adding-a-menu-item)

```python
second_menu = Menu(title="Second Menu")
menu_option = MenuItem(text="To The Second Menu, Please!", func=second_menu)
```

## Adding a Menu Item
To add an item to a Menu, you simply call the Menu's `add()` method and pass in a MenuItem object

```python
main_menu.add(menu_item=option_1)
# or
main_menu.add(menu_item=MenuItem("Click Me!", my_cool_func))
```

## Running a Menu
Running this whole thing requires creating a MenuManager object and passing it your "main menu". A "main menu" is the first menu you'd like your users to see. 
(To learn how to link many Menus together visit the [Chaining Menus](#chaining-menus) section)

Then you can call the MenuManager's `run()` method to begin running your Menu setup.

```python 
# pass in your first menu 
menu_manager = MenuManager(main_menu=my_first_menu)

# run
menu_manager.run()
```

# But Do You Have an Example I Can Just Copy?
Great question. Here's a simple working example of what this library can do:

```python
from MenuMate import MenuItem, Menu, MenuManager

### CUSTOM FUNCTIONS ###
# You write these #
def ask_whats_up():
    print("What's up? How was your day?")

def hello_world(): 
    print("Hello World!")

### TURNING YOUR FUNCTIONS INTO MENU ITEMS ###
option_1 = MenuItem(text="Ask Me What's Up", func=ask_whats_up)
option_2 = MenuItem(text="Say Hello", func=hello_world)

### SETTING UP A MENU OBJECT ###
main_menu = Menu(title="Main Menu")

### ADDING MENU ITEMS INTO A MENU ###
main_menu.add(menu_item=option_1)
main_menu.add(menu_item=option_2)

### SETTING UP A MENU MANAGER OBJECT ###
# pass your main menu into the menu manager #
menu_manager = MenuManager(main_menu=main_menu)

### RUN MENU MANAGER ###
menu_manager.run() 
```
Which will produce this output:

![Screenshot of code output in the terminal. Displays a menu with 2 options and a quit option. ](https://github.com/bethChris/MenuMate/blob/main/images/MenuMateEx1.jpg?raw=true)


# Advanced Funtionality For Those That Read This Far:
Welcome. At this point there is not much "advanced" functionality but this is a spot for pieces of functionality I feel need a bit more explanation.

## Chaining Menus
This was something I needed a lot for projects where I needed some menu items to lead to different menus with more options for customizing how the code would be ran. Whatever *your* use case is, this is a breakdown of how that works.

### Adding a Menu
As described in the [Creating a Menu Item](#creating-a-menu-item) section, adding a Menu as an option to a different Menu is as simple as creating a MenuItem object that contains a Menu object as the function, then adding the MenuItem like normal to the different Menu.

A couple limitations exist with this functionality:
1. Menu's cannot have a MenuItem that leads to a prior Menu. 
> **Ex**: If Menu A goes to Menu B then Menu B cannot have an option that leads to Menu A again. 

2. Menu's cannot have a MenuItem that leads back to itself. 
> **Ex**: Menu A cannot have an option that goes to Menu A

Both of these limitations exist to ensure the back button feature works properly. This still allows for many Menu's to lead to the same Menu, just not for that end Menu to include an option to go to any Menu that points to it.

>**Ex**: Menu A, Menu B, and Menu C all have an option to go to Menu D, but Menu D cannot have any option that leads to Menu A, Menu B or Menu C.

### The One Where You Just Copy and Paste
Here is another annotated code example. This one shows how to turn a Menu into a MenuItem and what the output might look like.

```python
from MenuMate import MenuItem, Menu, MenuManager

### CUSTOM FUNCTIONS ###
# You write these #
def a_simple_lad():
    print("Salt is spicy")
    
def peak_musical_genius():
    print("Ring-ding-ding-ding-dingeringeding!")

### SETTING UP MENU OBJECTS ###
main_menu = Menu(title="Main Menu")
second_menu = Menu(title="Nifty Second Menu")

### TURNING YOUR FUNCTIONS INTO MENU ITEMS ###
option_1 = MenuItem(text="Hot Take", func=a_simple_lad)
option_2 = MenuItem(text="What Does the Fox Say?", func=peak_musical_genius)

### ADDING MENU ITEMS INTO THE MENUS ###
main_menu.add(menu_item=option_1)
second_menu.add(menu_item=option_2)

### TURNING A MENU INTO A MENU ITEM ###
# the ~advanced~ part of this example #
second_menu_option = MenuItem(text="Show Me The Second Menu", func=second_menu)

### ADDING ANOTHER MENU ITEM TO MAIN_MENU ###
main_menu.add(menu_item=second_menu_option)

### SETTING UP A MENU MANAGER OBJECT ###
# pass your main menu into the menu manager #
menu_manager = MenuManager(main_menu=main_menu)

### RUN MENU MANAGER ###
menu_manager.run()
```
This produces the output:

![Screenshot of code output in the terminal. Displays a menu with an option to visit another menu. ](https://github.com/bethChris/MenuMate/blob/main/images/MenuMateEx2.jpg?raw=true)

