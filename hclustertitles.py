import clusters
from random import shuffle
import csv
import word_cloud

ctrs,words,data=clusters.readfile('processed.csv')

#create all 9 images
for s in ['min', 'max', 'cen']:
    clust=clusters.hcluster(data,distance=clusters.pearson, inter_dis=s)
    print ('clusters by pearson correlation')
    # clusters.printhclust(clust,labels=ctrs)
    clusters.drawdendrogram(clust,ctrs,jpeg='pearson_'+s+'.jpg')

    clust=clusters.hcluster(data,distance=clusters.euclidean, inter_dis=s)
    print ('clusters by euclidean distance')
    # clusters.printhclust(clust,labels=ctrs)
    clusters.drawdendrogram(clust,ctrs,jpeg='euclidean_'+s+'.jpg')

    clust=clusters.hcluster(data,distance=clusters.cosine, inter_dis=s)
    print ('clusters by cosine similarity')
    # clusters.printhclust(clust,labels=ctrs)
    clusters.drawdendrogram(clust,ctrs,jpeg='cosine_'+s+'.jpg')

#decided that clusters with euclidean distance and max inter distance gives the best result
clust=clusters.hcluster(data,distance=clusters.euclidean, inter_dis="max")
clusters.drawdendrogram(clust,ctrs,jpeg='euclidean_max'+'.jpg')

#cut the cluster at certain level, num can take in values of powers of 2, such as 2, 4, 8, 16. Here I decided that 8 gives the best result
output = clusters.outputhclust(clust,labels=[i for i in range(len(ctrs))], num = 8)


#create word cloud to give descriptive label to each cluster
i = 0
for c in output:
    i += 1
    cen = list(zip(*[data[i] for i in c]))
    cen = [int(sum(cen[k])/len(cen[k])) for k in range(len(cen))]
    print ([ctrs[r] for r in c])
    print(cen)
    word_cloud.count_words(cen, "hcluster " + str(i))


#output clusters for visulization
with open('hcluster_result.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    for i in range(len(output)):
        for num in output[i]:
            writer.writerow([ctrs[num], i+1])

#graph heatmap for cluster validation
shuffle(output)
clusters.cluster_validation(output, data)
