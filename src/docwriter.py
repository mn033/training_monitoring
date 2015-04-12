__author__ = 'gru'


from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot, Figure, Package, Plt
from pylatex.utils import italic, escape_latex
from pylatex.command import Command


class TrainingDocumentWriter:

    def __init__(self, title):
        self.title = title
        self.doc = Document(title)
        self.doc.packages.append(Package('geometry', options=['a4paper', 'top=2cm', 'bottom=2.5cm', 'left=2cm', 'right=2cm']))
        self.doc.packages.append(Package('titlesec', options=['sf']))
        self.doc.packages.append(Package('lmodern'))
        self.doc.append(Command('sffamily'))

        return


    def append_plot(self, pyplot, caption=''):
        with self.doc.create(Plt(position='htbp')) as plot:
            plot.add_plot(pyplot, width=ur'\textwidth')
            if caption!='':
                plot.add_caption(caption)

        return

    def append_section(self, section_title='', content=''):
        with self.doc.create(Section(section_title)):
            if content!='':
                self.doc.append(content)
        return

    def generate_pdf(self):
        self.doc.generate_pdf()
        return