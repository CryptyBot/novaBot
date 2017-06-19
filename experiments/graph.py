"""

IMPLEMENTATION OF graph TO DETERMINE ARBITRAGE OPPORTUNITIES VIA BELLMAN-FORD

Given pricing data for poloniex data, find arbitrage opportunities.

u'BTC_ETH': {
    u'last': u'0.01938904',
    u'quoteVolume': u'751935.44455731',
    u'high24hr': u'0.01998655',
    u'isFrozen': u'0',
    u'highestBid': u'0.01939181',
    u'percentChange': u'-0.00151710',
    u'low24hr': u'0.01896041',
    u'lowestAsk': u'0.01939861',
    u'id': 148,
    u'baseVolume': u'14596.47904223'
}

BTC: Base currency

        last
BTC ------------> ETH

        1/last
ETH <------------ BTC


"""

import networkx as nx
import matplotlib.pyplot as plt
import math
import requests
import json
import time



def getTickerData():
    response = requests.get("https://poloniex.com/public?command=returnTicker")
    tickerData = response.json()
    print 'received data...'
    return tickerData


def parseTicker(ticker):
    parsed = ticker.split('_')
    return parsed[0], parsed[1]


def removeLonerNodes(G):
    # Clean up loner currencies (if degree of node < 1, remove)
    for node in G.nodes():
        if len(G[node]) <= 1:
            G.remove_node(node)
    return G


def createGraphFromData(tickerData):
    G = nx.DiGraph()

    for ticker in tickerData:
        baseCurrency, tradeCurrency = parseTicker(ticker)
        # print ticker
        # print tickerData[ticker]

        lastPrice = float(tickerData[ticker]['last'])

        G.add_edge(baseCurrency, tradeCurrency, weight=lastPrice)
        G.add_edge(tradeCurrency, baseCurrency, weight=(1/lastPrice))

    G = removeLonerNodes(G)

    return G



def logEdges(G):
    # Bellman-Ford edge preparation \\ edge_weight = -log(edge_weight)
    for edge in G.edges(data=True):
        weight = edge[2]['weight']

        G_w = G[edge[0]][edge[1]]['weight']
        G[edge[0]][edge[1]]['weight'] = math.log(G_w)

        # print 'weight:\t\t',weight
        # print'new weight:\t', math.log(G_w)
    return G


def drawGraph(G):
    pos = nx.circular_layout(G)
    print G
    nx.draw(G,pos)
    # use default edge labels
    nx.draw_networkx_edge_labels(G,pos)

    plt.show()


def main():
    # for i in range(5):
        # time.sleep(1)

    data = getTickerData()
    Graph = createGraphFromData(data)

    # Graph = logEdges(Graph)
    drawGraph(Graph)
    print nx.info(Graph)


    try:
        path = nx.bellman_ford(Graph,'BTC',weight='weight')
    except Exception as e:
        print e


if __name__ == '__main__':
    main()
