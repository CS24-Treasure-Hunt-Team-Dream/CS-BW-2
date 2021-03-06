import os

from helper_functions import move_to_location, mine, ls8
from graphutils import graph
from player import Player
from dotenv import load_dotenv

load_dotenv()
MAIN_API_KEY = os.getenv("MAIN_API_KEY")
TEST_API_KEY = os.getenv("TEST_API_KEY")
MAIN_URL = os.getenv("MAIN_URL")
TEST_URL = os.getenv("TEST_URL")
NAME = os.getenv("NAME")
ROOM_NR = os.getenv("ROOM_NR")

TESTING = False
API_KEY = MAIN_API_KEY if not TESTING else TEST_API_KEY
URL = MAIN_URL if not TESTING else TEST_URL

player = Player()
print(f"Current cooldown: {player.cooldown}")

print("Hunting for treasure!")
print(f"New name: {player.name}")
print(f"Current gold: {player.gold}")
response = player.balance()
print(f"Current balance: {response}")
print(f"Player class: {player.abilities} ")
print(f"Player inventory: {player.inventory} ")
visited = set({})
# Once we have a name, we no longer collect gold. While no name or not 1000 gold, we traverse the map for treasure
while player.gold < 1000 and "User" in player.name:

    # Go to random room
    # If there are items in the room, then we take those items up until we are encumbered.
    # When we hit max items, we should return to the shop from our current room.
    # while player.encumbrance < player.strength - 1:
    #     visited.add(player.current_room)

    #     exits = graph.rooms[player.current_room]["exits"]
    #     unvisited = {direction: room for direction,
    #                  room in exits.items() if room not in visited}
    #     if unvisited:
    #         exits = unvisited

    #     direction = random.choice([d for d in exits])

    #     print(f"Moving {direction}...")
    #     player.wise_explorer(direction, exits[direction])
    #     print(f"Player moved {direction} to room {player.current_room}")

    #     for item in player.room_items:
    #         print(f"Found {item}! Taking it...")
    #         handle_items(player, item)
    #         print(f"Took {item}.\nCurrent items: {player.inventory}")

    # # Go back to the shop and sell the item
    # move_to_location(player, 1)
    # for item in player.inventory:
    #     if "treasure" in item:
    #         player.sell_treasure(item)
    #         print(player.gold)

    # While 1000 gold, make way to pirate ry.
    while player.gold >= 10000:
        move_to_location(player, 467)

    # At pirate ry, change name.
    name = NAME
    print(name)
    player.name_changer(name)
    print(f"New name: {player.name} ")
    # cooldown = response["cooldown"]
    # time.sleep(cooldown)

# Go to the Transmogrify
# move_to_location(player, 495)
# print("Transmogrify!")
# exit()

# Go to the shrine, and use pray function
# move_to_location(player, 22)
# print("PRAYING!")
# player.pray()

# print("Mining")
# response = player.init_player()
# print(response)
# mine(player)
# print(response)
# exit()
# move_to_location(player, 461)
# print("Praying for dash")
# player.pray()
# exit()

# solve multiple puzzle with ls-8 and mine coins


# maybe loop through once to start?
for i in range(0, 100):
    print("Heading to the well!")
    move_to_location(player, 55, PICKUP_ENABLED=False)
    response = player.examine(treasure="Wishing Well")
    if TESTING:
        print(response)
    print("Peering into the well...")
    ROOM_NR = ls8(response['description'])
    print("Decoded the location!")
    # Solve the puzzle
    # Get back a number

    # Move from the well to the new location
    print("Heading to the mine!")
    move_to_location(player, ROOM_NR, PICKUP_ENABLED=False)

    # Mine at new location
    response = mine(player)
    # Need while loop for proof checking
    while "messages" not in response or not response["messages"] or "New Block Forged" not in response["messages"][0]:
        response = mine(player)
    answer = player.balance()
    print(f"Current balance: {answer}")
