import matplotlib.pyplot as plt

class SimpleGraphPlotter:
    @staticmethod
    def plot(x, y, title="Graph", xlabel="X", ylabel="Y", style="-", color="blue"):
        """Plot a line graph."""
        plt.plot(x, y, style, color=color)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    @staticmethod
    def scatter(x, y, title="Scatter Plot", xlabel="X", ylabel="Y", color="blue", size=50):
        """Create a scatter plot."""
        plt.scatter(x, y, color=color, s=size)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    @staticmethod
    def bar(x, heights, title="Bar Graph", xlabel="Categories", ylabel="Values", color="blue"):
        """Create a bar graph."""
        plt.bar(x, heights, color=color)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(axis='y', linestyle='--')
        plt.show()

    @staticmethod
    def histogram(data, title="Histogram", xlabel="Values", ylabel="Frequency", color="blue", bins=10):
        """Create a histogram."""
        plt.hist(data, bins=bins, color=color, edgecolor='black')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()


