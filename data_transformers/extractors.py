def text_from_cluster(clustered_text, cluster_number):
    cluster_data, tweet_ids  = list(zip(*clustered_text))
    return [text for text, cluster in cluster_data 
        if cluster == cluster_number]
    
def ids_from_cluster(clustered_text, cluster_number):
    return [tweet_id for cluster_data, tweet_id in clustered_text
        if cluster_data[1] == cluster_number]
