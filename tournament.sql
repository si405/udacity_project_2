-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the players table

CREATE TABLE player (
	player_id serial PRIMARY KEY,
	player_name varchar(40) NOT NULL
);

-- Create the tournament table

CREATE TABLE tournament (
	tournament_id serial PRIMARY KEY,
	tournament_name varchar(30) NOT NULL	
);

-- Create a table for the players in this tournament. Players can compete in multiple tournaments

CREATE TABLE tournament_players (
	tournament_players_id serial PRIMARY KEY,
	player_id integer references player(player_id)
);

-- Create the tournament results table

CREATE TABLE match (
	match_id serial PRIMARY KEY,
	tournament_id integer references tournament(tournament_id),
	winning_player_id integer references player(player_id),
	winning_score integer,
	losing_player_id integer references player(player_id),
	losing_score integer
);
