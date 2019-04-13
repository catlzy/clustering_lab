from PIL import Image,ImageDraw
from math import *
import random
import matplotlib.pyplot as plt

def readfile(file_name):
    f = open(file_name)
    lines=[line for line in f]

    # First line is the column titles
    colnames=lines[0].strip().split(',')[:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split(',')
        # First column in each row is the rowname
        if len(p)>1:
            rownames.append(p[0])
            # The data for this row is the remainder of the row
            data.append([float(x) for x in p[1:]])
    return rownames,colnames,data


def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])):
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def print_2d_array(matrix):
    for i in range(len(matrix)):
        for j in range (len(matrix[i])):
            print (matrix[i][j], end = "")
        print('\n')


# different similarity metrics for 2 vectors
def manhattan(v1,v2):
    res=0
    dimensions=min(len(v1),len(v2))

    for i in range(dimensions):
        res+=abs(v1[i]-v2[i])

    return res


def euclidean(v1,v2):
    res=0
    dimensions=min(len(v1),len(v2))
    for i in range(dimensions):
        res+=pow(abs(v1[i]-v2[i]),2)

    return sqrt(float(res))


def cosine(v1,v2):
    dotproduct=0
    dimensions=min(len(v1),len(v2))

    for i in range(dimensions):
        dotproduct+=v1[i]*v2[i]

    v1len=0
    v2len=0
    for i in range (dimensions):
        v1len+=v1[i]*v1[i]
        v2len+=v2[i]*v2[i]

    v1len=sqrt(v1len)
    v2len=sqrt(v2len)
    return 1.0-(float(dotproduct)/(v1len*v2len))


def pearson(v1,v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)

    # Sums of the squares
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])

    # Sum of the products
    pSum=sum([v1[i]*v2[i] for i in range(min(len(v1),len(v2)))])

    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 1.0

    return 1.0-num/den


def tanimoto(v1,v2):
    c1,c2,shr=0,0,0

    for i in range(len(v1)):
        if v1[i]!=0: c1+=1 # in v1
        if v2[i]!=0: c2+=1 # in v2
        if v1[i]!=0 and v2[i]!=0: shr+=1 # in both

    return 1.0-(float(shr)/(c1+c2-shr))


def cluster_validation(clust, ori_data):
    data = []
    for i in range(len(clust)):
        for r in clust[i]:
            data.append(ori_data[r])
    distance_matrix = [[0 for _ in range(len(data))] for _ in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            distance_matrix[i][j] = euclidean(data[i], data[j])
    plt.imshow(distance_matrix)
    plt.colorbar(orientation='vertical')
    plt.show()


# Hierarchical clustering
class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance


def hcluster(rows,distance=euclidean, inter_dis = 'cen'):
    distances={}
    currentclustid=-1

    # Clusters are initially just the rows
    clust=[bicluster([rows[i]],id=i) for i in range(len(rows))]

    while len(clust)>1:
        lowestpair=(0,0)
        closest = float("inf")
        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id,clust[j].id) not in distances:
                    if inter_dis == "min":
                        distances[(clust[i].id,clust[j].id)]=min(distance(c1, c2) for c1 in clust[i].vec for c2 in clust[j].vec)
                    if inter_dis == "max":
                        distances[(clust[i].id,clust[j].id)]=max(distance(c1, c2) for c1 in clust[i].vec for c2 in clust[j].vec)
                    if inter_dis == "cen":
                        c1 = list(zip(*clust[i].vec))
                        c1 = [sum(c1[k])/float(len(c1[k])) for k in range(len(c1))]
                        c2 = list(zip(*clust[j].vec))
                        c2 = [sum(c2[k])/float(len(c2[k])) for k in range(len(c2))]
                        distances[(clust[i].id,clust[j].id)]=distance(c1, c2)

                d=distances[(clust[i].id,clust[j].id)]
                if d<closest:
                    closest=d
                    lowestpair=(i,j)

        # # calculate the average of the two clusters
        # mergevec=[
        #     (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
        #             for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster=bicluster(clust[lowestpair[0]].vec+clust[lowestpair[1]].vec,left=clust[lowestpair[0]],
                             right=clust[lowestpair[1]],
                             distance=closest,id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printhclust(clust,labels=None,n=0):
    # indent to make a hierarchy layout
    for i in range(n):
        print (' ', end="")
    if clust.id<0:
    # negative id means that this is branch
        print ('-')
    else:
    # positive id means that this is an endpoint
        if labels==None: print (clust.id)
        else: print (labels[clust.id])

    # now print the right and left branches
    if clust.left!=None: printhclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printhclust(clust.right,labels=labels,n=n+1)


def outputhclust(clust,labels=None,n=0, num = 8):
    output = [clust]
    while(len(output) != num):
        temp = []
        for c in output:
            temp.append(c.left)
            temp.append(c.right)
        output = temp[:]
    for i in range(len(output)):
        output[i] = traverseclust(output[i], labels)
    return output

def traverseclust(clust, labels):
    if clust!= None and clust.id >= 0:
        return [labels[clust.id]]
    return traverseclust(clust.left, labels) + traverseclust(clust.right, labels)



# draw hierarchical clusters
def getheight(clust):
    # Is this an endpoint? Then the height is just 1
    if clust.left==None and clust.right==None: return 1

    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left)+getheight(clust.right)


def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left==None and clust.right==None: return 0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance


def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    # height and width
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)

    # width is fixed, so scale distances accordingly
    scaling=float(w-150)/depth

    # Create a new image with a white background
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    # Draw the first node
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')


def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        # Line length
        ll=clust.distance*scaling
        # Vertical line from this cluster to children
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        # Horizontal line to left item
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        # Horizontal line to right item
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        # Call the function to draw the left and right nodes
        drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x+5,y-7),labels[clust.id],(0,0,0))


# k-means clustering
def kcluster(rows,distance=euclidean,k=4):
    # Determine the minimum and maximum values for each point
    ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
    for i in range(len(rows[0]))]

    # Create k randomly placed centroids
    clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
    for i in range(len(rows[0]))] for j in range(k)]

    lastmatches=None
    bestmatches = None

    for t in range(100):
        print ('Iteration %d' % t)
        bestmatches=[[] for i in range(k)]

        # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            for i in range(k):
                d=distance(clusters[i],row)
                if d<distance(clusters[bestmatch],row): bestmatch=i
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches==lastmatches: break
        lastmatches=bestmatches

        # Move the centroids to the average of their members
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs

    return bestmatches

def bisecting_kmean(rows,distance=euclidean,k=4, trials=50):
    data = rows[:]
    total_clust = [[i for i in range(len(rows))]]
    for i in range(1, k):
        sse = 0
        remove = total_clust[0]
        for c in total_clust:
            cursse = calculate_sse([c], data)
            if cursse > sse:
                remove = c
                sse = cursse
        total_clust.remove(remove)
        sse = float("inf")
        clust = []
        for t in range(trials):
            curclust = kcluster([data[r] for r in remove],distance,2)
            for j in range(len(curclust)):
                curclust[j] = [remove[k] for k in curclust[j]]
            cursse = calculate_sse(curclust, data)
            if sse > cursse:
                sse = cursse
                clust = curclust
        for c in clust:
            total_clust.append(c)
    return total_clust


def calculate_sse(clust, data):
    total_sse = 0
    data_clust = []
    for i in range(len(clust)):
        data_clust.append([data[r] for r in clust[i]])
    for i in range(len(data_clust)):
        ind_sse = 0
        data_by_col = list(zip(*data_clust[i]))
        for j in range(len(data_by_col)):
            mean = sum(data_by_col[j])/float(len(data_by_col[j]))
            for k in range(len(data_by_col[j])):
                ind_sse += (data_by_col[j][k]-mean)**2
        total_sse += ind_sse
    return total_sse


def scaledown(data,distance=pearson,rate=0.01):
    n=len(data)

    # The real distances between every pair of items
    realdist=[[distance(data[i],data[j]) for j in range(n)]
             for i in range(0,n)]

    # Randomly initialize the starting points of the locations in 2D
    loc=[[random.random(),random.random()] for i in range(n)]
    fakedist=[[0.0 for j in range(n)] for i in range(n)]

    lasterror=None
    for m in range(0,1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2)
                                 for x in range(len(loc[i]))]))

        # Move points
        grad=[[0.0,0.0] for i in range(n)]

        totalerror=0
        for k in range(n):
            for j in range(n):
                if j==k: continue
                # The error is percent difference between the distances
                errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]

                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
                grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm

                # Keep track of the total error
                totalerror+=abs(errorterm)
        print ("Total error:",totalerror)

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror<totalerror: break
        lasterror=totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            loc[k][0]-=rate*grad[k][0]
            loc[k][1]-=rate*grad[k][1]

    return loc


def draw2d(data,labels,jpeg='mds2d.jpg'):
    img=Image.new('RGB',(2000,2000),(255,255,255))
    draw=ImageDraw.Draw(img)
    for i in range(len(data)):
        x=(data[i][0]+0.5)*1000
        y=(data[i][1]+0.5)*1000
        draw.text((x,y),labels[i],(0,0,0))
    img.save(jpeg,'JPEG')
