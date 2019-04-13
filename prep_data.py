import clusters
import csv

def readfile(file_name):
    f = open(file_name)
    lines=[line for line in f]
    # First line is the column titles
    colnames = ['ctr'] + lines[0].strip().split(',')[2:-1]
    data={}
    for line in lines[1:]:
        p=line.strip().split(',')
        data[p[1]] = p[2:-1]
    return colnames, data


def fill_missing_val(data):
    new_data = {}
    neighbors_num = 3
    for curctr, v1_all in data.items():
        new_data[curctr] = v1_all
        similarity = {}
        neighbors = []
        if '' in v1_all:
            v2_index = []
            for i in range(len(v1_all)):
                if v1_all[i] != '':
                    v2_index.append(i)
            v1 = [int(v1_all[i]) for i in v2_index]
            for ctr, v2_all in data.items():
                v2 = [v2_all[i] for i in v2_index]
                if '' not in v2 and ctr != curctr:
                    similarity[ctr] = clusters.euclidean(v1, [int(x) for x in v2])
            sorted_similarity = sorted(similarity.items(), key=lambda kv: kv[1])
            for i in range(neighbors_num):
                neighbors.append(data[sorted_similarity[i][0]])
            for i in range(len(neighbors[0])):
                if v1_all[i] == '':
                    total = 0
                    num = 0
                    for j in range(neighbors_num):
                        try:
                            total += int(neighbors[j][i])
                            num += 1
                        except:
                            pass
                    new_data[curctr][i] = float(total)/num
        new_data[curctr] = [int(x) for x in new_data[curctr]]
    return new_data


def clean_data(new_data):
    f = open('country_details.csv')
    lines=[line for line in f]
    # First line is the column titles
    country_names = {}
    for line in lines[1:]:
        p=line.strip().replace('\"', '').split(',')
        country_names[p[0]] = p[1:]
    for key in country_names.keys():
        if len(country_names[key]) == 1:
            if country_names[key] == ['N/A']:
                new_data.pop(key, None)
            else:
                new_data[country_names[key][0]] = new_data.pop(key)
    return new_data


def outputfile(new_data, colnames):
    list = [colnames]
    for key, value in new_data.items():
        list.append([key]+value)
    with open('processed.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(list)
    return


if __name__=='__main__':
    colnames, data = readfile("dataset.csv")
    new_data = fill_missing_val(data)
    outputfile(clean_data(new_data), colnames)
