import requests

def login():
    """
    TODO: Implement it the right way.
    """
    input_data = input("Provide username.\nUsername: ")
    return input_data

def list_topics():
    pass

def main():
    login()

    while True:
        list_topics()
        input_data = input("Choose a topic.\n")

if __name__ == "__main__":
    main()
