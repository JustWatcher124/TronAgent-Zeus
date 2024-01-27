from env import ENV


def main() -> None:
    env = ENV()
    env.reset()
    while True:
        env.play_step([0, 1, 0],[])

if __name__ == "__main__":
    main()
