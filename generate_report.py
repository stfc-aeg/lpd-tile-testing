from matplotlib.backends.backend_pdf import PdfPages


def export(fig_list):
    pdf_file = PdfPages('test_results.pdf')
    for figure in fig_list:
        figure.savefig(pdf_file, format='pdf')
    pdf_file.close()
