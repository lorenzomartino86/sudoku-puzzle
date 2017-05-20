
class Helper(object):
    @staticmethod
    def cross(string1, string2):
        return [charOfString1+charOfString2
                for charOfString1 in string1
                for charOfString2 in string2]