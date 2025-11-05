from player import Player
from weapon import Weapon
from vehicle import Vehicle
from map import Map



player1 = Player("Player1")
player1.move(10, 20)
player1.take_damage(30)



player2 = Player("Player2")
player3 = Player("Player3")

akm = Weapon("AKM", 49)
m416 = Weapon("M416", 43)
buggy = Vehicle("Buggy", 90)
jeep = Vehicle("Jeep", 70)

erangel = Map("Erangel", "8x8 km")

erangel.add_player(player1)
erangel.add_player(player2)
erangel.add_player(player3)
erangel.add_vehicle(buggy)
erangel.add_vehicle(jeep)
player1.move(10, 20)
player1.pick_up_weapon(akm)
player2.move(15, 30)
player2.pick_up_weapon(m416)
buggy.drive("School")
jeep.drive("Military Base")
player1.take_damage(40)
buggy.take_damage(70)


