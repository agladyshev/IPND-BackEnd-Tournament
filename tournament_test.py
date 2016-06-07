#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options,
#be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.
from tournament import *


def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteMatches()
    deletePlayers()

    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1.countPlayers() returns 0 after initial deletePlayers() execution."
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1."
            " Got {c}".format(c=c))
    print "2.countPlayers() returns 1 after one player is registered."
    registerPlayer("Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2."
            " Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print """4. countPlayers() returns zero after registered players are
     deleted.\n5. Player records successfully deleted."""


def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteTournaments()
    deletePlayers()
    registerTournament("Polo")
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    enterTournament("Melpomene Murray", "Polo")
    enterTournament("Randy Schwartz", "Polo")
    standings = playerStandings("Polo")
    if len(standings) < 2:
        raise ValueError(
            "Players should appear in playerStandings even before "
            "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError(
            "Registered players' names should appear in standings, "
            "even if they have no matches played.")
    print """
    6. Newly registered players appear in the standings with no matches."""


def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteTournaments()
    deletePlayers()
    registerTournament("Polo")
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    enterTournament("Bruno Walton", "Polo")
    enterTournament("Boots O'Neal", "Polo")
    enterTournament("Cathy Burton", "Polo")
    enterTournament("Diane Grant", "Polo")
    standings = playerStandings("Polo")
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, "Polo")
    reportMatch(id3, id4, "Polo")
    standings = playerStandings("Polo")
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches()
    standings = playerStandings("Polo")
    if len(standings) != 4:
        raise ValueError(
            "Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError(
                "After deleting matches, players should have"
                " zero matches recorded.")
        if w != 0:
            raise ValueError(
                "After deleting matches, players should have"
                " zero wins recorded.")
    print """8. After match deletion, player standings are properly reset.\n9.
     Matches are properly deleted."""


def testPairings():
    """
    Test that pairings are generated properly
     both before and after match reporting.
    """
    deleteTournaments()
    deletePlayers()
    registerTournament("Polo")
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    enterTournament("Twilight Sparkle", "Polo")
    enterTournament("Fluttershy", "Polo")
    enterTournament("Applejack", "Polo")
    enterTournament("Pinkie Pie", "Polo")
    enterTournament("Rarity", "Polo")
    enterTournament("Rainbow Dash", "Polo")
    enterTournament("Princess Celestia", "Polo")
    enterTournament("Princess Luna", "Polo")
    standings = playerStandings("Polo")
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings("Polo")
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs."
            " Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2, "Polo")
    reportMatch(id3, id4, "Polo")
    reportMatch(id5, id6, "Polo")
    reportMatch(id7, id8, "Polo")
    pairings = swissPairings("Polo")
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs."
            " Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4),
     (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set(
        [frozenset([pid1, pid2]), frozenset([pid3, pid4]),
         frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


def testNoRematches():
    """Test that there are no rematches.
    Make isRematch return False all the time to test.
    """
    i = 0
    while i < 3:
        deleteTournaments()
        deletePlayers()
        registerTournament("Polo")
        registerPlayer("Twilight Sparkle")
        registerPlayer("Fluttershy")
        registerPlayer("Applejack")
        registerPlayer("Pinkie Pie")
        registerPlayer("Rarity")
        registerPlayer("Rainbow Dash")
        registerPlayer("Princess Celestia")
        registerPlayer("Princess Luna")
        enterTournament("Twilight Sparkle", "Polo")
        enterTournament("Fluttershy", "Polo")
        enterTournament("Applejack", "Polo")
        enterTournament("Pinkie Pie", "Polo")
        enterTournament("Rarity", "Polo")
        enterTournament("Rainbow Dash", "Polo")
        enterTournament("Princess Celestia", "Polo")
        enterTournament("Princess Luna", "Polo")
        playRound("Polo")
        playRound("Polo")
        playRound("Polo")
        db, cursor = connect()
        cursor.execute(
            "SELECT winner, loser FROM matches "
            "WHERE tournament = %s", (whatTournamentId("Polo"),))
        matches_all = cursor.fetchall()
        db.close()
        for match in matches_all:
            count = 0
            if match in matches_all in matches_all:
                count += 1
            if match[::-1] in matches_all:
                count += 1
            if count > 1:
                raise ValueError(
                    "Some of the players have played more than once "
                    "with each other")
        i += 1
    print ("11. No remathes have been played during"), i, ("games.")


def testFreeWins(tournament_id):
    """
    Part of testOddPlayers() test.
    Test to determine whether one player can receive free win only once
    """
    db, cursor = connect()
    cursor.execute(
        "SELECT winner FROM matches WHERE loser is NULL "
        "AND tournament = %s", (tournament_id,))
    free_wins = cursor.fetchall()
    db.close()
    free_winners = []
    for win in free_wins:
        if int(win[0]) in free_winners:
            raise ValueError(
                "More than one free win for player during tournament")
        free_winners.append(int(win[0]))
    print("All free wins are valid")


def testOddPlayers():
    """
    To prove that our tournaments work with odd number of players
    we play until winner is determined.
    Every round we check if every player had played his match and
    unpaired player had received free win.
    """
    print('Testing tournaments with odd number of players:')
    deleteTournaments()
    deletePlayers()
    registerTournament("Polo")
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    enterTournament("Twilight Sparkle", "Polo")
    enterTournament("Fluttershy", "Polo")
    enterTournament("Applejack", "Polo")
    enterTournament("Pinkie Pie", "Polo")
    enterTournament("Rarity", "Polo")
    enterTournament("Rainbow Dash", "Polo")
    enterTournament("Princess Celestia", "Polo")
    enterTournament("Princess Luna", "Polo")
    registerPlayer("Odd one")
    enterTournament("Odd one", "Polo")
    tournament_id = whatTournamentId("Polo")
    players_count = countPlayersTournament(tournament_id)
    rounds_played = 0
    while not (isWinner("Polo")):
        playRound("Polo")
        rounds_played += 1
        wins_count = countMatchesTournament(tournament_id)
        if wins_count != rounds_played * (int(players_count / 2) + 1):
            raise ValueError(
                "Number of wins in the round isn't correct."
                "Odd players didn't play.")
        print('Correct number of wins in the round'), rounds_played
        for standing in playerStandings("Polo"):
            if standing[3] != rounds_played:
                raise ValueError('Some players missed their match.')
        print ('Every player have played'), rounds_played, ('matches.')
    print('Tournament over. Winner is found.')
    testFreeWins(tournament_id)
    print('12. Tournament works with odd numbers.')


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testNoRematches()
    testOddPlayers()
    print "Success!  All tests pass!"
