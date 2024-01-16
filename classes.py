from itemID import *
from functions import *

currentT = 1

gameCompleted = False

helpS = """Commands:
    exit : closes the game
    type : displays character type thats currently being played
    switch : switches characters
    name : displays the name of the character currently being played
    location : displays the location of the character currently being played
    balance : displays the balance of the character currently being played
    health : displays the health of the character currently being played
    interact : interact with things in your location
    inventory : see everything in the inventory of the character being played
    quests : see all quests"""


class Game:
    def __init__(self):
        self.p = []
        self.finish = False
        self.ac = 0
        self.b = False

    def setPlayers(self, loc):
        n1 = input(colored(67, 194, 230, "Name for the Light Character : "))
        n2 = input(colored(67, 194, 230, "Name for the Dark Character : "))
        self.p = [Player(n2, loc), Player(n1, loc)]
        return self

    def chooseAction(self):
        inp = input(
            colored(52, 235, 52, "What to do?(type help for list of commands) : ")
        )
        if inp == "help":
            self.help()

        elif inp == "exit":
            self.exit()

        elif inp == "type":
            self.type()

        elif inp == "switch":
            self.switch()

        elif inp == "name":
            self.name()

        elif inp == "location":
            self.location()

        elif inp == "balance":
            self.balance()

        elif inp == "interact":
            self.interact()

        elif inp == "inventory":
            self.inventory()

        elif inp == "quests":
            self.questC()

    def help(self):
        print(colored(240, 201, 10, helpS))

    def exit(self):
        incP(colored(255, 0, 0, f"    Exiting game..."))
        exit()

    def type(self):
        global currentT
        if currentT == 1:
            txt = colored(67, 194, 230, f"    Light")
        else:
            txt = colored(67, 194, 230, f"    Dark")
        incP(txt)

    def switch(self):
        global currentT
        txt = colored(255, 0, 0, f"    Switching Characters...")
        incP(txt)
        if currentT:
            currentT = 0
        else:
            currentT = 1

    def name(self):
        global currentT
        incP(colored(67, 194, 230, f"    {self.p[currentT].name}"))

    def location(self):
        global currentT
        incP(colored(67, 194, 230, f"    {self.p[currentT].loc}"))

    def balance(self):
        global currentT
        incP(colored(67, 194, 230, f"    ${self.p[currentT].bal}"))

    def interact(self):
        global currentT
        print(self.p[currentT].loc.__str__(game=self))
        print("What to interact with?")
        select = input("")
        self = self.p[currentT].loc.interact(select, self)
        return self

    def inventory(self):
        global currentT
        for i in self.p[currentT].inv:
            print(colored(67, 194, 230, f"    {i}"))

    def questC(self):
        global currentT
        for i in self.p[currentT].quests:
            print(f"Requires: {i.need}, Reward: {i.rewardi}")

    def AddItem(self, pl):
        global currentT
        if currentT:
            self.p[currentT] = self.p[currentT].AddItem(pl)

    def run(self):
        global currentT
        while not gameCompleted:
            self.chooseAction()
            for i in self.p[currentT].quests:
                if i.need in self.p[currentT].inv:
                    print(f"Quest Completed, Recieved {i.rewardi}")
                    self = i.reward(self)
                    self.p[currentT].quests.remove(i)
            if "Glowing Gem" in self.p[currentT].inv and not self.b:
                print(
                    "You hear a rumbling sound from Beijing. But how do I get there..."
                )
                self.b = True
            if "Orb" in self.p[currentT].inv:
                print(
                    "Everything disappears, you wake up and you're home. Your real home."
                )
                break
        print("You've completed the game!!! Congrats!")
        exit()


class Player:
    def __init__(self, name, location, inventory=[], balance=100, typee=True):
        self.name = name
        self.loc = location
        self.inv = inventory
        self.bal = balance
        self.type = typee
        self.quests = []

    def AddItem(self, item):
        if item not in itemL:
            print("Item does not exist.")
            return self
        if len(self.inv) == 10:
            print("Inventory at max!")
        else:
            self.inv.append(item)
        return self

    def RemoveItem(self, item):
        if item not in itemL:
            print("Item does not exist.")
            return self
        if item in self.inv:
            self.inv.remove(item)
        else:
            print("That item is not in your inventory.")
        return self


class Shop:
    def __init__(self, items=[], prices=[]):
        self.items = items
        self.prices = prices

    def __str__(self):
        f = f""
        for i in range(len(self.items)):
            f += f"{self.items[i]} : {self.prices[i]} \n"
        return f

    def Buy(self, player, iid):
        if not (iid in self.items):
            print("Item not in shop.")
            return player
        ind = self.items.index(iid)
        if self.prices[ind] > player.bal:
            print("Not enough money!")
        if len(player.inv) == 10:
            print("Inventory at max!")
            return player
        player.bal -= self.prices[ind]
        player = player.AddItem(iid)
        return player

    def Sell(self, player, iid):
        if not (iid in player.inv):
            print("Item not in inventory.")
            return player
        player = player.RemoveItem(iid)
        i = int(idr[iid])
        if i == 0:
            player.bal += 10
        elif i == 1:
            player.bal += 20
        elif i == 2:
            player.bal += 20
        elif i == 3:
            player.bal += 30
        elif i == 4:
            player.bal += 50
        else:
            print("Cannot sell that item.")
            player.AddItem(iid)
        return player

    def interact(self, game):
        c = input("Would you like to buy or sell?: ").lower()
        if c == "buy":
            print(self)
            print("Which item would you like to buy?")
            inp = input("").title()
            if not inp in id.values():
                print("Item doesn't exist!")
                return game
            game.p[currentT] = self.Buy(game.p[currentT], inp)
        if c == "sell":
            for i in self.p[currentT].inv:
                print(i)
            inp = input("Which do you want to sell?: ").title()
            if not inp in id.values():
                print("Item doesn't exist!")
                return game
            game.p[currentT] = self.Sell(game.p[currentT], inp)
        return game


class NPC:
    def __init__(self, name, speech, given="", iid=-1, quest=""):
        self.name = name
        self.speech = speech
        self.given = given
        self.gbool = False
        self.quest = quest
        self.accepted = False
        self.itemID = iid

    def __str__(self):
        return self.name

    def interact(self, game):
        global currentT
        if self.itemID != -1:
            if self.accepted:
                for i in self.speech:
                    incP(colored(12, 173, 125, i))
                n = input("Accept?(y/n): ")
                if n == "y":
                    if self.itemID != None:
                        game.p[currentT].AddItem(id[self.itemID])
                        print(
                            f"You have recieved {id[self.itemID]} to help you on this quest!"
                        )
                    self.accepted = True
            else:
                print("You have already accepted this person`s quest!")
        else:
            if self.given != "" and self.gbool == False:
                if len(game.p[currentT].inv) != 10:
                    print(f"{self.name} has given you {self.given}")
                    self.gbool = True
                    game.p[currentT].inv.append(self.given)
                else:
                    print("Your inventory is full, you can't get the gift!")
                    return game
            if self.name == "Alex":
                game.ac += 1
            for i in self.speech:
                incP(colored(12, 173, 125, i))
        return game


class Quest:
    def __init__(self, need, rewardi):
        self.need = need
        self.rewardi = rewardi

    def reward(self, game):
        global currentT
        s = game
        game.AddItem(self.rewardi)
        game.p[currentT].inv.remove(self.rewardi)
        if len(game.p[currentT].inv) == 10:
            print("Quest's reward will be discarded due to having a full inventory!")
            print("The Quest can be redone.")
        return game


class Town:
    def __init__(self, name, places=[], people=[]):
        self.name = name
        self.places = places
        self.people = people

    def __str__(self, game):
        n = f""
        for i in self.places:
            if isinstance(i, Town):
                n += f"            {i.name} \n"
            elif isinstance(i, Shop):
                n += f"            Shop \n"
            else:
                n += f"            {i} \n"
        if game.b and self.name == "London":
            n += f"\n            Teleportation Center"
        o = f""
        for i in self.people:
            o += f"\n            {i.name}"
        if game.ac >= 3 and self.name == "Samsun":
            o += f"\n            Workers"
        if self.places != []:
            return colored(
                240,
                201,
                10,
                f"    {self.name}:  \n        Places: \n{n}        People: {o}",
            )
        else:
            return colored(240, 201, 10, f"    {self.name}:  \n        People: {o}")

    def interact(self, p, game):
        n = p.capitalize()

        # Crazy recursion that I think shouldnt work and should break python
        Home = Town(
            "Home",
            [],
            [
                NPC(
                    "Bob",
                    [
                        "Bob: Is that you?",
                        "You: What?",
                        "Bob: I can't believe you're back!",
                    ],
                )
            ],
        )

        London = Town(
            "London",
            [Home, Shop(["Foreign Coin"], [25])],
            [
                NPC(
                    "John",
                    [
                        "John: You're here! Please save us.",
                        "You: I'm confused, where am I?",
                        "John: You're in London, Rossumland! Where else would we be!?",
                    ],
                ),
                NPC(
                    "Linda",
                    ["You, I'm sorry, but who am I?", "Linda: You're our savior!"],
                ),
                NPC(
                    "Alex",
                    [
                        "Alex: Where have you been? We've missed you!",
                        "You: I don't know any of you.",
                    ],
                ),
                NPC(
                    "Miner",
                    [
                        "Miner: You famous around here?",
                        "You: I guess?",
                        "Miner: Have some stone, it's an honor.",
                        "You: What...",
                    ],
                    "Stone",
                ),
            ],
        )
        Dallas = Town(
            "Dallas",
            [Home],
            [
                NPC(
                    "James",
                    ["James: I thought you would never come back!", "You: Ok..."],
                ),
                NPC(
                    "Isabella",
                    ["Isabella: I can't believe it...", "You: Believe what?"],
                ),
                NPC(
                    "Lucas",
                    [
                        "Lucas: Great! You're here! Head to Buffalo and buy a Red Key so you can get to Budapest using the pier!",
                        "You: Um, sure.",
                    ],
                ),
            ],
        )
        Buffalo = Town(
            "Buffalo",
            [Home, Shop(["Red Key", "Blue Key", "Yellow Key"], [50, 50, 50]), "Pier"],
            [
                NPC(
                    "Liam",
                    [
                        "Liam: You don't belong here...",
                        italic("He knows something..."),
                    ],
                ),
                NPC("Lily", ["Lily: Sorry, I don't speak to outsiders."]),
                NPC(
                    "Miner",
                    [
                        "Miner: Oh, you're here, everyone knows you, you apparently live in another world where everyone else is from. They all expect you to save them.",
                        italic("Why me?..."),
                        "Miner: Take some gold, it might help!",
                    ],
                    "Gold",
                ),
            ],
        )

        Samsun = Town(
            "Samsun", [Dallas], [NPC("Gabe", ["Gabe: Nobody's been here in years!"])]
        )

        Home.places = [London, Dallas, Buffalo]

        London.places = [Home, Shop(["Foreign Coin"], [25])]
        Dallas.places = [Home, Samsun]
        Buffalo.places = [
            Home,
            Shop(["Red Key"], [50]),
            "Pier",
        ]

        Budapest = Town(
            "Budapest",
            [],
            [
                NPC(
                    "Sophia",
                    [
                        "Sophia: Oh! It's you! You know Alex in London? If you speak to him 3 times, he'll send his workers to Samsun. They can help you.",
                        "You: What? I have no clue what you're talking about.",
                        "Sophia: don't worry, you'll figure it out!",
                        "You: Ok...",
                        italic("That was weird..."),
                    ],
                ),
                NPC(
                    "Miner",
                    [
                        "Miner: I've heard of you...",
                        "Miner: Take some silver, it might help!",
                    ],
                    "Silver",
                ),
            ],
        )

        Beijing = Town(
            "Beijing",
            [],
            [
                NPC(
                    "Wise Woman",
                    "Wise Woman: You must be the chosen one my husband keeps yapping about, go to him, he knows what to do.",
                ),
                NPC(
                    "Wise Man",
                    "Wise Man: What! How did you get here! You must be the chosen one! Take this orb. It will save you.",
                    given="Glass Orb",
                ),
            ],
        )

        if (
            n == "Teleportation Center"
            and game.p[currentT].loc.name == "London"
            and "Teleporter" in game.p[currentT].inv
            and self.b
        ):
            if game.p[not currentT].loc.name == "Beijing":
                print("Your counterpart is there, you can't go there!")
                return game
            incP(colored(255, 102, 0, f"Teleporting to Beijing!"))
            game.p[currentT].loc = Beijing
            return game
        elif (
            n == "Teleportation Center"
            and game.p[currentT].loc.name == "Beijing"
            and "Teleporter" in game.p[currentT].inv
        ):
            if game.p[not currentT].loc.name == "London":
                print("Your counterpart is there, you can't go there!")
                return game
            incP(colored(255, 102, 0, f"Teleporting to London!"))
            game.p[currentT].loc = London
            return game
        elif n == "Teleportation Center" and not "London" in game.p[currentT].inv:
            print("You don't have a Teleporter! You can get one in Buffalo.")
            return game

        if (
            n == "Pier"
            and game.p[currentT].loc.name == "Buffalo"
            and "Red Key" in game.p[currentT].inv
        ):
            if game.p[not currentT].loc.name == "Budapest":
                print("Your counterpart is there, you can't go there!")
                return game
            incP(colored(255, 102, 0, f"Sailing to Budapest!"))
            game.p[currentT].loc = Budapest
            return game
        elif (
            n == "Pier"
            and game.p[currentT].loc.name == "Budapest"
            and "Red Key" in game.p[currentT].inv
        ):
            if game.p[not currentT].loc.name == "Buffalo":
                print("Your counterpart is there, you can't go there!")
                return game
            incP(colored(255, 102, 0, f"Sailing to Buffalo!"))
            game.p[currentT].loc = Buffalo
            return game
        elif n == "Pier" and not "Red Key" in game.p[currentT].inv:
            print("You don't have a Red Key!")
            return game
        if n == "Shop":
            for i in self.places:
                if isinstance(i, Shop):
                    game = i.interact(game)
                    return game
        for i in self.people:
            if n == i.name:
                game = i.interact(game)
                return game
        for i in self.places:
            if not isinstance(i, Shop):
                if n == i.name:
                    if game.p[not currentT].loc == i:
                        print("Your counterpart is there, you can't go there!")
                        return game
                    incP(colored(255, 102, 0, f"Going to {i.name}!"))
                    game.p[currentT].loc = i
                    return game
        if game.ac >= 3 and n == "Workers" and game.p[currentT].loc.name == "Samsun":
            print(
                "Head Worker: Buy a foreign coin for us in London and we will reward you with a glowing gem!"
            )
            game.p[currentT].quests.append(Quest("Foreign Coin", "Glowing Gem"))
            return game
        print("That's not a thing...")
        return game
