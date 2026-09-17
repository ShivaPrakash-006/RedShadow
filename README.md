# Red Shadow
## Overview
A simple top-down endless scrolling spaceship shooter, where you play as the red shadow! Your objective? Destroy as much ships as possible and try not to get hit. Get coins, upgrade you ship,
obtain new and powerful ships, rinse and repeat!

## Tech Stack
- Python
- Pygame
- MySQL/PyMySQL

## How to run it
- Just make a MySQL DB with the following schema:
scores(playNo INT, username VARCHAR(50), ship VARCHAR(20), score INT, coins INT, time INT)

- Change the MySQL credentials in the *main.py* file

- Run!
