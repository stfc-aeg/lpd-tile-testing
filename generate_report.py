from matplotlib.backends.backend_pdf import PdfPages
import os


def export(fig_list, filename, data_path):
    # save_path must not have trailing forward slash
    save_path = "{}/develop/projects/lpd/tile_analysis".format(os.environ['HOME'])

    # split() - remove file extension from filename of data
    pdf_file = PdfPages('{}/test_results_{}.pdf'.format(save_path, filename.split('.')[0]))

    for figure in fig_list:
        # Insert each figure into PDF created by Matplotlib
        figure.savefig(pdf_file, format='pdf')

    d = pdf_file.infodict()
    d['Title'] = "Analysis of {}".format(filename)

    pdf_file.close()
