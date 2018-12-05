# mokemon

# Project Plan
### 26.11 - init
- Battle mechanism
- VS Battle
### 3.12
- Tournament mechanism
### 10.12 - update
- Graphical update
### 17.12
- Content update (more monsters and abilities) and presentation
### 24.12 - presentation
---------------
## Flow in Server:
- Create a tournament
- Construct the tournament bracket
- Save player infos
- Start tournament
------
Flow in Client:
------
- Enter a Nick: 
- 2 Options:
	- Search For Tournament
	- VS Battle
---
Search For Tournament
List of Tournament
- BOUN Tournament
-- Select Boun Tournament
BOUN Tournament
- Set lineup
- Wait until tournament starts
- Repeat until the client loses (or the end of the tournament)
	- Battle scene
	- Wait until next round starts
- Tournament final scene (Update on new stage)
Notes:
If quit, then no reconnection and the opponent wins directly
---
VS Battle
List of Players (in Vs Battle in the server)
- Winner59
-- Select Winner59
	- Wait for acceptance from Winner59
	- Set lineup
		- Wait until both players finish lineup
	- Battle scene
Notes:
If quit, then no reconnection and the opponent wins directly
------------------
Battle Scene
Both players picks an action and do necessary updates...
------------------------------------
Code Design in Server

server.py
- Communicate with server
- Construct tournament
- Handle all macthes in tournament
Classes:
Action
Monster
Game // calculates damages and does ncessary updates

------------------
Code Design in Client

client.py
- Communicate with server
- Update gui
gui.py
resources // image folder
