'''
THIS FILE SHOULD BE CALLED ONLY WHEN NEW, EMPTY DATABASE IS CREATED AND TABLES STRUCTURE NEEDS TO BE RECOVERED
'''
table1_name = 'leagues'
table1_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['league_ticker', 'varchar(5)', 'UNIQUE NOT NULL'],
                ['league_full_name', 'varchar(50)', 'UNIQUE NOT NULL'],
                ['league_hyperlink', 'varchar(100)', 'NOT NULL']
            ]

table2_name = 'teams'
table2_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['league_full_name', 'varchar(50)', 'NOT NULL REFERENCES leagues(league_full_name)'],
                ['league_ticker', 'varchar(5)', 'NOT NULL REFERENCES leagues(league_ticker)'],
                ['team_name', 'varchar(80)', 'UNIQUE NOT NULL'],
                ['team_ticker', 'varchar(5)', 'UNIQUE NOT NULL']
            ]

table3_name = 'matches'
table3_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_flashscore_match', 'varchar(20)', 'UNIQUE NOT NULL'],
                ['league_ticker', 'varchar(5)', 'NOT NULL REFERENCES leagues(league_ticker)'],
                ['match_date', 'date', 'NOT NULL'],
                ['match_time', 'time', 'NOT NULL'],
                ['home_team_name', 'varchar(80)', 'NOT NULL REFERENCES teams(team_name)'],
                ['away_team_name', 'varchar(80)', 'NOT NULL REFERENCES teams(team_name)'],
                ['hyperlink', 'varchar(100)', 'NOT NULL'],
                ['ht_q1_pts', 'int', 'NOT NULL'],
                ['at_q1_pts', 'int', 'NOT NULL'],
                ['ht_q2_pts', 'int', 'NOT NULL'],
                ['at_q2_pts', 'int', 'NOT NULL'],
                ['ht_q3_pts', 'int', 'NOT NULL'],
                ['at_q3_pts', 'int', 'NOT NULL'],
                ['ht_q4_pts', 'int', 'NOT NULL'],
                ['at_q4_pts', 'int', 'NOT NULL'],
                ['ht_q5_pts', 'int'],
                ['at_q5_pts', 'int'],
                ['ht_odds_start', 'varchar(100)'],
                ['at_odds_start', 'varchar(100)'],
                ['ht_odds_end', 'varchar(100)'],
                ['at_odds_end', 'varchar(100)']
            ]

table4_name = 'players_info'
table4_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_flashscore_player', 'varchar(20)', 'UNIQUE NOT NULL'],
                ['full_name', 'varchar(50)', 'NOT NULL'],
                ['birth_date', 'date', 'NOT NULL'],
                ['height', 'int', 'NOT NULL'],
                ['hyperlink', 'varchar(80)', 'NOT NULL']
            ]

table5_name = 'players_statistic'
table5_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_match', 'int', 'REFERENCES matches(id)'],
                ['id_flashscore_match', 'varchar(20)', 'NOT NULL REFERENCES matches(id_flashscore_match)'],
                ['id_player', 'int', 'NOT NULL REFERENCES players_info(id)'],
                ['name_short', 'varchar(20)', 'NOT NULL'],
                ['team_ticker', 'varchar(5)', 'NOT NULL REFERENCES teams(team_ticker)'],
                ['pts', 'int', 'NOT NULL'],
                ['reb', 'int', 'NOT NULL'],
                ['ast', 'int', 'NOT NULL'],
                ['min', 'int', 'NOT NULL'],
                ['fgm', 'int', 'NOT NULL'],
                ['fga', 'int', 'NOT NULL'],
                ['pm2', 'int', 'NOT NULL'],
                ['pa2', 'int', 'NOT NULL'],
                ['pm3', 'int', 'NOT NULL'],
                ['pa3', 'int', 'NOT NULL'],
                ['ftm', 'int', 'NOT NULL'],
                ['fta', 'int', 'NOT NULL'],
                ['plus_minus', 'int', 'NOT NULL'],
                ['ofrb', 'int', 'NOT NULL'],
                ['dfrb', 'int', 'NOT NULL'],
                ['pf', 'int', 'NOT NULL'],
                ['st', 'int', 'NOT NULL'],
                ['tovr', 'int', 'NOT NULL'],
                ['bs', 'int', 'NOT NULL'],
                ['ba', 'int', 'NOT NULL'],
                ['tfs', 'int', 'NOT NULL']
            ]

table6_name = 'player_carrer'
table6_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_player', 'int', 'NOT NULL REFERENCES players_info(id)'],
                ['id_flashscore_player',' varchar(20)', 'NOT NULL REFERENCES players_info(id_flashscore_player)'],
                ['season_start_year', 'int', 'NOT NULL'],
                ['season_end_year', 'int', 'NOT NULL'],
                ['team_ticker', 'varchar(5)', 'NOT NULL REFERENCES teams(team_ticker)'],
                ['league_ticker', 'varchar(5)', 'NOT NULL REFERENCES leagues(league_ticker)']
            ]

from sql_postgress_comms import DB

with DB() as db:
    db.create_table(table1_name, table1_cols)
    db.create_table(table2_name, table2_cols)
    db.create_table(table3_name, table3_cols)
    db.create_table(table4_name, table4_cols)
    db.create_table(table5_name, table5_cols)
    db.create_table(table6_name, table6_cols)
