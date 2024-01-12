from game import SnakeGameAI
from settings import DEBUG

def main():
    game = SnakeGameAI()

    while True:
        
        game.play_step()
        if DEBUG:
            print("#########################################")

if __name__ == "__main__":
    main()
