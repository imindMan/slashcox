class Logger:
    @staticmethod
    def newline():
        print("[#]")

    @staticmethod
    def log(*args):
        print("[#]", *args)

    @staticmethod
    def error(*args):
        print("[!]", *args)
