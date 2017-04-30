from pprint import pprint

def topolgical_sort(graph_unsorted):
    graph_sorted = []
    graph_unsorted = dict(graph_unsorted)
    while graph_unsorted:
        acyclic = False
        for node, edges in list(graph_unsorted.items()):
            for edge in edges:
                if edge in graph_unsorted:
                    break
            else:
                acyclic = True
                del graph_unsorted[node]
                graph_sorted.append((node, edges))
        if not acyclic:
            raise RuntimeError("A cyclic dependency occurred")
    return graph_sorted

# filep = open("dummytac.txt")
# data = filep.readlines()


def removejumps(data):
    labelmap = {}
    revmap = {}
    index = 0
    for line in data:
        if "label:" in line:
            labelmap[line.split(' ')[1]] = index
            # revmap[index+1] = line.split(' ')[1]
        index += 1

    graph_unsorted = []
    graphdict = {}
    jumps = ['jump', 'je', 'jle', 'jge', 'jl', 'jg', 'goto']
    index = 0
    for line in data:
        if any(ji in line for ji in jumps):
            if( 'jump' in data[ labelmap[line.split(' ')[1]] + 1] or 'goto' in data[ labelmap[line.split(' ')[1]] + 1]):
                # print "note ",  labelmap[line.split(' ')[1]]+ 1, " " , index
                try:
                    graphdict[labelmap[line.split(' ')[1]]+ 1]
                    graphdict[labelmap[line.split(' ')[1]]+ 1].append(index)
                except:
                    graphdict[labelmap[line.split(' ')[1]]+ 1] = [index]
        index += 1
    for key in graphdict:
        graph_unsorted.append((key,graphdict[key]))

    graph_sorted = topolgical_sort( graph_unsorted)


    for (src,dest) in reversed(graph_sorted):
        for node in dest:
            line = data[node ].split(' ')
            line[1] = data[src].split(' ')[1]
            data[node] = ' '.join(line)

    # finaldata = ''.join(data)
    return data
    # filew = open("correcttac.txt", "w")
    # filew.write(finaldata)
# print removejumps(data)