from matplotlib.backends.backend_pdf import PdfPages
import os


def export(fig_list, filename):
    # Remove file extension from filename of data
    filename = filename.split('.')[0]

    # save_path must not have trailing forward slash
    save_path = "{}/develop/projects/lpd/tile_analysis".format(os.environ['HOME'])

    pdf_file = PdfPages('{}/test_results_{}.pdf'.format(save_path, filename))
    for figure in fig_list:
        # Insert each figure into PDF created by Matplotlib
        figure.savefig(pdf_file, format='pdf')

    d = pdf_file.infodict()
    d['Title'] = "Analysis of {}".format(filename)

    pdf_file.close()
