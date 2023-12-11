import vk_api
import networkx as nx
import matplotlib.pyplot as plt
import time
start_time = time.time()


access_token = 'vk1.a.AEAygR6PdYUaDeLqDAhUjcj6pucYbJQB9QJaQhBP78CNT6J9QjbAeAL9p7DVccsYEqUqKXdhRLsvzgxtVeWNIFYBqIc-G7VK4yuCyvEiuG7ovBVKGbiSzJvF2fBo1cT3M--HZfZaEosNa4auvgrNdHNlleKswN2gI8TH7kd0YtdbZBavTcGiGymAIEBJi3ciT-ZhJdMMyplpSsPYZuI1mw'

group_ids = []


try:
    vk_session = vk_api.VkApi(token=access_token)
except Exception as error:
    print(error)

vk = vk_session.get_api()

G = nx.Graph()

with open("source_id.txt", "r") as file:
    while line := file.readline():
        group_ids.append(line.rstrip())


def find_friends(id, deep):
    G.add_node(id)
    while deep > 0:
        users = vk.friends.get(user_id=id, fields='deactivated,is_closed', count=10)
        deep -= 1
        for k in users['items']:
            G.add_edge(id, k['id'])
            if 'deactivated' in k or k['is_closed']:
                users['items'].remove(k)
            else:
                find_friends(k['id'], deep)

for id in group_ids:
    find_friends(id, 3)
print("VK done")


plt.figure(num=None, figsize=(40, 20), dpi=100)
nx.draw(G, with_labels=False, node_color='red', node_size=50)
print("Draw1 fine")
ax = plt.gca()
ax.collections[0].set_edgecolor("#000000")
plt.savefig('result.png')
plt.show()

print("Draw2 fine")

with open("result.txt", "w") as file:
    print('\nЦентральность по близости: ', file=file)
    for g in group_ids:
        nodes = nx.closeness_centrality(G, u=g)
        print(vk.users.get(user_id=g)[0]['first_name'], vk.users.get(user_id=g)[0]['last_name'], nodes, file=file)

    nodes = nx.betweenness_centrality(G,k=100)
    print('Центральность по посредничеству: ', file=file)
    for g in group_ids:
        print(vk.users.get(user_id=g)[0]['first_name'], vk.users.get(user_id=g)[0]['last_name'], nodes[g], file=file)

    nodes = nx.eigenvector_centrality(G, max_iter=20)
    print('\nЦентральность по собственному значению: ', file=file)
    for g in group_ids:
        print(vk.users.get(user_id=g)[0]['first_name'], vk.users.get(user_id=g)[0]['last_name'], nodes[g], file=file)

    print("\n\n%s seconds" % (time.time() - start_time), file=file)
    print("Количество вершин ", G.number_of_nodes(), file=file)
    print("Количество ребер ", G.number_of_edges(), file=file)

print("%s seconds" % (time.time() - start_time))