import json

def convert_to_json(regions, filename):
    f = open(filename + '.csv')
    lines=[line for line in f]
    clusters = {}
    for line in lines[1:]:
        p=line.strip().replace('\"', '').split(',')
        clusters[p[0]] = p[1:]

    all_countries = {}
    for key, value in clusters.items():
        if key in regions.keys():
            for item in regions[key]:
                if item not in clusters.keys():
                    all_countries[item] = int(value[0])
        else:
            all_countries[key] = int(value[0])

    output = [["Country", "Cluster"]]
    for key, value in all_countries.items():
        output.append([key, value])

    with open(filename + ".js", 'w') as outfile:
        outfile.write("var "+filename[0]+"data = ")
        json.dump(output, outfile)


if __name__=='__main__':
    f = open('country_details.csv')
    lines=[line for line in f]
    regions = {}
    for line in lines[1:]:
        p=line.strip().replace('\"', '').split(',')
        if len(p) > 2:
            regions[p[0]] = p[1:]
    convert_to_json(regions, 'kcluster_result')
    convert_to_json(regions, 'hcluster_result')
