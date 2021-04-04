__author__ = "Eetu Asikainen"


from xmlrpc.client import ServerProxy
from typing import Optional


def client_ui(host: str = 'localhost', port: int = 8000, path: str = 'ass2') -> None:
    client = ServerProxy(f"http://{host}:{str(port)}/{path}")
    print("Eddie Note client:", end="")
    while True:
        print("\nWelcome to Eddie Note, choose what you want to do:")
        print("1: Send data about a topic to the server")
        print("2: Request Wikipedia data on topic")
        print("3: Get the data on a topic stored on the server")
        print("0: Exit the program")
        case = input_sanitizer(input("Please input your choice: "), 3)

        if case is None:
            continue
        elif case == 0:
            break
        elif case == 1:
            add_data(client)
        elif case == 2:
            query_wikipedia(client)
        elif case == 3:
            get_data(client)



def input_sanitizer(in_str: str, max: int, min: int = 0) -> Optional[int]:
    try:
        result = int(in_str)
    except ValueError:
        print("Please make sure you input a number.")
        return

    if result in range(min, max + 1):
        return result
    else:
        print(f"Please make sure your choice is in the range of {min} to {max + 1}.")


def add_data(client: ServerProxy) -> None:
    topic = input("Please input the topic you want to add note to: ")
    note_name = input("Please input the name of the note: ")
    note = input(f"Please input the text you want to the note: ")
    print(client.write_data(topic, note_name, note))


def query_wikipedia(client: ServerProxy) -> None:
    topic = input("Please input the topic you want to add wikipedia data to: ")
    search_term = input("Please input the search term you want to use, blank uses topic name: ") or topic
    print("Querying wikipedia, this may take some time...")
    try:
        search_results = client.query_wikipedia(search_term)
    except BaseException as e:
        print("Caught the following error from server: ")
        print(e)
        return
    if not search_results:
        print(f"Didn't find articles matching search '{search_term}'.")
        return
    elif len(search_results) == 1:
        article_name = search_results[0]
    else:
        article_name = search_result_selector(search_results)
    if not article_name:
        print("Cancelling operation.")
        return
    print(topic, article_name)
    print(client.add_wiki_result(topic, article_name))


def search_result_selector(results: list) -> Optional[str]:
    while True:
        print("Please choose the number matching the article you want to add data from:")
        for index, result in enumerate(results, 1):
            print(f"{index}: {result}")
        print("0: Cancel")
        choice = input_sanitizer(input("Your choice: "), len(results))
        if choice:
            return results[choice-1]
        elif choice == 0:
            return


def get_data(client: ServerProxy) -> None:
    topic = input("Please input the topic you want to get data from: ")
    print(client.read_data(topic))


if __name__ == "__main__":
    client_ui()
