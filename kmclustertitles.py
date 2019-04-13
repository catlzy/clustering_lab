import clusters
import matplotlib.pyplot as plt
from numpy import *
import csv
import word_cloud

if __name__=='__main__':
    ctrs,attributes,data=clusters.readfile('processed.csv')

    # create SSE graph
    bi_sse = []
    for i in range(1, 21):
        num_clusters=i
        print('Searching for {} clusters by bisecting kmean with euclidean:'.format(num_clusters))
        clust = clusters.bisecting_kmean(data, distance = clusters.euclidean, k = num_clusters, trials = 50)
        bi_sse.append(clusters.calculate_sse(clust, data))

    pearson_sse = []
    for i in range(1, 21):
        num_clusters=i
        clust=clusters.kcluster(data,distance=clusters.pearson,k=num_clusters)
        print('Searching for {} clusters by pearson correlation:'.format(num_clusters))
        # for i in range(num_clusters):
        #     print ('cluster {}:'.format(i+1))
        #     print ([ctrs[r] for r in clust[i]])
        pearson_sse.append(clusters.calculate_sse(clust, data))

    euclidean_sse = []
    for j in range(1, 21):
        num_clusters=j
        clust=clusters.kcluster(data,distance=clusters.euclidean,k=num_clusters)
        print('Searching for {} clusters by euclidean distance:'.format(num_clusters))
        # for i in range(num_clusters):
        #     print ('cluster {}:'.format(i+1))
        #     print ([ctrs[r] for r in clust[i]])
        euclidean_sse.append(clusters.calculate_sse(clust, data))

    cosine_sse = []
    for j in range(1, 21):
        num_clusters=j
        clust=clusters.kcluster(data,distance=clusters.cosine,k=num_clusters)
        print('Searching for {} clusters by cosine distance:'.format(num_clusters))
        # for i in range(num_clusters):
        #     print ('cluster {}:'.format(i+1))
        #     print ([ctrs[r] for r in clust[i]])
        cosine_sse.append(clusters.calculate_sse(clust, data))

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    ax.set_title('SSE for Different Distance Metrics')
    plt.plot([i+1 for i in range(20)], bi_sse, label='bisecting euclidean')
    plt.plot([i+1 for i in range(20)], pearson_sse, label='pearson')
    plt.plot([i+1 for i in range(20)], euclidean_sse, label='euclidean')
    plt.plot([i+1 for i in range(20)], cosine_sse, label='cosine')
    plt.xticks([i+1 for i in range(20)])
    ax.set_xlabel('Cluster Num')
    ax.set_ylabel('SSE')
    ax.legend(loc='best')
    plt.show()


    #discovered that bisecting k-means with k=6 gives relatively good results
    clust = clusters.bisecting_kmean(data, distance = clusters.euclidean, k = 6, trials = 50)

    #graph heatmap to validate cluster
    clusters.cluster_validation(clust, data)

    #output cluster results for visulization in world map
    with open('kcluster_result.csv', 'w') as output:
        writer = csv.writer(output, delimiter=',')
        for i in range(len(clust)):
            for num in clust[i]:
                writer.writerow([ctrs[num], i+1])

    #create word cloud to give descriptive label to each cluster
    i = 0
    for c in clust:
        i += 1
        cen = list(zip(*[data[i] for i in c]))
        cen = [int(sum(cen[k])/len(cen[k])) for k in range(len(cen))]
        print ([ctrs[r] for r in c])
        print(cen)
        word_cloud.count_words(cen, "cluster " + str(i))
