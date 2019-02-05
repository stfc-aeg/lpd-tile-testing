from matplotlib.backends.backend_pdf import PdfPages


def export(fig_list, filename):
    # Remove file extension from filename of data
    filename = filename.split('.')[0]

    pdf_file = PdfPages('test_results_{}.pdf'.format(filename))
    for figure in fig_list:
        # Insert each figure into PDF created by Matplotlib
        figure.savefig(pdf_file, format='pdf')

    pdf_file.close()
