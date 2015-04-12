__author__ = 'gru'

import parsers
from matplotlib import pyplot as plt
import numpy as np
import training_constants as Constants
import docwriter
import plotter

import click


@click.command()
@click.option('--input', help='Path to .xls-file.')
@click.option('--sheet', default = 0, help='Index of the spreadsheet')
@click.option('--output', default='', help='Path to .pdf-file.')

def create_training_stats(input,  sheet, output):
    isSVGOnly = False

    parser = parsers.XlsParser(input)
    parser.read_training_data()
    visualizer = plotter.Plotter(parser.data)

    if isSVGOnly:
        visualizer.create_combined_plot().savefig('sample_fig.png')
        return

    dw = docwriter.TrainingDocumentWriter(parser.read_cell_value(0,0,0))
    dw.append_section(parser.get_sheet_names()[0],'')
    for f in visualizer.get_full_stat():
        dw.append_plot(f)

    dw.generate_pdf()


    return

if __name__ == '__main__':
    create_training_stats()







# plt.style.use('bmh')
#
# x= parser.data[Constants.date_key]
# ind = np.arange(0,len(parser.data[Constants.date_key]))
#
# y1 = parser.data[Constants.total_training_key]
# y2 = parser.data[Constants.total_recovery_key]
# y3 = parser.data[Constants.total_outdoor_key]
#
#
# width = 1.0
# plt.figure(figsize=(10,3))
#
# p1 = plt.bar(ind, y1, width, color='r', alpha=0.75)
# p2 = plt.bar(ind, y2, width, color='b', alpha=0.75, bottom=y1 )
# p3 = plt.bar(ind, y3, width, color='g', alpha=0.75,bottom = [a+b for a,b in zip(y1,y2)])
#
#
# plt.xlim([0,len(parser.data[Constants.date_key])])
# plt.ylabel('Total time of training')
# plt.title('Total time of training per day')
# plt.xticks(ind+width/2,x,rotation='90')
# plt.yticks(np.arange(0,420,30))
# plt.grid(True)
# plt.legend( (p1[0], p2[0],p3[0]), ('Training', 'Recovery', 'Outdoor') )
#
# plt.show()