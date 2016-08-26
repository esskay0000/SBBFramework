import pylab as plt
import json
import numpy
import matplotlib.patches as mpatches

def round_value(value, round_decimals_to = 4):
    number = float(10**round_decimals_to)
    return int(value * number) / number

# filename = 'properties_per_team__sbb_trained_against_bayesian_vs_bayesian_opponent__1260_balanced_points.json'
# filename2 = 'properties_per_team__sbb_trained_against_bayesian_vs_bayesian_opponent__1260_unbalanced_points.json'

blah = "ncd_and_genotype"
filename = 'genotype_vs_ncd/'+blah+'/properties_per_team_'+blah+'_with_profiling__balanced.json'
filename2 = 'genotype_vs_ncd/'+blah+'/properties_per_team_'+blah+'_with_profiling__unbalanced.json'

with open(filename) as data_file:    
    data = json.load(data_file)
all_teams = []
for value in data.values():
    all_teams += value

with open(filename2) as data_file:    
    data = json.load(data_file)
all_teams2 = []
for value in data.values():
    all_teams2 += value

x = []
y = []

x2 = []
y2 = []

for value in all_teams:

    x.append(value.values()[0]['properties']['passive_aggressive'])
    y.append(value.values()[0]['properties']['tight_loose'])

for value in all_teams2:

    x2.append(value.values()[0]['properties']['passive_aggressive'])
    y2.append(value.values()[0]['properties']['tight_loose'])


plt.grid(b=True, which='both', color='0.65',linestyle='-')

patches = []



plt.xlabel('passive/aggressive')
plt.ylabel('tight/loose')

plt.axis([-0.05, 1.05, -0.05, 1.05])

# red_dot, = plt.plot(x2, y2,'bo',markersize=3.0) #, alpha=0.2)
# patches.append(mpatches.Patch(color='b', marker='o', label='unbalanced'))

# white_cross, = plt.plot(x, y,'rx',markersize=3.0) #, alpha=0.2)
# patches.append(mpatches.Patch(color='r', marker='x', label='balanced'))

# plt.legend(handles=patches, loc=3)
# plt.legend([red_dot, white_cross], ["unbalanced", "balanced"])

plt.scatter(x2, y2, c='b',marker='o', label='unbalanced')
plt.scatter(x, y, c='r',marker='x', label='balanced')
plt.legend()

largura = 4
temp1 = round_value(numpy.mean(x))
plt.plot([temp1, temp1], [-100, 700], 'k-', lw=largura, color='red', linestyle='--')
temp2 = round_value(numpy.mean(x2))
plt.plot([temp2, temp2], [-100, 700], 'k-', lw=largura, color='blue', linestyle='--')

temp1 = round_value(numpy.mean(y))
plt.plot([-100, 700], [temp1, temp1], 'k-', lw=largura, color='red', linestyle='--')
temp2 = round_value(numpy.mean(y2))
plt.plot([-100, 700], [temp2, temp2], 'k-', lw=largura, color='blue', linestyle='--')

# temp1 = round_value(numpy.mean(y))
# plt.plot([0, 700], [temp1, temp1], 'k-', lw=2, color='red', linestyle='--')
# temp2 = round_value(numpy.mean(y2))
# plt.plot([0, 700], [temp2, temp2], 'k-', lw=2, color='blue', linestyle='--')


# %Properties (balanced)
# %- passive_aggressive: 0.4641
# %- agressiveness: 0.4875
# %- tight_loose: 0.6488
# %- bluffing: 0.1345
# %- normalized_result_mean: 0.4854
# %
# %Properties (unbalanced)
# %- passive_aggressive: 0.4565
# %- agressiveness: 0.3957
# %- tight_loose: 0.4969
# %- bluffing: 0.3298
# %- normalized_result_mean: 0.5055


# plt.show()
# plt.savefig("with_metrics_no_profiling__"+metric_name+'_vs_score_for_unbalanced_and_balanced_points.png', bbox_inches='tight')
plt.savefig("behaviors.pdf", bbox_inches='tight')