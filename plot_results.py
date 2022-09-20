import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def visualize(results, title, registered, candidates):
    voter_n = sum(results)
    sizes = [x / voter_n for x in results]
    pie_colors = [plt.cm.Accent(i) for i in range(
        4, 7)] + [plt.cm.Set1(0)] + [plt.cm.Set1(i) for i in range(2, 8)]  # Custom colors
    fig, axes = plt.subplots(2, 1)
    ax = axes.ravel()
    ax[0].pie(sizes, labels=candidates, autopct='%1.1f%%', shadow=True,
              startangle=90, colors=pie_colors, normalize=False)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax[0].axis('equal')
    # ax[0].set_title(title)
    ax[1].pie(sizes, labels=results, shadow=True,
              colors=pie_colors, normalize=False)

    # add a circle at the center to transform it in a donut chart
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.suptitle('PHE Voting | ' + title + ' | Results', fontsize=14)
    plt.title('Turnout: {}%, ({}/{})'.format((voter_n / registered)
              * 100, voter_n, registered), y=-0.3)
    plt.show()
