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
    """ Call pyplot's subplot with the given parameters. """
    plt.subplot(x, y, z)


def show():
    """ Show the previously plotted plots. """
    plt.show()


def barplot(x, y, title, xaxis, yaxis):
    """ Draw a barplot with the given parameters. """
    plt.bar(x, y)
    plt.title(title, loc="center")
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)


def plot(x, y, label, xaxis, yaxis):
    """ Draw a simple lineplot with the given parameters. """
    plt.plot(x, y)
    plt.title(label, loc="center")
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)


def stitle(title):
    """ Set the supertitle of a subplot. """
    plt.suptitle(title)
