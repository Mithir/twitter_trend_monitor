from matplotlib import animation
import matplotlib.pyplot as plt


class PlotProvider:
    """
    a wrapper to the matplotlib client in order to create the graph
    """
    def __init__(self, hashtag_counter, refresh_interval=1000, show_top=10):
        self._show_top = show_top
        self._refresh_interval = refresh_interval
        self._hashtagCounter = hashtag_counter

    def animate(self, i):
        data = self._hashtagCounter.get_most_common(self._show_top)
        values = []
        keys = []

        for currData in data:
            keys.append(currData[0])
            values.append(currData[1])

        plt.clf()
        bar = plt.bar(range(len(data)), values, align='center')
        plt.xticks(range(len(data)), keys)

        return bar

    def start(self):
        fig, ax = plt.subplots()
        ani = animation.FuncAnimation(fig, self.animate, interval=self._refresh_interval)
        plt.show()
