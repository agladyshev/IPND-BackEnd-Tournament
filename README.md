# IPND-BackEnd-Tournament
Study project, implementing Swiss tournament system into playable tournament manager.

Gameplay allows you to create multiple tournaments, manage matches manually and automatically, 
create, delete, move and even generate players.

Extra features:

1. Supports multiple amounts of tournaments
2. Supports odd number of players in the tournament
3. Prevents rematches between players
4. Custom user interface, with gameplay

List of contents:

1. tournament.py - main procedural file, contains all basic functions for Swiss Tournament and some helper-procedures for user interface.
2. tournament_test.py - contains test cases for testing main fuctionality of the algorythm and TC for extra features #2 and #3. Test Cases support Multi-Tournament system, but don't test it. Multiple tournaments have been tested via user interface (UI.py)
3. UI.py - a custom user interface with text gameplay. Takes advantage of procedural recursion in Python.
4. printtable.py - extra library I have used to display SQL query results in formatted view (I didn't write this code)
5. tournament.sql - database schema for Swiss Tournament algorythm. Also contains table "names" that is used to store autogenerated names.
        
Instructions:

1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
2. Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository
3. Launch the Vagrant VM (`vagrant up`) and connect to VM (`vagrant ssh`)
4. Navigate to tournament project folder `cd /vagrant/tournament`
5. Write `psql` to go to PostgreSQL
6. Run `\i tournament.sql` to create and import the tournament database schema
7. Once the database has been setup, quit the PostgreSQL interface using `\q`
8. Execute the following command  `python tournament_test.py` to test the main methods implemented in tournament.py
9. Test results will be printed on the screen
10. Execute the following command `python UI.py` to play the game based on Swiss tournament system
