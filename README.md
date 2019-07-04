# pypass

Pypass is a fast, secure, and user-friendly CLI based password manager written in Python.

## Table of Contents
1. [Features](#features)
2. [Encryption](#encryption)
3. [User Guide](#user-guide)
4. [Examples](#examples)

## Features
Pypass serves as an alternative to pricey and bloated GUI-based password managers as well as well written CLI solutions that are very functional but often hard to use. Some features include:

* Secure storage of passwords in an embedded database.
* SHA-256 based encryption.
* Organized tree visualization of account information.
* Fuzzy saerching for account information
* Copy to clipboard
* Vim-based navigation

## Encryption
Pypass encrypts all passwords prior to storage. It uses the `cryptography` library built on the AES-128 specification and uses PBKDF2 (SHA-256 based) to derive keys. The master password to access the repository is salted and hashed (via `bcrypt`) and compared to user entries. The passwords generated by pypass use `urandom` to randomize ASCII letters and numbers.

## User Guide
### Setup and Dependencies
First, clone the repository:

```
$ git clone https://github.com/zhoufel1/pypass.git
```

It is recommended to use >=Python3.6.1. The dependencies are outlined in `requirements.txt`.

An install script `install` is included that will install and setup a virtual environment with the required dependencies. Alternatively, you can do:

```
$ pip3 install --upgrade -r requirements.txt
```

### Running pypass
The program is executed through via the 'run' script:
```
$ ./run
```
The program will prompt for the creation of a master password which will be used to access the database on future use.

It is VERY recommended for future convenience to create a shell script to access the virtual environment and run the program. For example, the following
`pypass` script allows pypass to be run via the command `pypass`:

```
#!/bin/bash

# Activate venv called 'password' containing the dependencies
source $HOME/.virtualenvs/password/bin/activate

# Run program
cd $HOME/pypass
./run

# Terminate venv on program close.
deactivate
```

### Usage
#### Navigation
Pypass's main menu can be navigated using `arrow keys` and `return` OR `h/j/k/l`.
Pressing `q` in the main menu terminates the program. The system clipboard is purged after the program terminates.
Pressing `ESC` during a search terminates the search.


## Examples

_project by Felix Zhou._
