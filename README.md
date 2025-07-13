# Tron: Zeus

> A modular reinforcement-learning framework for training and evaluating agents in a grid-based Tron-like game.

## Disclaimer

This project is based on [IsaiahPaget/TronAgent](https://github.com/IsaiahPaget/TronAgent), but has been heavily modified and extended. Please credit the original author accordingly.

## Purpose

1. Provide a system for training ML models using Reinforcement Learning.
2. Offer a modular and extensible architecture to plug in custom models.
3. Support gameplay against both ML agents and rule-based opponents.

## Major Enhancements

- Decoupled the game logic from PyGame.
- Designed extensible `Player` classes to support different learning strategies.
- Introduced modular training infrastructure (e.g., threaded training).
- Enabled optional game visualization and screenshot capture.
- Added support for all-against-all matchmaking and semi-automated video creation.

## Setup

> Note: This code was written with python version 3.11.12  
> newer versions might work, but you will have to test that out.

```bash
git clone https://github.com/JustWatcher124/TronAgent-Zeus.git
cd TronAgent-Zeus
pip install -r requirements.txt
```
### To play
```bash
python play_main.py
```
### To train
```bash
python threaded_training.py
```