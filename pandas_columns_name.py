pandas_matches_columns_names = ('flashscore_match_id', 'league_ticker', 'date', 
                                'time', 'home_team', 'away_team', 
                                'hyperlink', 'ht_qt1_pts', 'at_qt1_pts', 
                                'ht_qt2_pts', 'at_qt2_pts', 'ht_qt3_pts', 
                                'at_qt3_pts', 'ht_qt4_pts', 'at_qt4_pts', 
                                'ht_qt5_pts', 'at_qt5_pts', 'ht_odds_start', 
                                'at_odds_start', 'ht_odds_end', 'at_odds_end', 
                                'home_team_ticker', 'away_team_ticker', 'id_flashscore_home_team',
                                'id_flashscore_away_team')

pandas_players_stats_columns_names = ('id_flashscore_match', 'id_flashscore_player', 
                                        'id_flashscore_team', 'player_hyperlink',
                                        'name_short', 'team_ticker',  
                                        'pts', 'reb', 'ast', 'min',
                                        'fgm', 'fga', 'pm2', 'pa2',
                                        'pm3', 'pa3', 'ftm', 'fta',
                                        'plus_minus', 'ofrb', 'dfrb', 'pf',
                                        'st', 'tovr', 'bs', 'ba',
                                        'tfs')

pandas_players_info_columns_names = ('id_flashscore_player', 'player_name',
                                    'position', 'birth_date',  
                                    'height', 'hyperlink' )

pandas_teams_columns_name = ('league_full_name', 'league_ticker',
                            'id_flashscore_team', 'team_name', 
                            'team_ticker')
