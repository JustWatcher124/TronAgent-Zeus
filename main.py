from game import SnakeGameAI

def main():
    game = SnakeGameAI()

    while True:
        
        game.play_step()
        print("#########################################")

if __name__ == "__main__":
    main()
