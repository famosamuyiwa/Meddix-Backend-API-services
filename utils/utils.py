class Utils():


    def getCID(aid):
        splittedAId = aid.split("-")
        return splittedAId[1]

    def getPID(aid):
        splittedAId = aid.split("-")
        return splittedAId[2]