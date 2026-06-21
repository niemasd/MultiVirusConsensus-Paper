#! /usr/bin/env python3
'''
Create benchmark figures
'''

# imports
from matplotlib import rcParams
from matplotlib.lines import Line2D
from pathlib import Path
from seaborn import pointplot, set_context, set_style
import matplotlib.pyplot as plt

# constants
RESULTS_PATH = Path(__file__).parent.parent / 'results'
FIG_PATH = RESULTS_PATH.parent / 'figures'
TRANSLATE = {
    'ivar': 'iVar Consensus',
    'mvc': 'MultiVirusConsensus',
    'viral_consensus': 'ViralConsensus',
    'time': 'Runtime (s)',
    'mem': 'Peak Memory (MB)',
}
COLOR = {
    'ivar': 'red',
    'mvc': 'green',
    'viral_consensus': 'blue',
}
LINESTYLE = {
    'ivar': '--',
    'mvc': '-',
    'viral_consensus': ':',
}

# configure matplotlib
RC = {"font.size":12,"axes.titlesize":16,"axes.labelsize":14,"legend.fontsize":10,"xtick.labelsize":10,"ytick.labelsize":10}
set_context("paper", rc=RC); set_style("ticks"); rcParams['font.family'] = 'serif'

# parse h:mm:ss or m:ss time as seconds
def parse_time(s):
    parts = [float(x) for x in s.strip().split(':')]
    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours = 0; minutes, seconds = parts
    else:
        raise ValueError(f"Invalid time: {s}")
    return (hours * 3600) + (minutes * 60) + seconds

# run tool
if __name__ == "__main__":
    # parse benchmark results data
    data = dict() # data[coverage][replicate][tool]['time/mem'] = value
    tools = set()
    for p in RESULTS_PATH.glob('simulated.x*.r*.time.*.txt'):
        cov = int(p.name.split('.')[1].lstrip('x'))
        if cov not in data:
            data[cov] = dict()
        rep = int(p.name.split('.')[2].lstrip('r'))
        if rep not in data[cov]:
            data[cov][rep] = dict()
        tool = p.name.split('.')[4].strip()
        if tool not in data[cov][rep]:
            data[cov][rep][tool] = {'time':0, 'mem':0}
        tools.add(tool)
        with open(p, 'rt') as f:
            for line in f:
                l = line.strip()
                if l.startswith('Elapsed (wall clock) time'):
                    data[cov][rep][tool]['time'] += parse_time(l.split(': ')[-1])
                elif l.startswith('Maximum resident set size'):
                    mem = int(l.split(': ')[-1]) / 1000 # convert KB to MB
                    data[cov][rep][tool]['mem'] = max(data[cov][rep][tool]['mem'], mem)

    # create figures
    for plot in ['time', 'mem']:
        fig, ax = plt.subplots(figsize=(10,5)); handles = list()
        for tool in ['ivar', 'viral_consensus', 'mvc']:
            handles.append(Line2D([0],[0],color=COLOR[tool],label=TRANSLATE[tool],linewidth=1.5,linestyle=LINESTYLE[tool]))
            x = list(); y = list()
            for cov in sorted(data.keys()):
                for rep in data[cov].keys():
                    x.append(cov); y.append(data[cov][rep][tool][plot])
            pointplot(x=x, y=y, color=COLOR[tool], linestyles=LINESTYLE[tool])
        plt.xlabel('Coverage')
        plt.ylabel(TRANSLATE[plot])
        ax.set_yscale('log')
        plt.legend(handles=handles,bbox_to_anchor=(0.005, 0.995), loc=2, borderaxespad=0., frameon=True)
        fig.savefig(FIG_PATH / f'{plot}.pdf', format='pdf', bbox_inches='tight')
