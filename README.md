# Clustering: tutorial and lab
## Part I. Tutorial
### Clustering small documents

To run the code you need to install the graphics library Pillow-Pil - the same library which we used in the decision tree lab.
<ol>
  <li>
    Read file `titles.txt`. Each line represents a paper title. There are 2 evident paper types: titles 1-5 represents papers on Human-Computer Interaction, and titles 6-9 -- on Theory of Computing. 
  </li>
  <li>
    Convert documents into word matrix using `titles_to_vectors.py`. Look at the matrix in file `titles_vectors.txt`. Note that stopwords as well as the words that occur only once have been removed. Why is that?
  </li>
  <li>
    Explore different distance metrics by running `euclidean_documents.py`, `tanimoto_documents.py`, `cosine_documents.py`, and `pearson_documents.py`. For example, distance between d4 and d8 should be significant larger than distance between d7 and d8, because d7 belongs to the same topic as d8. What do you observe? Compare results for vector-based and geometrical distance: which ones work better for documents?
  </li>
  <li>
    Now let's explore the distance between different words based on their occurrence in the documents. For that run `pearson_words.py`.
  </li>
  <li>
    Create 2 clusters using k-means algorithm implemented in `clusters.py`. For this run `kmclustertitles.py`. Did k-means find the expected clusters?
  </li>
  <li> Now cluster words by the documents where they occur by running `kmclusterwords.py`. Do the group of words make sense? Try to play with different number of clusters.
  </li>
  <li>Finally, try hierarchical clustering of documents by running `hclustertitles.py`. Hierarchical clustering seems to work much better. Why do you think that is?
  </li>
</ol>

## Part II. Homework
### Clustering countries 
See <a href="https://docs.google.com/document/d/1x1odD42pG4v0E0ioEgKblb6hBwf-FhH0lYzRlvSSAcE/edit?usp=sharing">Google doc</a>.
### Files explanation
#### .py files
1. `prep_data.py` clean useless columns and fill missing values with mean of 3 nearest neighbors.
2. `clusters.py` has all related clustering functions, including distance metrics: pearson, euclidean, cosine, tanimoto, clustering techniques: k-means, bisecting-kmeans, hierarchical; and other utility functions.
3. `hclustertitles.py` can create pictures of hierarchical clusters with different distance metrics and inter distances, create heatmap, output clustering results, and create word clouds for each cluster.
4. `kmclustertitles.py` can create SSE graphs of different distance metrics, create heatmap, output clustering results, and create word clouds for each cluster.
5. `prep_visulization.py` changes country names to the ones Google visualization recognizes and convert clustering results `.csv` files to `.js` files.
6. `word_cloud.py` has utilities functions for creating the word clouds.

#### .csv files
<ol>
  <li>
    `dataset.csv` is the original dataset.
  </li>
  <li>
    `processed.csv` is the cleaned dataset with only useful columns for this lab and missing values filled with mean of three nearest neighbors.
  </li>
  <li>
    `country_details.csv` has two columns, first one is the country names in the dataset, and second one is the corresponding country names that Google visualization needs.
  </li>
  <li>
    `dimensions_keywords.csv` is key words for each cultural dimensions. This is for creating the word clouds.
  </li>
  <li>
    `hcluster_result.csv` is the results of hierarchical clustering.
  </li>
  <li>
    `kcluster_result.csv` is the results of bisecting kmeans clustering.
  </li>
</ol>

#### webpage files
`visulization.html`, `hcluster_result.js`, `kcluster_result.js` are for visulization. 

#### folders
<ol>
  <li>
    `graphs` contains all resulting graphs and pictures
  </li>
  <li>
    `other files` contains files that part I mentions but are useless for this lab.
  </li>
</ol>



