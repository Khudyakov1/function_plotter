from matplotlib import pyplot
import tkinter as tk
from math import *

class function_entry:
    def __init__(self, row, window):
        self.index = row
        self.function = tk.StringVar()
        self.window = window
        self.f_entry = tk.Entry(self.window, textvariable=self.function)
        self.f_entry.grid(row=self.index + 1, column=1, columnspan=4)
        self.f_label = tk.Label(window, text='f(x) = ')
        self.f_label.grid(row=self.index + 1, column=0)

    def activate(self):
        self.f_entry.config(state='normal')
    
    def deactivate(self):
        self.f_entry.config(state='disabled')

    def plot(self, min_x, max_x, plot_space):
        if self.function.get() == '':
            raise ValueError

        colors = ['g', 'b', 'peru']

        points = int(1e4)
        xlist = []
        ylist = []
        numbers = [0, 0]
        for k in range(points):
            x = min_x + (max_x - min_x) / points * k
            xlist.append(x)
            ylist.append(eval(self.function.get()))
            if ylist[k] > 0:
                numbers[0] += 1
            elif ylist[k] < 0:
                numbers[1] += 1
        ex_xlist = []
        ex_ylist = []
        for k in range(1,len(xlist) - 1):
            if (ylist[k - 1] < ylist[k] and ylist[k] > ylist[k + 1])\
                 or (ylist[k - 1] > ylist[k] and ylist[k] < ylist[k + 1]):
                ex_xlist.append(xlist[k])
                ex_ylist.append(ylist[k])
        plot_space[0].plot(xlist, ylist, color=colors[self.index])
        plot_space[0].plot(ex_xlist, ex_ylist, 'ro')
        plot_space[0].grid(color='gainsboro', linestyle='-', linewidth=2)
        plot_space[0].set_title('Функция f(x) = ' + self.function.get())
        plot_space[1].hist(ylist, 100, color=colors[self.index], density=True)
        plot_space[1].axis()
        plot_space[1].set_title('Распределение значений')
        labels = 'Положительные', 'Отрицательные'
        plot_space[2].pie(numbers)
        plot_space[2].legend(labels)
        plot_space[2].set_title('Распределение по знаку')
        
            

def plot_entries(entries, amount, xmin, xmax):
    fig, axs = pyplot.subplots(nrows=amount, ncols=3, figsize=(14,4 * amount))
    try:
        xmin = float(xmin)
        xmax = float(xmax)
        if amount > 1:
            for i in range(amount):
                entries[i].plot(xmin, xmax, axs[i])
        else:
            entries[0].plot(xmin,xmax,axs)
        pyplot.tight_layout()
        pyplot.show()
    except:
        pyplot.close()


def activate_entries(entries, amount):
    for i in range(len(entries)):
        if i < amount:
            entries[i].activate()
        else:
            entries[i].deactivate()

window = tk.Tk()

functions_amount = tk.IntVar()
functions_amount_menu = tk.OptionMenu(window, functions_amount, 1, 2, 3)
functions_amount_menu.grid(row=0, column=0)
functions_amount.trace_add('write', lambda var, index, mode: activate_entries(entries, functions_amount.get()))

range_min = tk.Entry(window, width=5)
range_min.grid(row=0, column=2)
range_min.insert(0, '-10')
tk.Label(text='от ').grid(row=0, column=1)
range_max = tk.Entry(window, width=5)
range_max.insert(0, '10')
tk.Label(text=' до ').grid(row=0, column=3)
range_max.grid(row=0, column=4)

entries = []
for i in range(3):
    entries.append(function_entry(i, window))

functions_amount.set(1)

graph_button = tk.Button(window, text='Построить график', command = lambda: plot_entries(entries, functions_amount.get(), range_min.get(), range_max.get()))
graph_button.grid(row=6, column=0, columnspan=5)


window.mainloop()