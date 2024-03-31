# Homebound

A simple space tycoon game written in Python, with Pyglet.

# Ideas

## Mechanics

management game in space
- manage oxygen, food, energy (electricity):3
- launch sattelites (attack detection, communication)
- rocket fuel manufacturing
- ressources excavation (ore, sand, rocks, water, liquid oxygen, fuel ...)
- technology tree, with tech research buildings
- entertainement structures
- defense drone manufacturing
- transport ships manufacturing (people, ressources)

features:
- time speed switch (pause, real time, x2, x10 ...)
- specific technology needed for specific planets (cold / hot temperature resistance, high gravity)
- strategic choices of technology ? or Factorio-like tech tree
- setup new colonies on different planets / moons -> minimum ressources required
- win if Earth is restored
- loss if all people die / if martians restore earth before the player:3
- priority system on ressources production for each colony
- starting planet

places available:
- inner solar system:
    - Mercury
    - Venus
    - Earth -> moon
    - Mars -> enemies (uncolonizable)
    - asteroid belt -> Ceres, Pallas and Vestameow
- outer solar system:
    - Jupiter (gas giant) -> Ganymede, Callisto, Io, and Europa
    - Saturn (gas giant) -> Titan, Enceladus, Iapetus, Rhea, Dione, Tethys, and Mimas
    - Uranus (ice giant) -> Titania, Oberon, Umbriel, Ariel, and Miranda
    - Neptune (ice giant) -> Triton, Nereid, Proteus, Naiad, Thalassa, Despina and Galatea
    - The Centaurs (maybe not):3

---

Game background:
- Earth was destroyed because of climate change / nuclear war / biological weapons / zombies
- There is a moon base, already there, full of unspecialised colons
- You were chosen to lead the recolonization efforts of the earth: you were given the command of the few specialized people already on the base, a few resources and basic buildings

Goal: send enough resources (people + materials) to earth to win the game meow

Game loop:
- At the start of the game, the moon colony gives you basic amenities, like food, oxygen and energy
- you can train new workers, but they will require food and oxygen, so demand will increase
- no concept of money, only resources and time is payed
- you can build new buildings, like drill sites, schools (only on the moon) or research stations
- you can build new spaceships and spaceship modules at a spaceship factory
- you can build new colonies on other planets / moons, by sending a spaceship with a base module
- you can establish routes from colony to colony, or colony to earth
- to force the player to go explore, the resources are unlimited but harder / slower to drill as time passes (up to a minimum)
- each possible colony location has resources either scarce or abundant -> must colonise many worlds to be able to gather enough resources to win

types of workers:
- can be converted into new jobs at schools meow
- can be assigned to different buildings
- can be relieved / fired on the moon (sent back to base)
- each cost a given amount of resources and time to train
- workers -> build / operate the buildings
- flyers -> operate the spaceships
- scientists -> research new technologies:3

types of buildings (can be upgraded):
- drilling station
- warehouse
- research station
- water electrolysis station (oxygen + hydrogen)
- liquid tank
- furnace (metal ore processing)
- training school
- spaceship hangar
- spaceship factory
- spaceport (landing + take off)
- greenhouses (food)

types of spaceships: (different according to the amount of modules they can carry)
- small -> 1 modules
- medium -> 2 modules
- large -> 4 modules

spaceship modules:
- Liquid tanks
- resources storage
- base module (deployed on new colonies, base main building)
- passengers module

research possible:
- unlock buildings and spaceships
- research faster production (unlock building levels)
- make spaceships faster

types of resources:
- raw material:
    - rocks (sand, diamonds, ...)
    - ore (uranium, iron, carbon, copper, titanium, platinum ...)
    - water
- manufactured ressources:
    - oxygen
    - electricity
    - food
    - metal
    - hydrogen
    - liquid oxygen
    - liquid hydrogen

## Scenes

### Intro

- Present game setup
- click to continue

### Menus

#### Main menu

- "Game title"
- Continuer
- Nouvelle partie
- Quitter
- Mute button

#### Pause menu

- Continuer
- Sauvegarder
- Sauvegarder et quitter
- Mute button

### Solar system map

- Every planet side by side
- Sun on the left
- Planets not colonized are greyed out
- each colonized planet is clickable to switch to the colony view of the planet
- show trajectory and position of travelling spaceships
- normal / fast time scale

### Colony

- show building grid
- show resources (materials + life support)
- show members on base, by job
- button to build -> show list of unlocked buildings
- when hovering buildings, show:
    - building type
    - power required
    - number of assigned workers
    - level of building
- when clicking on buildings -> pop up:
    - show building type + level
    - show assigned workers, add and remove
    - show production (research, training, power generation, material drilled, ...)
    - button to enable/disable building
    - button to upgrade building, with required resources
    - button to destroy building
- "send spaceship" button (only available if a spaceport has been built) -> pop up:
    - destination field
    - which spaceship to use
    - which modules to attach
    - which resources to add in each module
- "research" button (only available if a laboratory has been built):
    - "start research" tab -> show price and time required to complete the research
    - "completed research" -> show all completed research
- "build spaceships" button -> adds spaceships to build queue
- "build modules" button -> adds modules to build queue
- hangar button:
    - show available spaceships
    - show available modules
- normal / fast time scale

### Game over
