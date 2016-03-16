import requests
from bs4 import BeautifulSoup
import os
import numpy as np

from collections import OrderedDict

def get_mols():
    url = 'http://spec.jpl.nasa.gov/ftp/pub/catalog/catdir.html'
    resp = requests.get(url)
    tree = BeautifulSoup(resp.text, 'lxml')
    data = tree.find('pre')
    raw_links = data.find_all('a')
    cats = OrderedDict()
    for row in raw_links:

        if 'Tex' not in row.text and 'pdf' not in row.text:
            file = row.text.replace('.cat', '').replace('c', '')
            file = str(int(file))
            cats[file] = {'link': 'http://spec.jpl.nasa.gov/' + row.get('href')}
    split_data = data.text.split('\n')

    for row in split_data[1:]:
        values = row.split(' ')
        cleaned = [x for x in values if x]
        if cleaned:
            id = cleaned[0]
            name = cleaned[1]
            cats[id]['name'] = name

    return cats

def get_cat(link):
    resp = requests.get(link)
    return resp.text


def parse_raw_cat(data):

    data = data.split('\n')

    freq = []
    inten = []
    e_lower = []

    for i, row in enumerate(data):
        if row != '':
            #print('doingthis')
            freq.append(float(row[:13]))
            inten.append(10**float(row[13+8:13+8+8]))
            e_lower.append(float(row[31:41]))

    return np.dstack((freq, inten, e_lower))[0]


def _sim(linelist, start, stop, linewidth, resolution=0.1, freq=None, sim_factor=2500):


    if freq is None:
        resolution = linewidth / 5
        freq = np.arange(start, stop, resolution)
    else:
        resolution = abs(freq[1] - freq[0])
        start = min(freq)
        stop = max(freq)

    data = np.zeros(len(freq))
    if np.shape(linelist)[1] > 2:
        linelist = linelist[:, 0:2]
    for line, inten in linelist:
        index1 = int((line - (10*linewidth/2) -start) / resolution)
        index2 = int((line + (10*linewidth/2) -start) / resolution)
        sub_data = freq[index1:index2]
        ##print(sub_data)

        data[index1:index2] += gaussian(sub_data, line, linewidth/2, inten*sim_factor)

    output_data = np.dstack((freq, data))[0]
    #print(freq)
    #print(data)

    return output_data

def line_list_to_spectrum(frequency, intensity, start, stop, linewidth,
                          temp=300,  axis=None, e_lower=None):

    if e_lower is not None:
        intensity = scale_by_temp(frequency, intensity, e_lower, temp)
        #print('got here')

    spectrum = _sim(np.dstack((frequency, intensity))[0], start, stop,
                    linewidth=linewidth, freq=axis)
    return spectrum

def gaussian(x, mu, sig, inten):
    return inten  * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def scale_by_temp(freq, intensity, energy_lower, temperature):

    k = 0.6950356 #in cm-1/k
    kt = k * temperature
    kt300 = k * 300
    #print(kt)
    #print(kt300)
    mhz_freq = lambda f: f * 0.0000333#29970.2547 * f
    x = (np.exp(-(energy_lower + mhz_freq(freq))/kt) - np.exp(-energy_lower / kt))
    y = (np.exp(-(energy_lower + mhz_freq(freq)) / kt300) - np.exp(-energy_lower / kt300))
    #print(x/y)
    return intensity * (x / y)

if __name__ == '__main__':
    from matplotlib import pyplot as plt
    mols = get_mols()
    cat = get_cat(mols['38005']['link'])
    parsed = parse_raw_cat(cat)
    spectrum = line_list_to_spectrum(parsed[:,0], parsed[:,1], 0, 1000000, linewidth=0.1, e_lower=parsed[:,2])

    plt.plot(spectrum.index.values, spectrum.intensity.values)
    plt.show()