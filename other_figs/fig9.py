import argparse
import os
import pandas as pd
import seaborn as sns
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
import pickle

def smooth(scalars, weight):  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value

    return smoothed

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

#folders = ["../Enero_datasets/dataset_sing_top/data/results_single_top/evalRes_NEW_Garr199905/EVALUATE/"]
folders = ["../Enero_datasets/dataset_sing_top/data/results_single_top/evalRes_NEW_EliBackbone/EVALUATE/","../Enero_datasets/dataset_sing_top/data/results_single_top/evalRes_NEW_Janetbackbone/EVALUATE/","../Enero_datasets/dataset_sing_top/data/results_single_top/evalRes_NEW_HurricaneElectric/EVALUATE/"]

if __name__ == "__main__":
    # This script is to plot the Figures 5 and 6 from COMNET 2022 paper.

    # Before executing this file we must execute the eval_on_single_topology.py file to evaluate the DRL model and store the results
    # We also need to evaluate DEFO for these new topologies. To do this, I copy the corresponding
    # folder where it needs to be and I execute the script run_Defo_single_top.py for each topology.
    # python figures_5_and_6.py -d SP_3top_15_B_NEW

    K15 = "K=15"
    K20 = "K=20"
    K25 = "K=25"
    differentiation_str1 = "Enero_3top_15_B_SAC67"
    differentiation_str2 = "Enero_3top_15_B_SAC49"
    differentiation_str3 = "Enero_3top_15_B_SAC66"

    drl_top1_uti = []
    ls_top1_uti = []
    enero_top1_uti = []
    cost_drl_top1 = []
    cost_ls_top1 = []
    cost_enero_top1 = []

    drl_top2_uti = []
    ls_top2_uti = []
    enero_top2_uti = []
    cost_drl_top2 = []
    cost_ls_top2 = []
    cost_enero_top2 = []

    drl_top3_uti = []
    ls_top3_uti = []
    enero_top3_uti = []
    cost_drl_top3 = []
    cost_ls_top3 = []
    cost_enero_top3 = []


    if not os.path.exists("../Figs"):
        os.makedirs("../Figs")

    path_to_dir = "../Figs/"


    dd_Eli = pd.DataFrame(columns=[K15, K20, K25, 'Topologies'])
    dd_Janet = pd.DataFrame(columns=[K15, K20, K25, 'Topologies'])
    dd_Hurricane = pd.DataFrame(columns=[K15, K20, K25, 'Topologies'])

    # Iterate over all topologies and evaluate our DRL agent on all TMs
    for folder in folders:
        K15_eval_res_folder = folder + differentiation_str1 + '/'
        topology_eval_name = folder.split('NEW_')[1].split('/')[0]
        for subdir, dirs, files in os.walk(K15_eval_res_folder):
            it = 0
            for file in files:
                if file.endswith((".pckl")):
                    results = []
                    path_to_pckl_rewards = K15_eval_res_folder + topology_eval_name + '/'
                    with open(path_to_pckl_rewards+file, 'rb') as f:
                        results = pickle.load(f)
                    if folder==folders[0]:
                        dd_Eli.loc[it] = [results[9],0, 0,topology_eval_name]
                    elif folder==folders[1]:
                        dd_Janet.loc[it] = [results[9],0, 0,topology_eval_name]
                    else:
                        dd_Hurricane.loc[it] = [results[9],0, 0,topology_eval_name]
                    it += 1
        K20_eval_res_folder = folder + differentiation_str2 + '/'
        for subdir, dirs, files in os.walk(K20_eval_res_folder):
            it = 0
            for file in files:
                if file.endswith((".pckl")):
                    results = []
                    path_to_pckl_rewards = K20_eval_res_folder + topology_eval_name + '/'
                    with open(path_to_pckl_rewards+file, 'rb') as f:
                        results = pickle.load(f)
                    if folder==folders[0]:
                        dd_Eli.loc[it, K20] = results[9]
                    elif folder==folders[1]:
                        dd_Janet.loc[it, K20] = results[9]
                    else:
                        dd_Hurricane.loc[it, K20] = results[9]
                    it += 1
        K25_eval_res_folder2 = folder + differentiation_str3 + '/'
        for subdir, dirs, files in os.walk(K25_eval_res_folder):
            it = 0
            for file in files:
                if file.endswith((".pckl")):
                    results = []
                    path_to_pckl_rewards = K25_eval_res_folder2 + topology_eval_name + '/'
                    with open(path_to_pckl_rewards+file, 'rb') as f:
                        results = pickle.load(f)
                    if folder==folders[0]:
                        dd_Eli.loc[it, K25] = results[9]
                    elif folder==folders[1]:
                        dd_Janet.loc[it, K25] = results[9]
                    else:
                        dd_Hurricane.loc[it, K25] = results[9]
                    it += 1

    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['figure.figsize'] = (11.5, 9)
    plt.rcParams['xtick.labelsize'] = 22
    plt.rcParams['ytick.labelsize'] = 22
    plt.rcParams['legend.fontsize'] = 17
    fig, ax = plt.subplots()

    plt.xlim((0, 50.0))
    plt.xticks(np.arange(0, 50, 8))
    plt.tight_layout()


    # Define some hatches
    hatches = cycle(['\\', '-', '|'])
    cdf = pd.concat([dd_Eli,dd_Janet,dd_Hurricane])
    mdf = pd.melt(cdf, id_vars=['Topologies'], var_name=['Topology'])      # MELT
    ax = sns.boxplot(x="Topologies", y="value", hue="Topology", data=mdf, palette="mako")  # RUN PLOT
    plt.rcParams['axes.grid'] = True
    plt.rcParams['figure.figsize'] = (3.47, 2.0)
    plt.rcParams['axes.titlesize'] = 22
    plt.rcParams['xtick.labelsize'] = 22
    plt.rcParams['ytick.labelsize'] = 22
    plt.rcParams['legend.fontsize'] = 20
    ax.set_xlabel("",fontsize=0)
    ax.set_ylabel("Maximum Link Utilization",fontsize=24)
    plt.rcParams["axes.labelweight"] = "bold"
    ax.grid(which='major', axis='y', linestyle='-')
    plt.rcParams.update({'font.size': 22})
    plt.rcParams['pdf.fonttype'] = 42
    # Loop over the bars
    for i, patch in enumerate(ax.artists):
        # Boxes from left to right
        hatch = next(hatches)
        patch.set_hatch(hatch*2)
        col = patch.get_facecolor()
        #patch.set_edgecolor(col)
        patch.set_edgecolor("black")
        patch.set_facecolor('None')

        # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        for j in range(i * 6, i * 6 + 6):
            line = ax.lines[j]
            line.set_color("black")
            line.set_mfc("black")
            line.set_mec("black")
            # Change color of the median
            if j == i*6+4:
                line.set_color("orange")
                line.set_mfc("orange")
                line.set_mec("orange")

    for i, patch in enumerate(ax.patches):
        hatch = next(hatches)
        patch.set_hatch(hatch*2)
        col = patch.get_facecolor()
        #patch.set_edgecolor(col)
        patch.set_edgecolor("black")
        patch.set_facecolor('None')
    plt.legend(loc='upper left', ncol=3)
    plt.ylim((0.5, 1.35))
    plt.tight_layout()
    plt.savefig(path_to_dir+'fig9.png', bbox_inches='tight',pad_inches = 0)
    plt.clf()
    plt.close()
