import matplotlib.pyplot as plt


def pie_visualize(title, labels, sizes, colors, explode):
    """ Draw a piechart using pyplot with the given parameters. """
    # The default configuration, left here so that I don't have to constantly look up how to use the method.
    # Data to plot
    # labels = 'Python', 'C++', 'Ruby', 'Java'
    # sizes = [215, 130, 245, 210]
    # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    # explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.title(title)
    plt.show()


def subplot(x, y, z):
    plt.subplot(x, y, z)


def show():
    plt.show()
