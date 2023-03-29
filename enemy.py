# IMRORT MODULES
from paddle import Paddle
import pygame as pg
import random
import csv

class Enemy(Paddle):

    def __init__(self, x: int, y: int) -> None:
        """Defines the constructor for an Enemy object"""
        super().__init__(x, y)
        self.filename = "enemy_training_data.csv"
        self.fields = ["enemy_pos_y", "player_pos_y", "ball_pos_y", "successful"]

        self.data = self._read_data_()
        self._clean_data_()
        self.data = self._read_data_()

    def _clean_data_(self) -> None:
        """Removes duplicate entries from training data"""
        data_rows = []

        for row in self.data:
            row = row.replace("\n", "").split(",")
            if row not in data_rows:
                data_rows.append(row)

        try:
            with open(self.filename, "w") as file:
                writer = csv.writer(file)
                writer.writerows(data_rows)
        except FileNotFoundError:
            raise Exception("File \"{}\" Not Found!".format(self.filename))

    def _read_data_(self) -> list:
        """Reads training data from file"""
        training_data = ""

        try:
            with open(self.filename, "r") as file:
                training_data = file.readlines()
        except FileNotFoundError:
            raise Exception("File \"{}\" Not Found!".format(self.filename))

        return training_data

    def write_data(self, new_data: list) -> None:
        """Writes new training data to file"""
        try:
            with open(self.filename, "a") as file:
                writer = csv.writer(file)
                if len(self.data) == 0:
                    writer.writerow(self.fields)
                writer.writerows(new_data)
        except FileNotFoundError:
            raise Exception("File \"{}\" Not Found!".format(self.filename))

    def make_decision(self, player_pos_y, player_height, window: object):
        for x,line in enumerate(self.data):
            if x > 0:
                fields = line.split(",")
                if player_pos_y in range(int(float(fields[1])), int(float(fields[1])) + player_height):
                    return int(float(fields[2]) - self.height/2)
        return None
