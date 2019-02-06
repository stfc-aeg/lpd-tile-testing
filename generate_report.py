from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os
from datetime import datetime


def export(fig_list, filename, data_path):
    # save_path must not have trailing forward slash
    save_path = "{}/develop/projects/lpd/tile_analysis".format(os.environ['HOME'])

    # split() - remove file extension from filename of data
    pdf_file = PdfPages('{}/test_results_{}.pdf'.format(save_path, filename.split('.')[0]))

    #text_fig = create_text_figure(filename, data_path)
    # Insert at front of list so it'll be the first page
    #fig_list.insert(0, text_fig)

    for figure in fig_list:
        # Insert each figure into PDF created by Matplotlib
        figure.savefig(pdf_file, format='pdf')

    d = pdf_file.infodict()
    d['Title'] = "Analysis of {}".format(filename)

    pdf_file.close()
