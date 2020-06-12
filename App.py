import tkinter as tk
import tkinter.ttk as ttk
import \
    mywidgets as mw
from random import choice, shuffle

OX = ['O', 'X']
VINS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
PS = [[0, 2, 6, 8], [1, 3, 5, 7]]
S = 'Зіграно ігор: {}.\nІз них:\n    перемог - {};\n    поразок - {};\n    нічиїх - {}.'


class App(tk.Frame):
    user_win = pc_win = drawn = 0

    def __init__(self, master):
        super(App, self).__init__(master)
        self.create_widgets()

    def create_widgets(self):

        # Статистика гри
        self.info = mw.Cells(self, title='Статистика', text=S.format(0, 0, 0, 0))
        self.info.grid(column=0, row=0, rowspan=2, sticky='nsew')
        # Radiogrup Вибір ходу
        self.step = mw.Radiogrup(self, text='Вибрати хід', items=('Випадково', 'Першим', 'Другим'))
        self.step.grid(column=1, row=0, rowspan=2, sticky='nsew')
        # Radiogrup Вибір знака
        self.sign = mw.Radiogrup(self, text='Вибір знака', items=('Ваш знак "0"', 'Ваш знак "X"'))
        self.sign.grid(column=2, row=0, sticky='nsew')
        # кнопка старт
        self.btn = ttk.Button(self, text="Старт", command=self.start)
        self.btn.grid(column=2, row=1, sticky='nsew')
        # Статус игры
        self.stat = mw.Cells(self, title='Статус гри', text='Вітаємо вас в грі "Хрестики - Нулики"!')
        self.stat.grid(column=0, row=2, columnspan=3, sticky='nsew')
        # Игровые ячейки
        self.cells = mw.Cells(self, cols=3, rows=3, bd=3, relief='raise', width=2, font='Menlo 100')
        self.cells.grid(column=0, row=3, columnspan=3)

    def start(self):
        '''Запуск игры'''
        self.continue_ = True
        self.board = [''] * 9
        self.free_cells = list(range(9))
        self.stat.grup[0].config(text='Обережно! Гра активована! Удачі!')
        for i in range(9):
            self.cells.bind_("<Button-1>", self.turn_user, i)
            self.cells.grup[i].config(bg='white', text='')
        if self.step.var.get() == 2:
            self.turn_pc()
        elif self.step.var.get() == 0:
            if choice([1, 2]) == 2:
                self.turn_pc()
        self.widget_state()

    def widget_state(self, wst='disabled'):
        [i.config(state=wst) for i in [*mw.Radiogrup.grup, self.btn]]

    def find_best_turn(self, sign):
        for iturn in self.free_cells:
            iboard = self.board[:]
            iboard[iturn] = sign
            for a, b, c in VINS:
                if iboard[a] == iboard[b] == iboard[c] == sign:
                    return iturn

    def default_choice(self):
        choise = [4]
        for i in PS:
            shuffle(i)
            choise.extend(i)
        for iturn in choise:
            if iturn in self.free_cells:
                return iturn

    def turn_user(self, cell_num):
        '''Ход игрока'''
        self.turn(cell_num, self.sign.var.get())
        if self.continue_:
            self.turn_pc()

    def turn_pc(self):
        '''Ход компьютера'''
        cell_num = self.find_best_turn(not self.sign.var.get())
        if cell_num == None:
            cell_num = self.find_best_turn(self.sign.var.get())
            if cell_num == None:
                cell_num = self.default_choice()
        self.turn(cell_num, not self.sign.var.get())

    def turn(self, cell_num, sign):
        '''Обработка текущего хода и определение исхода игры'''
        self.cells.grup[cell_num].unbind("<Button-1>")
        self.cells.grup[cell_num].config(text=OX[sign])
        self.board[cell_num] = sign
        self.free_cells.remove(cell_num)
        for a, b, c in VINS:
            if self.board[a] == self.board[b] == self.board[c] == sign:
                if sign == self.sign.var.get():
                    self.stat.grup[0].config(text='Вітаю з перемогою')
                    self.user_win += 1
                    color = 'green'
                else:
                    self.stat.grup[0].config(text='Перемога за ПК! Ну як так?!!!')
                    self.pc_win += 1
                    color = 'red'
                [self.cells.grup[i].config(bg=color) for i in (a, b, c)]
                [self.cells.grup[i].unbind("<Button-1>") for i in self.free_cells]
                self.game_over()
                return
        if not self.free_cells:
            self.stat.grup[0].config(text='Нічия. Ви точно можете краще!')
            self.drawn += 1
            [cell.config(background='yellow') for cell in self.cells.grup]
            self.game_over()

    def game_over(self):
        '''Окончание игры'''
        self.continue_ = False
        self.info.grup[0].config(
            text=S.format(self.user_win + self.pc_win + self.drawn, self.user_win, self.pc_win, self.drawn))
        self.widget_state('normal')


def main():
    root = tk.Tk()
    root.title('Гра хрестики-нулики"')
    root.resizable(False, False)
    App(root).grid()
    root.mainloop()


if __name__ == '__main__':
    main()
