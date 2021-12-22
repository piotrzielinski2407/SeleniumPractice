from extract_matches import ExtractMatchIds
from hyperlinks_handler import ArchiveLinkCreator

class ExtractSeasonsMatchId(ExtractMatchIds, ArchiveLinkCreator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hyperlinks = self.return_hyperlinks()

    def __str__(self):
        return 'Extract match id in seasons selcted in settings'

    def __repr__(self):
        return 'ExtractSeasonsMatchId()'


if __name__ == '__main__':
    #some testing here  

    test = ExtractSeasonsMatchId()
    