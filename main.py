import vk_api
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import time
start_time = time.time()

access_token = 'vk1.a.AEAygR6PdYUaDeLqDAhUjcj6pucYbJQB9QJaQhBP78CNT6J9QjbAeAL9p7DVccsYEqUqKXdhRLsvzgxtVeWNIFYBqIc-G7VK4yuCyvEiuG7ovBVKGbiSzJvF2fBo1cT3M--HZfZaEosNa4auvgrNdHNlleKswN2gI8TH7kd0YtdbZBavTcGiGymAIEBJi3ciT-ZhJdMMyplpSsPYZuI1mw'

group_ids = [308412461, 232210943, 209834587, 45745684, 513083713, 606396724, 188959578, 275549140, 412981588]


try:
    vk_session = vk_api.VkApi(token=access_token)
except Exception as error:
    print(error)

vk = vk_session.get_api()

G = nx.Graph()
users_id = []
friends = {}

def find_friends(id, deep):
    users_id.append(id)
    while deep > 0:
        try:
            users = vk.friends.get(user_id=id, fields='deactivated,is_closed', count=10)
            friends[id] = users
            deep -= 1
            for k in users['items']:
                G.add_edge(id, k['id'])
                if 'deactivated' in k or k['is_closed']:
                    users['items'].remove(k)
                else:
                    find_friends(k['id'], deep)
        except:
            return 

for id in group_ids:
    find_friends(id, 3)

for user in users_id:
    for k in friends:
        for i in friends[k]['items']:
            if user == i['id']:
                G.add_edge(user, k)




color_map = []
for node in G:
    if node in group_ids:
        color_map.append('blue')
    else:
        color_map.append('red')
nx.draw_spring(G, with_labels=False, node_color=color_map, node_size=100)
plt.savefig('result.png')
plt.show()

with open("result.txt", "a") as file:
    nodes = list(nx.betweenness_centrality(G).items())
    print('Центральность по посредничеству: ', file=file)
    for n in nodes:
        for g in group_ids:
            if n[0] == g:
                print(n, file=file)

    nodes = list(nx.closeness_centrality(G).items())
    print('Центральность по близости: ', file=file)
    for n in nodes:
        for g in group_ids:
            if n[0] == g:
                print(n, file=file)

    nodes = list(nx.eigenvector_centrality(G).items())
    print('Центральность по собственному значению: ', file=file)
    for n in nodes:
        for g in group_ids:
            if n[0] == g:
                print(n, file=file)


print("--- %s seconds ---" % (time.time() - start_time))