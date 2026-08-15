#! /usr/bin/env python3
'''
Create benchmark figures
'''

# imports
from matplotlib import rcParams, use
from matplotlib.lines import Line2D
from pathlib import Path
from seaborn import pointplot, set_context, set_style
from subprocess import run
from tqdm import tqdm
import matplotlib.pyplot as plt

# constants
BENCHMARK_PATH = Path(__file__).parent.parent
RESULTS_PATH = BENCHMARK_PATH / 'results'
REFERENCES_PATH = BENCHMARK_PATH / 'references'
FIG_PATH = RESULTS_PATH.parent / 'figures'
TRANSLATE = {
    'ivar': 'iVar Consensus',
    'mvc': 'MultiVirusConsensus',
    'viral_consensus': 'ViralConsensus',
    'time': 'Runtime (s)',
    'memory': 'Peak Memory (MB)',
    'accuracy': 'Percent Identity',
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
use('Agg')
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
    data = dict() # data[coverage][replicate][tool]['time/memory'] = value
    tools = set()
    print("Parsing /usr/bin/time outputs...")
    for p in tqdm(list(RESULTS_PATH.glob('x*.r*.time.*.txt'))):
        cov = int(p.name.split('.')[0].lstrip('x'))
        if cov not in data:
            data[cov] = dict()
        rep = int(p.name.split('.')[1].lstrip('r'))
        if rep not in data[cov]:
            data[cov][rep] = dict()
        tool = p.name.split('.')[-2].strip()
        if tool not in data[cov][rep]:
            data[cov][rep][tool] = {'time':0, 'memory':0, 'accuracy':list()}
            tools.add(tool)
        with open(p, 'rt') as f:
            for line in f:
                l = line.strip()
                if l.startswith('Elapsed (wall clock) time'):
                    data[cov][rep][tool]['time'] += parse_time(l.split(': ')[-1])
                elif l.startswith('Maximum resident set size'):
                    memory = int(l.split(': ')[-1]) / 1000 # convert KB to MB
                    data[cov][rep][tool]['memory'] = max(data[cov][rep][tool]['memory'], memory)
    print("Parsing reference sequences...")
    refs = dict() # refs[ref] = sequence
    for p in tqdm(list(REFERENCES_PATH.glob('*.fas'))):
        with open(p, 'rt') as f:
            ref, seq = [s.strip() for s in f.read().strip()[1:].splitlines()]
        refs[ref.split()[0]] = seq
    print("Parsing consensus sequences...")
    for p in tqdm(list(RESULTS_PATH.glob('x*.r*.consensus.*.fas'))):
        cov = int(p.name.split('.')[0].lstrip('x'))
        rep = int(p.name.split('.')[1].lstrip('r'))
        tool = p.name.split('.')[-2].strip()
        ref = '.'.join(p.name.split('.')[3:-2])
        if ref not in refs:
            raise ValueError(f"Unknown reference: {p}")
        ref_seq = refs[ref]
        with open(p, 'rt') as f:
            con_seq = ''.join(l.strip() for l in f.read().strip().splitlines()[1:])
        if len(con_seq) == len(ref_seq):
            identity = sum(1 for i in range(len(con_seq)) if con_seq[i] == ref_seq[i]) / len(con_seq)
        else:
            paf_row = run(['minimap2', '-x', 'asm5', REFERENCES_PATH / f'{ref}.fas', p], check=True, capture_output=True).stdout.decode().strip().splitlines()[0].split('\t')
            identity = int(paf_row[9]) / int(paf_row[10])
        data[cov][rep][tool]['accuracy'].append(identity)

    # create figures
    for plot in ['time', 'memory', 'accuracy']:
        print(f"Creating Figure: {plot}")
        fig, ax = plt.subplots(figsize=(10,5)); handles = list()
        for tool in ['ivar', 'viral_consensus', 'mvc']:
            handles.append(Line2D([0],[0],color=COLOR[tool],label=TRANSLATE[tool],linewidth=1.5,linestyle=LINESTYLE[tool]))
            x = list(); y = list()
            for cov in sorted(data.keys()):
                for rep in data[cov].keys():
                    curr_y = data[cov][rep][tool][plot]
                    if isinstance(curr_y, list):
                        x += [cov]*len(curr_y); y += curr_y
                    else:
                        x.append(cov); y.append(curr_y)
            pointplot(x=x, y=y, color=COLOR[tool], linestyles=LINESTYLE[tool])
        plt.xlabel('Coverage')
        plt.ylabel(TRANSLATE[plot])
        ax.set_yscale('log')
        plt.legend(handles=handles,bbox_to_anchor=(0.005, 0.995), loc=2, borderaxespad=0., frameon=True)
        fig.savefig(FIG_PATH / f'{plot}.pdf', format='pdf', bbox_inches='tight')
