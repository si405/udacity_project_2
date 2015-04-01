#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# Establish the connection to the database

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM match;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM player;")
    db_result = c.fetchone()[0]
    DB.close()
    return db_result

 
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO player (player_name) values (%s)", 
      (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT player_id, player_name, COUNT(WinMatch.winning_player_id) as Win, COUNT(PlayedMatch) as Played FROM Player LEFT OUTER JOIN Match AS WinMatch ON Player.player_id  = WinMatch.winning_player_id LEFT OUTER JOIN Match AS PlayedMatch ON ((Player.player_id = PlayedMatch.losing_player_id) or (Player.player_id = PlayedMatch.winning_player_id)) GROUP BY player_id;")
    db_result = c.fetchall()
    DB.close()
    return db_result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO match (winning_player_id,losing_player_id) values (%s, %s)", 
      (winner,loser))
    DB.commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    ## Create database connection
    db_result = []
    DB = connect()
    c = DB.cursor()

    ## Find all the players, their wins and matches played order by games won
    ## This returns the list in the order needed to process them as pairs
    c.execute("SELECT player_id, player_name, COUNT(WinMatch.winning_player_id) as Win, COUNT(PlayedMatch) as Played FROM Player LEFT OUTER JOIN Match AS WinMatch ON Player.player_id  = WinMatch.winning_player_id LEFT OUTER JOIN Match AS PlayedMatch ON ((Player.player_id = PlayedMatch.losing_player_id) or (Player.player_id = PlayedMatch.winning_player_id)) GROUP BY player_id order by Win DESC;")
    rows = c.fetchall()
 
    ## For the returned rows process them in pairs by just storing the information from the first
    ## player of the pair, reading the second player details and then adding that information to 
    ## the results. This is repeated for however many players are in the tournament
    ## Use a counter to determine the odd and even numbers of the pairs
    i = 1
    for row in rows:
        ## Is this the first player of the pair?
        if i % 2 != 0: 
            player_1_id = row[0]
            player_1_name = row[1]
        else:
            ## This is the second player of the pair so add the details to the result set
            pair = (player_1_id, player_1_name,row[0],row[1])
            db_result.append(pair)
        i = i + 1

    ## Close the database connection and return the results
    DB.close()
    return db_result


