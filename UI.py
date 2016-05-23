#!/usr/bin/env python
# 
# UI.py -- Total Swiss Manager v1.0
# interactive implementation of Swiss-system tournament

from tournament import *
from printtable import pprinttable


def mainMenu():
    """
    Main gameplay procedure.
    Game start page.
    Allows to create new tournaments and enter tournaments to play in them.
    """
    print "\n||||| Total Swiss Manager v1.0 |||||\n"
    tournaments = getTournaments()
    print "Tournaments registered:", len(tournaments)
    print "Total amount of players registered:", countPlayers()
    print "Total amount of matches played:", countMatches()
    print "To create new tournament, enter 'CREATE'"
    print "To enter an existing tournament, enter 'PLAY'"
    print "To exit the game, enter 'EXIT'\n"  
    menu_choices = ['create', 'play', 'exit']
    choice = getInput(menu_choices)
    if choice == 'exit':
        return
    if choice == 'create':
        print "Please, enter the title for the tournament:"
        new_tournament = raw_input()
        registerTournament(new_tournament)
        mainMenu()
    if choice == 'play':
        if tournaments:
            print "\nList of tournaments:"
            printList(tournaments)
        else:
            print "There are no tournaments at the moment."
            print "You can CREATE tournament in main menu"
            print "To return back to main menu, press ENTER"
            raw_input()
            mainMenu()
        print "To start game, enter the title of the tournament"
        print "To return back to main menu, press ENTER"
        menu_choices = ['']
        menu_choices = menu_choices + tournaments
        choice = raw_input()
        while choice not in menu_choices:
            print "Incorrect input, try again:"
            choice = raw_input()          
        if choice == '':
            mainMenu()
        if choice in tournaments:
            tournamentMenu(choice)


def tournamentMenu(tournament):
    """
    Gameplay procedure.
    Takes tournament title as input.
    Allows player to view standings, organize rounds of tournament and to
    create/assign/unassign/delete players in the tournament.
    """
    tournament_id = whatTournamentId(tournament)
    print "\nYou have entered tournament", tournament
    players_count = countPlayersTournament(tournament_id)
    matches_count = countMatchesTournament(tournament_id)
    print "Number of registered players:", players_count
    print "Maches played:", matches_count
    if players_count != 0:
        current_round = 2 * matches_count / players_count
    else:
        current_round = matches_count
    print "Current round:", current_round, "\n"        
    print "To view the current standings, enter VIEW"
    print "To play next round, enter PLAY"
    print "To reset the standings, enter RESET"
    print "To add new player, enter ADD"
    print "To delete or unassign player or all players, enter DEL"
    print "To return back to main menu, press ENTER\n"
    menu_choices = ['view', 'play', 'reset', 'add', 'del','']
    choice = getInput(menu_choices)         
    if choice == '':
        mainMenu()
    if choice == 'view':
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER"
        raw_input()
        tournamentMenu(tournament)
    if choice == 'reset':
        deleteMatchesTournament(tournament_id)
        tournamentMenu(tournament)
    if choice == 'play':
        playRoundMenu(tournament)
    if choice == 'add':
        addPlayerMenu(tournament)
    if choice == 'del':
        delPlayerMenu(tournament)


def playRoundMenu(tournament):
    """
    Gameplay procedure.
    Takes tournament title as input.
    Allows user to run matches, autoplayed matches with pseudorandom result,
    view current standings.
    """
    print "\nTo view paired players for the next round, enter VIEW"
    print "To auto-play round, enter AUTO"
    print "To enter results manually, enter PLAY"
    print "To return to previous menu, press ENTER\n"
    menu_choices = ['view', 'auto', 'play', '']
    choice = getInput(menu_choices)
    if choice == 'view':
        headers = ['ID 1', 'Name 1', 'ID 2', "Name 2"]
        pprinttable(swissPairings(tournament), headers)
        print "\nTo return to previous menu, press ENTER"
        raw_input()
        playRoundMenu(tournament)
    if choice == '':
        tournamentMenu(tournament)
    if choice == 'auto':
        playRound(tournament)
        print "\nPress ENTER to see updated standings"
        raw_input()
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        playRoundMenu(tournament)
    if choice == 'play':
        manualRound(tournament)
        print "\nPress ENTER to see updated standings"
        raw_input()
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER"
        raw_input()
        playRoundMenu(tournament)


def manualRound(tournament):
    """
    Gameplay procedure.
    Takes tournament title as input.
    Allows player to run a round and 
    to decide what players would win.
    """
    tournament_id = whatTournamentId(tournament)
    pairings = swissPairings(tournament)
    headers = ['ID 1', 'Name 1', 'ID 2', "Name 2"]
    pprinttable(pairings, headers)
    for pair in pairings:
        print '\nWho should win:', pair[1], 'or', pair[3], '?'
        print "Enter the winner's id:"
        choices = [str(pair[0]), str(pair[2])]
        winner = getInput(choices)
        if winner == str(pair[0]):
            loser = pair[2]
        else: 
            loser = pair[0]
        reportMatch(int(winner), int(loser), tournament)
    if (isOdd(tournament_id)):
        odd_player = findOdd(pairings, tournament_id)
        freeWin(odd_player, tournament_id)
        print "\n", odd_player, 'receives a free win'


def addPlayerMenu(tournament):
    """
    Gameplay procedure.
    Takes tournament title as input.
    Menu allows player to view current standings,
    assign players to the tournament,
    create new players and autogenerate number of players.
    """
    tournament_id = whatTournamentId(tournament)
    print "\nTo view a current standings, enter VIEW"
    print "To add an unassigned player, enter ASSIGN"
    print "To create completely new player, enter NEW"
    print "To create a number of autogenerated players, enter AUTO"    
    print "To return to previous menu, press ENTER\n"
    choices = ['assign', 'new', 'view', '', 'auto']
    choice = getInput(choices)
    if choice == '':
        tournamentMenu(tournament)
    if choice == 'view':
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        addPlayerMenu(tournament)
    if choice == 'assign':
        assignMenu(tournament)
    if choice == 'new':
        print "Type the name of a new player:"
        add_player = raw_input()
        registerPlayer(add_player)
        enterTournament(add_player, tournament)
        print "\nTo return to previous menu, press ENTER\n"
        add_player = raw_input()
        addPlayerMenu(tournament)
    if choice == 'auto':
        print "Enter an positive integer amount of players (up to 100)"
        players_amount = getInt()
        new_players = generatePlayers(players_amount)
        for player in new_players:
            registerPlayer(player)
            enterTournament(player, tournament)
        print "\nPress ENTER to see updated standings"
        raw_input()
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        addPlayerMenu(tournament)          


def assignMenu(tournament):
    """
    Minor gameplay procedure.
    Takes tournament title as input.
    Supports functionality of addPlayerMenu()
    Allows to add unassigned players to the tournament.
    """
    free_players = getFreePlayers()
    if free_players:
        print "Currently unassigned players:"
        printList(free_players)
        print "Type the name of a player to add him to current tournament"
        add_player = raw_input()
        while add_player not in free_players:
            print "Incorrect input, try again:"
            add_player = raw_input() 
        enterTournament(add_player, tournament)
        print "\nPress ENTER to see updated standings"
        raw_input()
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        addPlayerMenu(tournament)
    else: 
        print "There are no free players at the moment"
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        addPlayerMenu(tournament)        


def delPlayerMenu(tournament):
    """
    Gameplay procedure.
    Takes tournament title as input.
    Creates menu which allows player to unassign 
    or delete players from tournament.
    """
    print "\nTo view a current standings, enter VIEW"
    print "To unassign all players from the tournament, enter UNALL"
    print "To delete all players in the tournament, enter DELALL"
    print "To unassign one player, enter UNASSIGN"
    print "To delete one player, enter DEL"
    print "To return to previous menu, press ENTER\n"    
    choices = ['unall', 'delall', 'unassign', '', 'del', 'view']
    choice = getInput(choices)
    if choice == '':
        tournamentMenu(tournament)
    if choice == 'view':
        dispStandings(tournament)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        delPlayerMenu(tournament)
    if choice == 'del':
        dispStandings(tournament)
        print "\nEnter the name of the player to delete permanently"
        player = raw_input()
        while not checkPlayer(player, tournament):
            print "Invalid input. Please, try again:"
            player = raw_input()
        deletePlayer(player)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        delPlayerMenu(tournament)
    if choice == 'unassign':
        dispStandings(tournament)
        print "\nEnter the name of the player to unassign from tournament"
        player = raw_input()
        while not checkPlayer(player, tournament):
            print "Invalid input. Please, try again:"
            player = raw_input()
        leaveTournament(player)
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        delPlayerMenu(tournament)
    if choice == 'unall':
        for player in playerStandings(tournament):
            leaveTournament(player[1])
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        delPlayerMenu(tournament)
    if choice == 'delall':
        for player in playerStandings(tournament):
            deletePlayer(player[1])
        print "\nTo return to previous menu, press ENTER\n"
        raw_input()
        delPlayerMenu(tournament)


def getInput(menu_choices):
    """
    Helper interface function for menu navigation.
    Takes as input a list of valid input entries.
    Returns valid player's input.
    """
    choice = raw_input().lower()
    while choice not in menu_choices:
        print "Incorrect input, try again:" 
        choice = raw_input().lower()
    return choice


def dispStandings(tournament):
    """
    Helper interface function.
    Prints standings in formatted view.
    Takes tournament title as input.
    """
    standings = playerStandings(tournament)
    headers = ['ID', 'Name', 'Wins', 'Matches']
    pprinttable(standings, headers)
    if standings:
        if isWinner(tournament):
            print '\nTournament is over. We have a winner!'
    if not standings:
        print '\nTournament has not yet begun'


def printList(list):
    """
    Helper interface function.
    Prints list in formatted view.
    """
    index = 1
    for element in list:
        print index, element
        index += 1


def getInt():
    """
    Helper interface procedure.
    Asks user for positive integer number.
    Returns positive integer number.
    """
    valid = False
    while not valid:
        number = raw_input()
        while not number.isdigit():
            print "That's not a positive integer!"
            print "Please enter a positive integer number: "
            number = raw_input()
        number = int(number)
        if number == 0:
            print "That's not a positive integer!"
            print "Please enter a positive integer number: "
        else:
            valid = True
    return number
     

mainMenu()
