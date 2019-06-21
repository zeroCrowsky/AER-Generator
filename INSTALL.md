Installation
====

#  Tool setup
Tested with Python 3.6.7, Ubuntu 18.04.2 LTS

Step 1 - Install pip3 :

    > curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    > python3 get-pip.py

Step 2 - Install virtualenv (via pip) :

    > pip3 install virtualenv

# Local install (via virtualenv and pip)
Step 1 - Create virtual environment (just once) :

    > virtualenv -p python3 env

Step 2 - activate virtual environment :  

    > source env/bin/activate

Step 3 - install dependencies :

    > pip install -r requirement.txt


# Notes
Deactivate virtual environment :

    > deactivate
    