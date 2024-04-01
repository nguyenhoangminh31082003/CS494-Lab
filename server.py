from Server.ServerModel import ServerModel

if __name__ == '__main__':
    N = 0
    while N < 2 or N > 10:
        n = input("How many players in a game (2 <= N <= 10): ")
        N = int(n)
    
    gameServer = ServerModel(N)
    gameServer.run()