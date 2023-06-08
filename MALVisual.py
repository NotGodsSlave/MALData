import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, argparse

mal_genres = ["Action", "Adventure", "Boys Love", "Comedy", "Drama", "Fantasy", "Girls Love", "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life",
              "Sports", "Supernatural", "Ecchi", "Hentai", "Cars", "Demons", "Game", "Harem", "Historical", "Martial Arts", "Mecha", "Military", "Music",
              "Parody", "Police", "Psychological", "Samurai", "School", "Space", "Supew Power", "Vampire"]

def genre_correlation(df):
    df_genres = df[mal_genres]
    for genre in mal_genres:
        if not (True in set(df_genres[genre])):
            df_genres = df_genres.drop(genre, axis=1)
    corr = df_genres.corr()
    f, ax = plt.subplots(figsize=(16, 12))
    cmap = sns.diverging_palette(250, 10, as_cmap=True)
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(corr, cmap=cmap, mask=mask)
    plt.savefig("genre_correlation.jpg")
    plt.close()

def genre_scores(df):
    genre_scores = {}
    for genre in mal_genres:
        if 1 in df[genre].values:
            genre_scores[genre] = df.groupby(genre)['Score'].mean()[1]
    plt.figure(figsize = (24,12))
    plt.bar(list(genre_scores.keys()), genre_scores.values(), color='b')
    plt.xticks(rotation='vertical')
    plt.savefig("scores_by_genre.jpg")
    plt.close()

def score_distribution(df, bins):
    scores = df['Score']
    plt.figure(figsize = (24,12))
    plt.hist(scores, bins = bins)
    plt.savefig("score_distribution.jpg")
    plt.close()

def score_by_status(df):
    dbs = df.groupby('Status')['Score'].mean()
    plt.figure(figsize = (24,12))
    plt.bar(df['Status'].unique(),dbs)
    plt.savefig("scores_by_status.jpg")
    plt.close()

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser("Visuals parser")
    arg_parser.add_argument('--f', required=False, default='titles.csv',
                            help="Path to dataset to visualise")
    args = arg_parser.parse_args()
    df = pd.read_csv(args.f)
    genre_correlation(df)
    genre_scores(df)
    score_distribution(df, 20)
    score_by_status(df)

