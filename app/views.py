import os

from flask import render_template, redirect, flash, Markup, Blueprint, url_for, session
import markdown
import numpy as np
import simplejson as json

from app import app

from app import forms
from app.engines import jpl

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route("/spectra", methods=['GET', 'POST'])
def spectra():
    mols = jpl.get_mols()
    select_list = [(int(key), val['name']) for key, val in mols.items()]
    form = forms.SpectraForm(select_list)
    if form.validate_on_submit():

        session['plot_data'] = form.molecules.data
        session['params'] = {'start':form.start_freq.data,
                             'stop': form.stop_freq.data,
                             'temp': form.temp.data,
                             'resolution': form.resolution.data,
                             'normalize': form.normalize.data
                             }

        return redirect('/plot')
    return render_template('specform.html',form=form)

@app.route('/plot')
def plot():

    data = session.get('plot_data', None)
    params = session.get('params', None)
    temp = params['temp']
    plot_vals = create_binned(data, params, temp)


    return render_template('plot.html', plot_vals=json.dumps(plot_vals))

@app.route('/spectrum')
def spectrum():
    pass


def create_binned(data, params, temp):
    mols = jpl.get_mols()
    names = []
    cats = []
    resolution = abs(params['start'] - params['stop'])/1000 * params['resolution']
    for mol in data:

        cat = jpl.get_cat(mols[str(mol)]['link'])
        cats.append(cat)
        names.append(mols[str(mol)]['name'])
    z = []
    x = []

    for i, cat in enumerate(cats):
        line_list = jpl.parse_raw_cat(cat)
        line_list[:,1] = 10**line_list[:, 1]

        if temp != 300:
            line_list[:, 1] = jpl.scale_by_temp(line_list[:,0], line_list[:,1], line_list[:,2], temp)


        freq, inten = bin_data(line_list, params['start'], params['stop'], resolution)
        x = freq.tolist()
        z.append(inten.tolist())
    if params['normalize']:
        m = np.array(z).max()
        for i, row in enumerate(z):
            temp_array = np.array(row)
            scaler = temp_array.max()/m
            z[i] = (temp_array/scaler).tolist()
    plot_vals = {
            'z': z,
            'x': x,
            'y': names,
            'type': 'heatmap',
            'colorscale': 'Viridis'
              }

    return plot_vals


def make_spectra(data, start, stop, temp, linewidth):
    return jpl.line_list_to_spectrum(frequency=data[:,0],
                              intensity=data[:,1],
                              start=start,
                              stop=stop,
                              temp=temp,
                              e_lower=data[:,2],
                                    linewidth=linewidth)

def bin_data(data, m, ma, resolution):
    bins = np.linspace(m, ma, resolution)
    heat = []
    for i, bottom in enumerate(bins[:-1]):
        ceil = bins[i+1]
        inten = data[np.where((data[:,0] < ceil) & (data[:,0]> bottom)), 1].sum()

        freq = (ceil + bottom)/2
        heat.append([freq, inten])

    heat = np.array(heat)
    print(len(bins))
    return heat[:,0], heat[:, 1]