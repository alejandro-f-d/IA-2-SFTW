from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_word_cloud(word_counts, path_save, maxwords= 10):
    """Generación del diagrama a mostrar."""
    
    wc = WordCloud(width=800, height=400, background_color='white', max_words=maxwords)
    wc.generate_from_frequencies(word_counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc)
    plt.axis('off')
    # plt.show()
    plt.savefig(f"{path_save}/abstract_keywords")

def generate_figure_plot(data_dict, path_save):
    names = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(12, 6))
    bars = plt.bar(names, values, color='skyblue', edgecolor='navy')

    plt.xlabel('Document Name', fontweight='bold')
    plt.ylabel('Number of Figures', fontweight='bold')
    plt.title('Figures per Scientific Paper', fontsize=14)
    
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, yval, ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(f"{path_save}/count_figures")
    # plt.show()

