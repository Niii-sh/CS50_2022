import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


# load_data这个函数 其实就是把CSV的数据全部转化到names people movies中
# names 为 id对应 name的集合 因为可能存在重名问题
# people 字典(或者说多个对应的hash_map) person_id <-> name birth movies(包含movie_id的集合)
# movies 同理   movie_id <——> title year stars(包含person id的集合)
def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    """
    这里BFS的思路 我觉得还是按照Brian 上课给的那个伪码思路来会比较好 怎么说呢 更有意义些吧
    另外本题中许多使用函数都已经准备好了 还是很不错的 
    Pseudocode:
    1.If the frontier is empty, 
        Stop. There is no solution to the problem
    2.Remove a node from the frontier. This is the node that will be considered.
    3.If the node contains the goal state,
        Return the solution.Stop.
     Else: 
        Expand the node (find all the new nodes that could be reached from this node), and add resulting nodes to the frontier.
        Add the current node to the explored set.
    """
    frontier = QueueFrontier()
    start = Node(state=source, parent=None, action=None)
    frontier.add(start)
    explored = set()

    while True:
        if frontier.empty():
            raise "no solution"
        node = frontier.remove()
        explored.add(node)
        # 遍历该person所在的movie中 所有的person
        for movie_id, person_id in neighbors_for_person(node.state):
            # 符合两个条件则继续对node 进行考虑
            # 1. 当前frontier中 没有该person_id 否则就重复计算了没有必要
            # 2，当前person_id 没有遍历过 否则会导致死循环
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=movie_id)
                # 如果当前节点的person_id == target 说明已经找到了 与 该person共同主演的电影 则生成solution
                if child.state == target:
                    solution = []
                    # 由于 child 的生成中 parent = node 已经定义好了 所以在这里只要顺着parent往下遍历就可以获取路径的值
                    # 最后只需返回 每一步路径中 person_id 到 person_id 的键值对即可
                    while child.parent is not None:
                        solution.append((child.action, child.state))
                        child = child.parent
                    solution.reverse()
                    return solution
                frontier.add(child)
        # 用python写 虽然算法思路是一样的 但代码书写还是和C++ java 有一些区别需要适应一下

def person_id_for_name(name):
    """
    通过id 获取person的信息
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    其实就是遍历 movie集合中所有的person_id 并返回集合
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
