'''
THIS FILE SHOULD BE CALLED ONLY WHEN NEW, EMPTY DATABASE IS CREATED AND TABLES STRUCTURE NEEDS TO BE RECOVERED
'''
table1_name = 'leagues'#this table must be filled in manually for each league
table1_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['league_ticker', 'varchar(5)', 'UNIQUE NOT NULL'],
                ['league_full_name', 'varchar(50)', 'UNIQUE NOT NULL'],
                ['league_hyperlink_prefix', 'varchar(100)', 'NOT NULL']
            ]

table2_name = 'teams'
table2_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['league_full_name', 'varchar(50)', 'NOT NULL REFERENCES leagues(league_full_name)'],
                ['league_ticker', 'varchar(5)', 'NOT NULL REFERENCES leagues(league_ticker)'],
                ['id_flashscore_team', 'varchar(20)', 'UNIQUE NOT NULL'],
                ['team_name', 'varchar(80)', 'NOT NULL'],
                ['team_ticker', 'varchar(5)', 'NOT NULL']
            ]

table3_name = 'matches'
table3_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_flashscore_match', 'varchar(20)', 'UNIQUE NOT NULL'],
                ['league_ticker', 'varchar(5)', 'NOT NULL REFERENCES leagues(league_ticker)'],
                ['match_date', 'date', 'NOT NULL'],
                ['match_time', 'time', 'NOT NULL'],
                ['home_team_name', 'varchar(80)', 'NOT NULL'],
                ['away_team_name', 'varchar(80)', 'NOT NULL'],
                ['hyperlink', 'varchar(100)', 'NOT NULL'],
                ['ht_q1_pts', 'varchar(3)', 'NOT NULL'],
                ['at_q1_pts', 'varchar(3)', 'NOT NULL'],
                ['ht_q2_pts', 'varchar(3)', 'NOT NULL'],
                ['at_q2_pts', 'varchar(3)', 'NOT NULL'],
                ['ht_q3_pts', 'varchar(3)', 'NOT NULL'],
                ['at_q3_pts', 'varchar(3)', 'NOT NULL'],
                ['ht_q4_pts', 'varchar(3)', 'NOT NULL'],
                ['at_q4_pts', 'varchar(3)', 'NOT NULL'],
                ['ht_q5_pts', 'varchar(3)'],
                ['at_q5_pts', 'varchar(3)'],
                ['ht_odds_start', 'varchar(100)'],
                ['at_odds_start', 'varchar(100)'],
                ['ht_odds_end', 'varchar(100)'],
                ['at_odds_end', 'varchar(100)'],
                ['home_team_ticker', 'varchar(5)', 'NOT NULL'],
                ['away_team_ticker', 'varchar(5)', 'NOT NULL'],
                ['id_flashscore_home_team', 'varchar(20)', 'NOT NULL REFERENCES teams(id_flashscore_team)'],                
                ['id_flashscore_away_team', 'varchar(20)', 'NOT NULL REFERENCES teams(id_flashscore_team)']                
            ]

table4_name = 'players_info'
table4_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_flashscore_player', 'varchar(20)', 'UNIQUE NOT NULL'],
                ['full_name', 'varchar(50)', 'NOT NULL'],
                ['player_position', 'varchar(50)', 'NOT NULL'],
                ['birth_date', 'varchar(15)', 'NOT NULL'],
                ['height', 'varchar(5)', 'NOT NULL'],
                ['hyperlink', 'varchar(80)', 'NOT NULL']
            ]

table5_name = 'players_statistic'
table5_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_flashscore_match', 'varchar(20)', 'NOT NULL REFERENCES matches(id_flashscore_match)'],
                ['id_flashscore_player', 'varchar(20)', 'NOT NULL REFERENCES players_info(id_flashscore_player)'],
                ['id_flashscore_team', 'varchar(20)', 'NOT NULL REFERENCES teams(id_flashscore_team)'],
                ['name_short', 'varchar(20)', 'NOT NULL'],
                ['team_ticker', 'varchar(5)', 'NOT NULL'],
                ['pts', 'varchar(5)'],
                ['reb', 'varchar(5)'],
                ['ast', 'varchar(5)'],
                ['min', 'varchar(5)'],
                ['fgm', 'varchar(5)'],
                ['fga', 'varchar(5)'],
                ['pm2', 'varchar(5)'],
                ['pa2', 'varchar(5)'],
                ['pm3', 'varchar(5)'],
                ['pa3', 'varchar(5)'],
                ['ftm', 'varchar(5)'],
                ['fta', 'varchar(5)'],
                ['plus_minus', 'varchar(5)'],
                ['ofrb', 'varchar(5)'],
                ['dfrb', 'varchar(5)'],
                ['pf', 'varchar(5)'],
                ['st', 'varchar(5)'],
                ['tovr', 'varchar(5)'],
                ['bs', 'varchar(5)'],
                ['ba', 'varchar(5)'],
                ['tfs', 'varchar(5)']
            ]

table6_name = 'player_carrer'
table6_cols=[
                ['id', 'SERIAL PRIMARY KEY'],
                ['id_player', 'int', 'NOT NULL REFERENCES players_info(id)'],
                ['id_flashscore_player',' varchar(20)', 'NOT NULL REFERENCES players_info(id_flashscore_player)'],
                ['season_start_year', 'varchar(4)', 'NOT NULL'],
                ['season_end_year', 'varchar(4)', 'NOT NULL'],
                ['id_flashscore_team', 'varchar(5)', 'NOT NULL REFERENCES teams(id_flashscore_team)'],
                ['league_ticker', 'varchar(5)', 'NOT NULL REFERENCES leagues(league_ticker)']
            ]

from sql_postgress_comms import DB

with DB() as db:
    db.create_table(table1_name, table1_cols)
    db.create_table(table2_name, table2_cols)
    db.create_table(table3_name, table3_cols)
    db.create_table(table4_name, table4_cols)
    db.create_table(table5_name, table5_cols)
    #db.create_table(table6_name, table6_cols)
    
    leagues=[
        ['ACB', 'Liga Endesa', 'https://www.flashscore.com/basketball/spain/acb-']
    ]

    db.insert_data(leagues, table_name='leagues')
    