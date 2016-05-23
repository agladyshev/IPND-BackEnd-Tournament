#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteTournaments():
    """Remove all the tournaments from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "DELETE FROM tournaments")
    DB.commit()
    DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "DELETE FROM matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "DELETE FROM players")
    DB.commit()
    DB.close()


def getTournaments():
    """Returns the list of existing tournaments"""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT title FROM tournaments")
    tournaments_db = cursor.fetchall()
    DB.close()
    tournaments =[]
    for tournament in tournaments_db:
        tournaments.append(tournament[0])
    return tournaments    


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT count(*) FROM players")
    count = int(cursor.fetchall()[0][0])
    DB.close()
    return count


def countMatches():
    """
    Get total amount of matches played in all tournaments.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT count(*) FROM matches")
    matches_count = int(cursor.fetchall()[0][0])
    DB.close()
    return matches_count    


def countMatchesTournament(tournament_id):
    """
    Get total amount of matches played in the tournament.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT count(*) FROM matches WHERE tournament = %s", (tournament_id,))
    matches_count = int(cursor.fetchall()[0][0])
    DB.close()
    return matches_count       


def registerTournament(title):
    """
    Adds a tournament to the tournament database.
    Args:
      title: the title for the new tournament.
    """    
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO tournaments (title)"
        " VALUES (%s)", (title,))
    DB.commit()
    DB.close()    


def countPlayersTournament(tournament_id):
    """Returns the number of players currently registered in tournament"""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT count(*) FROM standings WHERE tournament = %s", (tournament_id,))
    count = int(cursor.fetchall()[0][0])
    DB.close()
    return count


def deleteMatchesTournament(tournament_id):
    """Remove all the match records for the tournament from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "DELETE FROM matches WHERE tournament = %s", (tournament_id,))
    DB.commit()
    DB.close()


def whatTournamentId(title):
    """
    Helper function to transform tournament title into tournament ID
    Input: tournament title
    Output: tournament id
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT id FROM tournaments WHERE title = (%s)", (title,))
    tournament_id = cursor.fetchall()
    DB.close()
    if not tournament_id:
        print "There is no tournament with the title:", title
    else:
        tournament_id = int(tournament_id[0][0])
        return tournament_id 


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO players (name)"
        " VALUES (%s)", (name,))
    DB.commit()
    DB.close()


def deletePlayer(name):
    """Purge the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "DELETE FROM players WHERE name = (%s)", (name,))
    DB.commit()
    DB.close()


def getFreePlayers():
    """
    This procedure returns a list of players, 
    which are not assigned to any tournament.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT name FROM players WHERE tournament is NULL")
    players = cursor.fetchall()
    free_players = []
    for player in players:
        free_players.append(player[0])
    return free_players


def enterTournament(name, tournament):
    """
    Assigns player to specific tournament.
    Could be used multiple times.
    Takes as input name of the player, and tournament title.
    Resets current standings in en tournament.
    """
    tournament_id = whatTournamentId(tournament)
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT * FROM matches " 
        "WHERE tournament = %s", (tournament_id,))
    matches = cursor.fetchall()
    # No players - no 
    if not matches:
        cursor.execute("UPDATE players SET tournament = %s WHERE name = %s",
            (tournament_id, name,))
        DB.commit()
    else:
        print ("\nMoving player to another tournament will reset the standings"
            " in :"), tournament
        print "Continue? (Y/N)"
        if raw_input().lower() == "y":
            cursor.execute("UPDATE players SET tournament = %s WHERE name = %s",
                (tournament_id, name,))
            cursor.execute("DELETE FROM matches WHERE tournament = %s",
                (tournament_id,))
            DB.commit()           
    DB.close()


def leaveTournament(name):
    """
    Makes player leave any tournament he participates in.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("UPDATE players SET tournament = NULL WHERE name = %s",
        (name,))
    DB.commit()    


def playerStandings(tournament):
    """Returns a list of the players and their win records 
    of the particular tournament, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Takes: tournament title
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT id, name, wins, matches FROM standings " 
        "WHERE tournament = %s", (whatTournamentId(tournament),))
    player_standings = cursor.fetchall()
    DB.close()
    return player_standings


def isSameTournament(id1, id2):
    """
    Determines whether two player are in the same tournament.
    Takes players' ids.
    Returns boolean.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT * FROM players as a, players as b "
        "WHERE a.tournament = b.tournament "
        "AND a.id = %s"
        "AND b.id = %s", (id1, id2,))
    valid_pairs = cursor.fetchall()
    DB.close()
    if not valid_pairs:
        print "The players", id1,"and", id2, "are not in the same tournament"
        return False
    else:
        return True


def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: title of the tournament
    We ask for tournament to simplify logic.
    We want to provide tournament title when initializing class tournament.
    """
    tournament_id = whatTournamentId(tournament)
    if isSameTournament(winner, loser):
        if not isRematch(winner,loser, tournament_id):
            DB = connect()
            cursor = DB.cursor()
            cursor.execute(
                "INSERT INTO matches (winner, loser, tournament) "
                "VALUES (%s, %s, %s)",(winner, loser, tournament_id,))
            DB.commit()
            DB.close()
        else:
            print("This pair has already played in the tournament")
 
 
def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Takes: tournament title
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    tournament_id = whatTournamentId(tournament)
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT id1, name1, id2, name2 FROM pairings WHERE tournament = %s",
        (tournament_id,))
    pairings_all = cursor.fetchall()
    DB.close()
    pairings_swiss = make_unique(pairings_all, tournament_id)
    if not pairings_swiss:
        print "There are no suitable pairs to continue the game"
        return pairings_swiss    
    if not (isOdd(tournament_id)):
        return pairings_swiss
    odd_player = findOdd(pairings_swiss, tournament_id)
    
    # logic to prevent player from skipping match twice
    while wasSkipped(odd_player, tournament_id):
        pairings_all = reArrange(pairings_all, odd_player)
        pairings_swiss = make_unique(pairings_all, tournament_id)
        odd_player = findOdd(pairings_swiss, tournament_id)

    return pairings_swiss


def make_unique(pairings_all, tournament_id):
    """Helper procedure for function swissPairings
    Takes as input list of all possible pairs
    Prevent rematches
    Outputs a list of pairs with unique players"""
    paired_ids = []
    unique_pairs = []    
    for pair in pairings_all:
        if not (isRematch(pair[0], pair[2], tournament_id)):
            if pair[0] not in paired_ids and pair[2] not in paired_ids:
                unique_pairs.append(pair)
                paired_ids.append(pair[0])
                paired_ids.append(pair[2])
    return unique_pairs


def isRematch(id1, id2, tournament_id):
    """
    Helper procedure, determines whether a pair of players
    has already played in the tournament.
    Takes two ids, tournament_id as an input, returns boolean.
    """ 
    pair = (id1, id2)
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT winner, loser FROM matches WHERE tournament = %s",
        (tournament_id,))
    matches_all = cursor.fetchall()
    DB.close()
    for match in matches_all:
        if pair == match or pair[::-1] == match:
            return True
    return False


def findOdd(pairings, tournament_id):
    """ 
    Searches for unpaired player.
    Input: list of paired players.
    Output: id of unpaired player.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
    "SELECT id FROM players WHERE tournament = %s",
        (tournament_id,))
    players_ids = cursor.fetchall()
    DB.close()
    all_ids = []
    for player_id in players_ids:
        all_ids.append(player_id[0])
    paired_ids = []
    for pair in pairings:
        paired_ids.append(pair[0])
        paired_ids.append(pair[2])
    odd_player = list(set(all_ids) - set(paired_ids))[0]
    return odd_player


def isOdd(tournament_id):
    """
    Checks if the number of players in tournament is odd
    """
    count = countPlayersTournament(tournament_id)
    if count % 2 != 0:
        return True
    else:
        return False


def wasSkipped(odd_player, tournament_id):
    """
    Helper procedure for tournament with odd number of players
    Takes as an input a player's id and return boolean on whether
    this player have skipped a round in current tournament.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT winner FROM matches "
        "WHERE loser is NULL AND tournament = %s", (tournament_id,))
    skippers = cursor.fetchall()
    DB.close()
    
    for skipper in skippers:
        if odd_player == skipper[0]:
            return True
    return False


def reArrange(pairings_all, player):
    """
    Helper procedure for rearranging intial list of paired players
    in order to secure match for particular player (for odd number of players)
    Takes as input list of all possible matches and player's id.
    Output is a rearranged list of matches with player's matches on top.
    """
    player_pairings = []
    other_pairings = []
    for pair in pairings_all:
        if pair[0] == player or pair[2] == player:
            player_pairings.append(pair)
        else:
            other_pairings.append(pair)
    pairings_all = player_pairings + other_pairings
    return pairings_all


def freeWin(odd_player, tournament_id):
    """
    Assigns free win to a player.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "INSERT INTO matches (winner, tournament) "
        "VALUES (%s, %s)", (odd_player, tournament_id,))
    DB.commit()
    DB.close()


def playRound(tournament):
    """
    Gaming procedure. Make players play one round with pseudorandom results.
    """
    tournament_id = whatTournamentId(tournament)
    pairings = swissPairings(tournament)
    if pairings:
        for pair in pairings:
            players = [pair[0], pair[2]]
            random.shuffle(players)
            reportMatch(players[0], players[1], tournament)    
        if (isOdd(tournament_id)):
            odd_player = findOdd(pairings, tournament_id)
            freeWin(odd_player, tournament_id)


def isWinner(tournament):
    """
    Checks if the winner is discovered.
    """
    wins = 0
    standings = playerStandings(tournament)
    for standing in standings:
        if int(standing[2]) == wins:
            return False
        if standing[2] > wins:
            wins = int(standing[2])
            winner = int(standing[0])
    return True


def generatePlayers(players_amount):
    """
    Procedure for retrieving a list of desired length with sample names.
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT name FROM names LIMIT (%s)", (players_amount,))
    players = cursor.fetchall()
    DB.close()    
    new_players = []
    for player in players:
        new_players.append(player[0])
    return new_players


def checkPlayer(player, tournament):
    """
    Checks if player participate in the tournament.
    Takes: player's name, tournament's title
    Outputs: boolean
    """
    tournament_id = whatTournamentId(tournament)
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM players WHERE name = (%s) "
        "AND tournament = (%s)", (player, tournament_id,))     
    players = cursor.fetchall()
    DB.close()  
    if players:
        return True
    else:
        return False    