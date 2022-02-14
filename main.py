from cache import cache_history
from settings import load_settings
from aditional_functions import substract_list_content
from extract_seasons import ExtractSeasonsMatchId
from multithread_scrapping import MatchScrapClientHandler,PlayerInfoClientHandler
from hyperlinks_handler import players_links_to_scrap
from write_data_to_DB import SaveScrappedData

settings = load_settings()
driver = ExtractSeasonsMatchId()
scrapped_match_ids = driver.return_matches_id()
match_id_in_DB = cache_history.load_match_ids()#pre load values for id's that already exist in DB
driver.driver.quit()
match_id_to_scrap = substract_list_content(scrapped_match_ids,match_id_in_DB)
scrap_handler = MatchScrapClientHandler(match_id_to_scrap)
scrap_handler.create_threads()
df_matches_data = scrap_handler.get_matches_data()
df_players_stats = scrap_handler.get_players_data()
players_hyperlinks = players_links_to_scrap(df_players_stats)
scrap_handler = PlayerInfoClientHandler(players_hyperlinks)
scrap_handler.create_threads()
df_players_info = scrap_handler.get_player_info()
save_handler = SaveScrappedData(df_matches_data,df_players_stats,df_players_info)
save_handler.save_data()
cache_history.close_DB_interface()





