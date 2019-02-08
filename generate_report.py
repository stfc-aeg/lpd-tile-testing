from matplotlib.backends.backend_pdf import PdfPages
import os


def export(fig_list, filename, data_path):
    ''' Creates PDF file of all the figures displayed in the notebook
    '''
    # Protecting path from trailing '/' from $HOME
    home_location = os.environ['HOME']
    if home_location[-1] == '/':
        home_location = home_location[:-1]

    save_path = "{}/develop/projects/lpd/tile_analysis".format(os.environ['HOME'])

    # split() - remove file extension from filename of data
    pdf_file = PdfPages('{}/test_results_{}.pdf'.format(save_path, filename.split('.')[0]))

    for figure in fig_list:
        # Insert each figure into PDF created by Matplotlib
        figure.savefig(pdf_file, format='pdf')

    # Add metadata to PDF file
    d = pdf_file.infodict()
    d['Title'] = "Analysis of {}".format(filename)

    pdf_file.close()
