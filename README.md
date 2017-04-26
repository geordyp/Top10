# Top10
A social media app where people can share their top ten favorite things under different categories.

## Setup
Install Vagrant and VirtualBox if you have not already done so.
### Starting The Project
1. After cloning this repo to your machine, cd into the projects directory.
2. Enter the command `vagrant up`. This command can take awhile to run. Ignore the error `default: stdin: is not a tty`.
3. Enter the command `vagrant ssh`.
4. Once vagrant is up and running cd into '/vagrant'. If you enter `ls` you will see that you are now in the projects directory from within the virtual environment.
5. Enter `python application.py` and navigate to 'localhost:5000' to view the project.
### Closing The Project
1. Enter the command `exit` to exit the vagrant environment.
2. Then enter the command `vagrant halt` to shut down the vagrant environment.

## Authors
* Reagan Wood
* Carrington Cooper
* Geordy Williams
