import random
from math import log2

import discord

END_SCORE = 2048

up_button = discord.ui.Button(emoji="⬆️", style=discord.ButtonStyle.green, row=4)
down_button = discord.ui.Button(emoji="⬇️", style=discord.ButtonStyle.green, row=4)
left_button = discord.ui.Button(emoji="⬅️", style=discord.ButtonStyle.green, row=4)
right_button = discord.ui.Button(emoji="➡️", style=discord.ButtonStyle.green, row=4)

colors = [discord.ButtonStyle.grey,
          discord.ButtonStyle.green, discord.ButtonStyle.red, discord.ButtonStyle.blurple]


def transpose(matrix):
    new = []

    for i in range(4):
        new.append([])
        for j in range(4):
            new[i].append(matrix[j][i])

    return new


def compress(matrix):
    changed = False

    new_mat = []

    for i in range(4):
        new_mat.append([0] * 4)

    for i in range(4):
        pos = 0
        for j in range(4):
            if matrix[i][j] != 0:
                new_mat[i][pos] = matrix[i][j]
                if j != pos:
                    changed = True
                pos += 1

    return new_mat, changed


def reverse(matrix):
    new_mat = []

    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(matrix[i][3 - j])

    return new_mat


def merge(matrix):
    changed = False
    for i in range(4):
        for j in range(3):

            if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                matrix[i][j] = matrix[i][j] * 2
                matrix[i][j + 1] = 0
                changed = True

    return matrix, changed


class Tile(discord.ui.Button):
    def __init__(self, label: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        power = int(log2(label)) if label > 0 else 0
        self.style = colors[power % len(colors)]
        self.label = str(label) if power > 0 else ' '
        self.disabled = True
        self.is_empty = False if power > 0 else True


class EmptyTile(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(label=0, *args, **kwargs)
        self.style = discord.ButtonStyle.grey
        self.label = ' '
        self.disabled = True
        self.is_empty = True


class Board(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        matrix = []
        for i in range(4):
            matrix.append([0] * 4)

        self.matrix = matrix
        self.add_new()
        self.add_new()

        self.update_board()

    def update_board(self):
        self.clear_items()
        up_button.callback = self.up_callback
        down_button.callback = self.down_callback
        left_button.callback = self.left_callback
        right_button.callback = self.right_callback
        self.add_item(up_button)
        self.add_item(down_button)
        self.add_item(left_button)
        self.add_item(right_button)

        for i in range(4):
            for j in range(4):
                self.add_item(
                    Tile(
                        label=self.matrix[i][j],
                        row=i
                    )
                    if self.matrix[i][j] > 0
                    else EmptyTile(row=i))

    def add_new(self):
        r = random.randint(0, 3)
        c = random.randint(0, 3)

        while self.matrix[r][c] != 0:
            r = random.randint(0, 3)
            c = random.randint(0, 3)

        self.matrix[r][c] = 2

    def get_game_state(self) -> int:
        """
        Returns the state of the game

        0: Game is not over
        1: Game is over and won
        2: Game is over and lost
        """

        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == END_SCORE:
                    return 1

        for i in range(4):
            for j in range(4):
                if 0 == self.matrix[i][j]:
                    return 0

        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i + 1][j] or self.matrix[i][j] == self.matrix[i][j + 1]:
                    return 0

        for j in range(3):
            if self.matrix[3][j] == self.matrix[3][j + 1]:
                return 0

        for i in range(3):
            if self.matrix[i][3] == self.matrix[i + 1][3]:
                return 0

        return 2

    def move_left(self, matrix):
        new, changed1 = compress(matrix)
        new, changed2 = merge(new)
        changed = changed1 or changed2
        new, temp = compress(new)
        if changed:
            self.matrix = new
        return new, changed

    def move_right(self, matrix):
        new = reverse(matrix)
        new, changed = self.move_left(new)
        new = reverse(new)
        self.matrix = new
        return new, changed

    def move_up(self, matrix):
        new = transpose(matrix)
        new, changed = self.move_left(new)
        new = transpose(new)
        self.matrix = new
        return new, changed

    def move_down(self, matrix):
        new = transpose(matrix)
        new, changed = self.move_right(new)
        new = transpose(new)
        self.matrix = new
        return new, changed

    async def up_callback(self, interaction: discord.Interaction):
        matrix, changed = self.move_up(self.matrix)
        if changed:
            self.add_new()
            self.update_board()
            if self.get_game_state() == 1:
                await interaction.response.edit_message(content="You won!", view=None)
            elif self.get_game_state() == 2:
                await interaction.response.edit_message(content="You lost!", view=None)
            else:
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("That doesn't seem to do anything...", ephemeral=True)

    async def down_callback(self, interaction: discord.Interaction):
        matrix, changed = self.move_down(self.matrix)
        if changed:
            self.add_new()
            self.update_board()
            if self.get_game_state() == 1:
                await interaction.response.edit_message(content="You won!", view=None)
            elif self.get_game_state() == 2:
                await interaction.response.edit_message(content="You lost!", view=None)
            else:
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("That doesn't seem to do anything...", ephemeral=True)

    async def left_callback(self, interaction: discord.Interaction):
        matrix, changed = self.move_left(self.matrix)
        if changed:
            self.add_new()
            self.update_board()
            if self.get_game_state() == 1:
                await interaction.response.edit_message(content="You won!", view=None)
            elif self.get_game_state() == 2:
                await interaction.response.edit_message(content="You lost!", view=None)
            else:
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("That doesn't seem to do anything...", ephemeral=True)

    async def right_callback(self, interaction: discord.Interaction):
        matrix, changed = self.move_right(self.matrix)
        if changed:
            self.add_new()
            self.update_board()
            if self.get_game_state() == 1:
                await interaction.response.edit_message(content="You won!")
            elif self.get_game_state() == 2:
                await interaction.response.edit_message(content="You lost!")
            else:
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message("That doesn't seem to do anything...", ephemeral=True)
