from classes import Town, NPC, Shop, Game
from functions import italic
import json

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
    ],
)

Samsun = Town("Samsun", [Dallas], [NPC("Gabe", ["Gabe: Nobody's been here in years!"])])

Home.places = [London, Dallas, Buffalo]

London.places = [Home, Shop(["Foreign Coin"], [25])]
Dallas.places = [Home, Samsun]
Buffalo.places = [
    Home,
    Shop(["Red Key"], [50]),
    "Pier",
]

g = Game()
g.setPlayers(Home)
g.run()
