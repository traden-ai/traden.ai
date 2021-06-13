class Earnings:

    """class for representing fundamental data regarding earnings"""

    def __init__(self, data):
        self.fiscalDateEnding = data["fiscalDateEnding"]
        self.reportedDate = data["reportedDate"]
        self.reportedEPS = data["reportedEPS"]
        self.estimatedEPS = data["estimatedEPS"]
        self.surprise = data["surprise"]
        self.surprisePercentage = data["surprisePercentage"]