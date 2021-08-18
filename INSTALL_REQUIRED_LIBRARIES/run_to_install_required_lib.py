#!/usr/bin/python
# Author: Hoang Truong

##############################################################################
###  a script to automatically upgrade pip and install required libraries  ###
##############################################################################

import sys
import os
import subprocess


def install(package):
    # install package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')



if __name__ == "__main__":

    # make sure pip is installed first
    os.system(sys.executable + " " + os.getcwd() + "\INSTALL_REQUIRED_LIBRARIES\get_pip.py")
    
    _ = input("Press Enter to continue...")
    clear_screen()

    # install youtube-dl
    install('pygame')
    # install pyglet
    install('pyglet')

    # clear screen and exit
    clear_screen()
    print("---FINISHED---")
    _ = input("Press Enter to continue...")
    clear_screen()