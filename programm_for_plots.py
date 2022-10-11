import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import AutoMinorLocator
from io import StringIO
import re
import argparse

def start_parsing():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('infile', help="input file")
    return parser.parse_args()

args = start_parsing()

with open(args.infile, 'r') as file:
    lines = file.readlines()
molecule = lines[0].strip()
table_data = lines[1:-3]
line = lines[-3].strip()
last_line = lines[-1].strip();

#reading the table for plot
table = pd.read_csv(StringIO("".join(table_data)), sep='\s+', header=None, names=['x', 'y', 'y_err', 'freq'], engine='python')
table_max = table.max()
table_min = table.min()
range_x = table_max.x - table_min.x
range_y = table_max.y - table_min.y + 2*table_max.y_err

amount_of_dots = len(table)

#reading parametrs for approximate line
(x1, y1, x2, y2) = re.findall(r'[0-9\-\+e\.]+|NaN', line)[0:4]
x = np.array([float(x1), float(x2)])
y = np.array([float(y1), float(y2)])

#reading the T_rot and N_tot line (it is the last line)
(T, T_err, N, N_err) = re.findall(r'[0-9\-\+e\.]+|NaN', last_line)[0:4]

#designing the plot
fig, ax = plt.subplots()

ax.grid(True, which = 'major')
ax.grid(True, which = 'minor', linestyle = 'dotted')

ax.plot(table.x, table.y, 'k.', ms = 8)
ax.errorbar(table.x, table.y, yerr = table.y_err, ecolor='black', fmt=' ', capsize=3)
ax.set_xlabel('$E_u/k_b$, K')
ax.set_ylabel('ln($N_u/g_u$), cm$^{-2}$')
ax.set_title(molecule)
ax.axis([max(0, table_min.x - 0.1*range_x), table_max.x + 0.1*range_x, table_min.y - table_max.y_err - 0.1*range_y, table_max.y + table_max.y_err + 0.1*range_y])

ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
ax.text(0.45, 0.82, " T$_{rot}$ = %s $\pm$ %s K  \n N$_{tot}$ = %s $\pm$ %s cm$^{-2}$"%(T, T_err, N, N_err), style='italic',
        bbox={'facecolor': 'white', 'alpha': 1, 'pad': 10}, transform=ax.transAxes,)

plt.plot(x, y, alpha=0.7)

#saving to pdf
plt.savefig(molecule+".pdf")
