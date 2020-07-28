import json
import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn import metrics
from sklearn.cluster import DBSCAN
import sklearn.utils
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from celluloid import Camera
import time
import threading

def draw(x, y):
    global is_plot
    while is_plot:
        plt.figure(1)
        plt.cla()
        plt.ylim(-9000, 9000)
        plt.xlim(-9000, 9000)
        plt.scatter(x, y, c='r', s=8)
        plt.pause(0.001)
    plt.close("all")

def dbscan(x, y, plt):
    X = np.stack([x, y], axis=1)

    XS = StandardScaler().fit_transform(X)
    # print(X)
    db = DBSCAN(eps=0.13, min_samples=4).fit(XS)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    # print(core_samples_mask)
    core_samples_mask[db.core_sample_indices_] = True
    # print(core_samples_mask)
    labels = db.labels_
    #print(labels)

    #Number of clusters in labels, ignoring noise if present
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    #print('Estimated number of clusters: %d' % n_clusters_)
    #print('Estimated number of noise points: %d' % n_noise_)
    #print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    #print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
    #print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    #print("Adjusted Rand Index: %0.3f"
    #      % metrics.adjusted_rand_score(labels_true, labels))
    #print("Adjusted Mutual Information: %0.3f"
    #      % metrics.adjusted_mutual_info_score(labels_true, labels))
    #print("Silhouette Coefficient: %0.3f"
    #      % metrics.silhouette_score(X, labels))

    # plt.ylim(-4000, 8000)
    # plt.xlim(-4000, 4000)
    # plt.scatter(x, y, c='r', s=1)
    # plt.show()

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0,1,len(unique_labels))]
    plt.ylim(-4000, 8000)
    plt.xlim(-4000, 4000)
    plt.scatter(X[:, 0], X[:, 1], c='r', s=1)

    for k, col in zip(unique_labels, colors):
        if k == -1:
            col=[0,0,0,1]
        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

        xy = X[class_member_mask & ~core_samples_mask]
        #plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
        #         markeredgecolor='k', markersize=2)

    #plt.title('Estimated number of clusters: %d' % n_clusters_)
    #plt.show()
    camera.snap()

is_plot = True
x = []
y = []

for _ in range(430):
    x.append(0)
    y.append(0)

with open("/Users/soobinjeon/Developments/AD/LidarTracker/Data/data_2.json", "r") as st_json:
    ldata = json.load(st_json)

    cnt = 0
    prevsf = 0
    startTimestamp = 0

    camera = Camera(plt.figure())

    ischecked = False
    inputdata = []
    for data in ldata['rawdata']:
        if startTimestamp == 0:
            startTimestamp = data['timestamp']
        ctimestamp = data['timestamp']
        tgap = ctimestamp - startTimestamp

        if tgap > 3.0 and data['start_flag'] == True and cnt != 0:
            gap = cnt - prevsf
            #print(cnt, gap, data)
            prevsf = cnt
            if ischecked == False:
                ischecked = True
            else:
                ischecked = False

                cnt = 0
                for data in inputdata:
                    x[cnt] = data['distance'] * math.cos(math.radians(90-data['angle']))
                    y[cnt] = data['distance'] * math.sin(math.radians(90-data['angle']))
                    #print(x[cnt], y[cnt])
                    cnt += 1
                dbscan(x,y, plt)

                #print("Draw Graph",cnt)
                #plt.ylim(-4000, 8000)
                #plt.xlim(-4000, 4000)
                #plt.scatter(x, y, c='r', s=1)
                #plt.show()
 #               camera.snap()

                inputdata.clear()
                #break

        if ischecked:
            inputdata.append(data)

        cnt += 1

    print(len(inputdata))

   # threading.Thread(target=draw).start()
    print("Make movie")
    anim = camera.animate(blit=True)
    anim.save('scatter.mp4')

#    anim = camera.animate(blit=True)
#    anim.save('animation.gif', writer='PillowWriter', fps=2)