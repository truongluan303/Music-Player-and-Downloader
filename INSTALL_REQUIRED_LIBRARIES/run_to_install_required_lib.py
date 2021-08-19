#!/usr/bin/python
# Author: Hoang Truong

##############################################################################
###  a script to automatically upgrade pip and install required libraries  ###
##############################################################################

import sys
import os
from subprocess import check_call


def __install(package: str) -> None:
    # install package
    result = check_call([sys.executable, "-m", "pip", "install", package])
    if result != 0:
        print('An Error has occurred while installing ' + package)
        _ = input("Press Enter to continue...")
    else:
        print('Successfully installed ' + package)
        _ = input("Press Enter to continue...")


def __clear_screen() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



def install_required_libraries() -> None:
    # make sure pip is installed first
    os.system(sys.executable + " " + os.getcwd() + "\install_lib\get_pip.py")
    
    _ = input("Press Enter to continue...")
    __clear_screen()

    # install youtube-dl
    __install('pygame')
    # install pyglet
    __install('pyglet')

    # clear screen and exit
    #__clear_screen()
    print("---FINISHED---")
    _ = input("Press Enter to continue...")
    __clear_screen()
