import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_graph(noten):
    left = ['1', '-1', '1-2', '+2', '2', '-2', '2-3', '+3', '3', '-3', '3-4', '+4', '4', '-4', '4-5', '+5', '5', '-5', '5-6', '+6', '6']
    height = [noten.count(i/4) for i in range(4, 25)]
    tick_labels = ['1', '-1', '1-2', '+2', '2', '-2', '2-3', '+3', '3', '-3', '3-4', '+4', '4', '-4', '4-5', '+5', '5', '-5', '5-6', '+6', '6']
    plt.bar(left, height, tick_label=tick_labels, width=0.8, color=['green'])
    plt.xlabel('Noten')
    plt.ylabel('Anzahl der Noten')
    plt.title('Noten')
    plt.savefig(r'C:/Users/linla\Documents/GitHub/Noten-Berechner/static/images/graph')