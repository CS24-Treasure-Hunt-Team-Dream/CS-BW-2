import time
import requests
import hashlib
import random
import os
import re

from cpu import CPU

from mine import proof_of_work, valid_proof
from helper_functions import handle_items, move_to_location, mine
from graphutils import graph
from player import Player
from dreamy import dreamy
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
    # path = graph.bfs(player.current_room, 1)
    # move_to_location(player, path)
    # for item in player.inventory:
    #     if "treasure" in item:
    #         player.sell_treasure(item)
    #         print(player.gold)

    # While 1000 gold, make way to pirate ry.
    while player.gold >= 10000:
        path = graph.bfs(player.current_room, 467)
        move_to_location(player, path)

    # At pirate ry, change name.
    name = NAME
    print(name)
    player.name_changer(name)
    print(f"New name: {player.name} ")
    # cooldown = response["cooldown"]
    # time.sleep(cooldown)

# Go to the Transmogrify
# path = graph.bfs(player.current_room, 495)
# move_to_location(player, path)
# print("Transmogrify!")
# exit()

# Go to the shrine, and use pray function
# path = graph.bfs(player.current_room, 22)
# move_to_location(player, path)
# print("PRAYING!")
# player.pray()

# print("Mining")
# path = graph.bfs(player.current_room, 195)
# move_to_location(player, path)
# response = player.init_player()
# print(response)
# mine(player)
# print(response)
# exit()
# path = graph.bfs(player.current_room, 461)
# move_to_location(player, path)
# print("Praying for dash")
# player.pray()
# exit()

# solve multiple puzzle with ls-8 and mine coins
# pattern = re.compile('/\d+(?=\D)/g')


def ls8(description):
    # Extract just the LS-8 program from the message
    code = description[41:].split('\n')

    # Relevant portion of the program that calculates the room number
    #
    # 10000010 LDI R1, VALUE_1      # Load R1 register with VALUE_1
    # 00000001
    # VALUE_1
    # 10000010 LDI R3, VALUE_2      # Load R3 register with VALUE_2
    # 00000010
    # VALUE_2
    # 10101000 AND R1, R3           # Calculate R1 & R3 and store in R1
    # 00000001
    # 00000010
    # 10000010 LDI R3, VALUE_3      # Load R3 register with VALUE_3
    # 00000010
    # VALUE_3
    # 10101011 XOR R1, R3           # Calculate R1 ^ R3 and store in R1
    # 00000001
    # 00000010
    # 01001000 PRA R1               # Print ASCII digit corresponding to the value in R1
    # 00000001
    # 00000001 HLT                  # Halt the CPU

    # Call the LS-8 emulator to run the program
    # cpu = CPU()
    # cpu.load(code)
    # message = cpu.run()[-3:]

    # Bypass LS-8 emulation by applying same math in the following LS-8
    message = chr(int(f"0b{code[122]}", 2) & int(
        f"0b{code[125]}", 2) ^ int(f"0b{code[131]}", 2))
    message += chr(int(f"0b{code[139]}", 2) & int(
        f"0b{code[142]}", 2) ^ int(f"0b{code[148]}", 2))
    message += chr(int(f"0b{code[156]}", 2) & int(
        f"0b{code[159]}", 2) ^ int(f"0b{code[165]}", 2))

    return int(message)


# maybe loop through once to start?
for i in range(0, 100):
    print("Heading to the well!")
    path = graph.bfs(player.current_room, 55)
    move_to_location(player, path)
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
    path = graph.bfs(player.current_room, ROOM_NR)
    move_to_location(player, path)

    # Mine at new location
    response = mine(player)
    # Need while loop for proof checking
    while "messages" not in response or not response["messages"] or "New Block Forged" not in response["messages"][0]:
        response = mine(player)
    answer = player.balance()
    print(f"Current balance: {answer}")

    path = graph.bfs(player.current_room, 55)
    move_to_location(player, path)
