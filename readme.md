# Multicircle
***Two player game build using pygame and UDP server written in Go.***

___

## Overview

This project was built to explore ways of commucation between processes using UDP transport layer protocol. The idea of the project was to implement a 2 player game using client-server architecture where the server is a mediator between 2 player processes. The task of the server is to accept data from both of the players, process it, and send all needed game data back to players. Game's client task is to render the gameplay on screen and at the same time communicate each step of the player to the server.

## Build & run

***Note:*** To build and run Multicircle game you need to have [Python](https://www.python.org/downloads/) and [Go](https://go.dev/dl/) installed on your machine.

### Build

- Clone this repository into your desired directory:
    
      git clone https://github.com/mykolamateichuk/two-player-game-using-pygame-and-udp.git .

- Go into *server/* directory and build the server executable:

      go build .

- Go into *client/* directory and initialize the virtual environment:

    ***Windows***

      python -m venv <your-venv-name>

    ***Mac & Linux*** (depends on your installation)
    
      python3 -m venv <your-venv-name>

- Activate the virtual environment:

    ***Windows***

      .\<your-venv-name>\Scripts\activate
    
    ***Mac & Linux***

      source <your-venv-name>/bin/activate

- Install pygame module from *requirements.txt*:

      pip install -r requirements.txt
    
### Run

*If you want to run the server and both clients on the same machine open 3 terminal windows/tabs and follow these steps:*

- In terminal **#1** run a server process inside *server/* directory:

      go run .

- In terminals **#2** and **#3** run clients processes inside *client/* directory:

      python multicircle.py

After starting before mentioned processes you should see 2 windows on your screen with POVs from clients. If you navigate to the terminal window/tab running the server you should see the log stream.

    
*If you want to run the server and clients on separate machines open terminal windows/tabs on all machines and follow these steps:*

- On machine **#1** run a server process inside *server/* directory:

      go run .

- On machine **#2** and **#3** run clients processes inside *client/* directory:

      python multicircle.py <ip-address-of-the-server>


    Example `python multicircle.py 192.168.1.1`

After starting before mentioned processes you should see running server logs on the first machine and windows with clients' POVs on the second and third machines.

***Note:*** You can combine method described above and run server and one client on one machine and the other client on another machine. In this case you have to specify IP address of the server only while starting the client on the second machine.

## Screenshots

![Gameplay Screenshot](/screenshots/screen1.png)
