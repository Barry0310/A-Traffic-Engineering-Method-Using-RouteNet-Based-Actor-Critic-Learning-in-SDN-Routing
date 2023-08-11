import networkx
import itertools
import gym_graph
import gym
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

root = "../Figs"

if not os.path.exists(root):
    os.makedirs(root)

directory = "../Figs/topology"

if not os.path.exists(directory):
    os.makedirs(directory)

ENV_NAME = 'GraphEnv-v16'
dataset_root_folder = "../Enero_datasets/dataset_sing_top/data/results_my_3_tops_unif_05-1/"
dataset_folder_name1 = dataset_root_folder + "NEW_BtAsiaPac"
dataset_folder_name2 = dataset_root_folder + "NEW_Garr199905"
dataset_folder_name3 = dataset_root_folder + "NEW_Goodnet"
dataset_folder_name4 = dataset_root_folder + "NEW_EliBackbone"
dataset_folder_name5 = dataset_root_folder + "NEW_Janetbackbone"
dataset_folder_name6 = dataset_root_folder + "NEW_HurricaneElectric"
take_critic_demands = True
SEED = 9
percentage_demands = 15


env_training1 = gym.make(ENV_NAME)
env_training1.seed(SEED)
env_training1.generate_environment(dataset_folder_name1 + "/TRAIN", "BtAsiaPac", 0, 100, percentage_demands)
env_training1.top_K_critical_demands = take_critic_demands

env_training2 = gym.make(ENV_NAME)
env_training2.seed(SEED)
env_training2.generate_environment(dataset_folder_name2 + "/TRAIN", "Garr199905", 0, 100, percentage_demands)
env_training2.top_K_critical_demands = take_critic_demands

env_training3 = gym.make(ENV_NAME)
env_training3.seed(SEED)
env_training3.generate_environment(dataset_folder_name3 + "/TRAIN", "Goodnet", 0, 100, percentage_demands)
env_training3.top_K_critical_demands = take_critic_demands

env_training = [env_training1, env_training2, env_training3]

env_training4 = gym.make(ENV_NAME)
env_training4.seed(SEED)
env_training4.generate_environment(dataset_folder_name4 + "/TRAIN", "EliBackbone", 0, 100, percentage_demands)
env_training4.top_K_critical_demands = take_critic_demands

env_training5 = gym.make(ENV_NAME)
env_training5.seed(SEED)
env_training5.generate_environment(dataset_folder_name5 + "/TRAIN", "Janetbackbone", 0, 100, percentage_demands)
env_training5.top_K_critical_demands = take_critic_demands

env_training6 = gym.make(ENV_NAME)
env_training6.seed(SEED)
env_training6.generate_environment(dataset_folder_name6 + "/TRAIN", "HurricaneElectric", 0, 100, percentage_demands)
env_training6.top_K_critical_demands = take_critic_demands

env_eval = [env_training4, env_training5, env_training6]

for env in env_training:
    D = networkx.DiGraph()
    for u, v in env.graph.edges():
        if not D.has_edge(u, v):
            D.add_edge(u, v)
    degree = []
    for n in env.graph.nodes():
        degree.append(env.graph.degree[n])
    simp = []
    for n1 in env.graph.nodes():
        for n2 in env.graph.nodes():
            if n1 != n2:
                count = 0
                for m in env.src_dst_k_middlepoints[str(n1) + ':' + str(n2)]:
                    path = env.shortest_paths[n1, m].copy()
                    if m != n2:
                        path += env.shortest_paths[m, n2][1:].copy()
                    if networkx.is_simple_path(D, path):
                        count += 1
                simp.append(count / len(env.src_dst_k_middlepoints[str(n1) + ':' + str(n2)]))
    print(env.graph_topology_name)
    path = []
    print('degree', min(degree), max(degree), sum(degree)/len(degree), np.std(degree))
    ebb = networkx.edge_betweenness_centrality(D)
    eb = [e for e in ebb.values()]
    print('edge betweenness', np.around(min(eb), 4), np.around(max(eb), 4), np.around(sum(eb)/len(eb), 4), np.around(np.std(eb), 4))
    print('simple rate', sum(simp) / len(simp))
    print('average clustering coefficient', networkx.average_clustering(D))
    ce = [c for n, c in networkx.degree_centrality(D).items()]
    print('centrality', np.average(ce))
    print('diameter', networkx.diameter(D))
    plt.clf()
    pos = networkx.spring_layout(env.graph, k=4)
    networkx.draw(env.graph, pos, with_labels=True)
    plt.savefig(directory+'/'+env.graph_topology_name+'.png')
    print()

for env in env_eval:
    D = networkx.DiGraph()
    for u, v in env.graph.edges():
        if not D.has_edge(u, v):
            D.add_edge(u, v)
    degree = []
    for n in env.graph.nodes():
        degree.append(env.graph.degree[n])
    simp = []
    for n1 in env.graph.nodes():
        for n2 in env.graph.nodes():
            if n1!=n2:
                count = 0
                for m in env.src_dst_k_middlepoints[str(n1)+':'+str(n2)]:
                    path = env.shortest_paths[n1,m].copy()
                    if m!=n2:
                        path += env.shortest_paths[m,n2][1:].copy()
                    if networkx.is_simple_path(D, path):
                        count+=1
                simp.append(count/len(env.src_dst_k_middlepoints[str(n1)+':'+str(n2)]))
    print(env.graph_topology_name)
    print('degree', min(degree), max(degree), sum(degree)/len(degree), np.std(degree))
    ebb = networkx.edge_betweenness_centrality(D)
    eb = [e for e in ebb.values()]
    print('edge betweenness',np.around(min(eb), 4), np.around(max(eb), 4), np.around(sum(eb)/len(eb), 4), np.around(np.std(eb), 4))
    print('simple rate', sum(simp)/len(simp))
    print('average clustering coefficient', networkx.average_clustering(D))
    ce = [c for n, c in networkx.degree_centrality(D).items()]
    print('centrality', np.average(ce))
    print('diameter', networkx.diameter(D))

    plt.clf()
    pos = networkx.spring_layout(env.graph, k=4)
    networkx.draw(env.graph, pos, with_labels=True)
    plt.savefig(directory + '/' + env.graph_topology_name + '.png')
    print()

rel = ['Compuserve', 'Biznet', 'Darkstrand', 'Arpanet19728', 'Geant2001', 'Renater2001', 'Janetbackbone', 'Renater2004']
dataset_root_folder = "../Enero_datasets/results-1-link_capacity-unif-05-1/results_zoo/"
for r in rel:
    env = gym.make(ENV_NAME)
    env.seed(SEED)
    env.generate_environment(dataset_root_folder + r, r, 0, 100, percentage_demands)
    env.top_K_critical_demands = take_critic_demands
    for u, v in env.graph.edges():
        if not D.has_edge(u, v):
            D.add_edge(u, v)
    degree = []
    for n in env.graph.nodes():
        degree.append(env.graph.degree[n])
    print(env.graph_topology_name)
    print('degree', min(degree), max(degree), sum(degree) / len(degree), np.std(degree))
    ebb = networkx.edge_betweenness_centrality(D)
    eb = [e for e in ebb.values()]
    print('edge betweenness', np.around(min(eb), 4), np.around(max(eb), 4), np.around(sum(eb) / len(eb), 4),
          np.around(np.std(eb), 4))
    print('average clustering coefficient', networkx.average_clustering(D))
    ce = [c for n, c in networkx.degree_centrality(D).items()]
    print('centrality', np.average(ce))
    #plt.clf()
    #pos = networkx.spring_layout(env.graph, k=4)
    #networkx.draw(env.graph, pos, with_labels=True)
    #plt.savefig(directory + '/' + env.graph_topology_name + '.png')
    print()

# import networkx as nx
#
# # 创建一个多重有向图
# G = nx.MultiDiGraph()
#
# # 添加节点和边
# G.add_nodes_from([1, 2, 3, 4])
# G.add_edges_from([(1, 2), (2, 1), (2, 3), (3, 4), (3, 2), (4, 3)])
#
# # 将多重有向图转换为有向图
# D = nx.DiGraph()
# for u, v, k in G.edges(keys=True):
#     if not D.has_edge(u, v):
#         D.add_edge(u, v, weight=0.0)
#     D[u][v]['weight'] += G[u][v][k].get('weight', 1.0)
#
# # 计算betweenness centrality
# betweenness = nx.algorithms.centrality.betweenness_centrality(D)
#
# # 打印结果
# print(betweenness)
