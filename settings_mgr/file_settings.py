class FileSettings():
    file_settings = {
    "finename" : "Unknown",
    "renderProps" : {
        "engine" : "Unknown",
        "featureSet" : "Unknown",
        "device" : "Unknoown"
    },
    "outputProps" : {
        "resolution" : {
            "x" : 0,
            "y" : 0
        }
    }
}

    def __init__(self, filename):
        self.file_settings.filename = fileName

    def compare(self, otherFileSettings):
        # default to being the same (ie o, not 1)
        result = 0
        
        # do the comparison work here
        return result
        