__author__ = 'gru'

import TrainingDataParser
from matplotlib import pyplot as plt
import numpy as np
from collections import Counter
import TrainingDataConstants as Constants
from matplotlib.patches import Rectangle


class Plotter:
    def __init__(self, training_data):
        self.d = training_data
        # use a certain style
        plt.style.use('bmh')
        return

    def get_full_stat(self):
        figures = []
        figures.append(self.plot_bar_graph())
        figures.append(self.generate_line_plot('State of skin and health', self.d[Constants.date_key],
                                               [self.d[Constants.skin_key], self.d[Constants.health_key]], ['r', 'b'],
                                               [Constants.skin_key, Constants.health_key],
                                               '[0 = poor ... 10 = outstanding]'))
        figures.append(self.generate_line_plot('Form and Motivation', self.d[Constants.date_key],
                                               [self.d[Constants.form_key], self.d[Constants.motivation_key]],
                                               ['g', 'c'], [Constants.form_key, Constants.motivation_key],
                                               '[0 = poor ... 10 = outstanding]'))
        figures.append(self.generate_line_plot('Mental Fitness and sleep', self.d[Constants.date_key],
                                               [self.d[Constants.mental_fitness_key], self.d[Constants.sleep_key]],
                                               ['m', 'y'],
                                               [Constants.mental_fitness_key, Constants.sleep_key],
                                               '[0 = poor ... 10 = outstanding]'))
        figures.append(self.plot_train_share())
        figures.append(self.plot_pie_charts())

        return figures

    def generate_line_plot(self, title, x, y_list, colors, labels, y_label):

        for i, y in enumerate(y_list):
            y_list[i] = self.match_list_length(x, y)

        ind = np.arange(0, len(x))

        fig = plt.figure(figsize=(10, 3))
        ax = fig.add_subplot(111)

        legend_refs = []
        for i, y in enumerate(y_list):
            l = ax.plot(ind, y, 0, 10, color=colors[i], alpha=0.75, linewidth=1.5, linestyle='-', marker='o')
            legend_refs.append(l[0])
        width = 1.0
        ax.set_xlim([-width / 2, len(x)]) # compensate the origin to match with bar chart from above
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.axes.set_xticks(ind)
        ax.set_xticklabels(x, rotation='90')
        ax.set_yticks(np.arange(0, 10, 1))
        ax.grid(False)
        ax.legend(legend_refs, labels)
        plt.gcf().subplots_adjust(bottom=0.25)  # prevent the labels from being cut off

        return fig


    def plot_train_share(self):
        y = self.d[Constants.total_training_key]
        y1 = self.d[Constants.warmup_key]
        y2 = self.d[Constants.project_key]
        y3 = self.d[Constants.power_end_key]
        y4 = self.d[Constants.local_end_key]
        y5 = self.d[Constants.campus_key]
        y6 = self.d[Constants.systemwall_key]
        y7 = self.d[Constants.fingerboard_key]
        y8 = self.d[Constants.core_key]
        y9 = self.d[Constants.athletics_key]

        y1_clean = self.remove_non_training_entries(y, y1)
        y2_clean = self.remove_non_training_entries(y, y2)
        y3_clean = self.remove_non_training_entries(y, y3)
        y4_clean = self.remove_non_training_entries(y, y4)
        y5_clean = self.remove_non_training_entries(y, y5)
        y6_clean = self.remove_non_training_entries(y, y6)
        y7_clean = self.remove_non_training_entries(y, y7)
        y8_clean = self.remove_non_training_entries(y, y8)
        y9_clean = self.remove_non_training_entries(y, y9)

        dates = self.d['Date']
        dates_clean = self.clean_date_list(y, dates)

        # print y1_clean
        # print y2_clean
        # print y3_clean
        #print dates_clean

        y = np.row_stack((y1_clean, y2_clean, y3_clean, y4_clean, y5_clean, y6_clean, y7_clean, y8_clean, y9_clean))
        x = np.arange(len(dates_clean))

        fig = plt.figure(figsize=(10, 3))
        # make the stack plot
        stack_coll = plt.stackplot(x, y)
        plt.title('Share of training methods')
        plt.ylabel('Time in minutes')
        plt.xlim([0, len(dates_clean)])
        ind = np.arange(0, len(dates))
        plt.xticks(ind, dates_clean, rotation='90')
        # make proxy artists
        proxy_rects = [Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0]) for pc in stack_coll]
        # make the legend
        label_list = [Constants.warmup_key, Constants.project_key, Constants.power_end_key, Constants.local_end_key,
                      Constants.campus_key, Constants.systemwall_key, Constants.fingerboard_key, Constants.core_key,
                      Constants.athletics_key]
        plt.legend(proxy_rects, label_list)
        plt.grid(True)
        plt.gcf().subplots_adjust(bottom=0.25)  # prevent the labels from being cut off

        return fig

    def plot_bar_graph(self):
        d = self.d
        dates = d[Constants.date_key]

        x = d[Constants.date_key]
        ind = np.arange(0, len(dates))
        y1 = d[Constants.total_training_key]
        y2 = d[Constants.endurance_key]
        y3 = d[Constants.total_recovery_key]
        y4 = d[Constants.total_outdoor_key]

        width = 1.0

        fig = plt.figure(figsize=(10, 3))
        ax0 = fig.add_subplot(111)

        p1 = ax0.bar(ind, y1, width, color='r', alpha=0.75)
        p2 = ax0.bar(ind, y2, width, color='c', alpha=0.75, bottom=y1)
        p3 = ax0.bar(ind, y3, width, color='b', alpha=0.75, bottom=[a + b for a, b in zip(y1, y2)])
        p4 = ax0.bar(ind, y4, width, color='g', alpha=0.75, bottom=[a + b + c for a, b, c in zip(y1, y2, y3)])

        ax0.set_xlim([0, len(dates)])
        ax0.set_ylabel('Total time of training')
        ax0.set_title('Total time of training per day')
        ax0.axes.set_xticks(ind + width / 2)
        ax0.set_xticklabels(x, rotation='90')
        ax0.set_yticks(np.arange(0, 420, 30))
        ax0.grid(False)
        ax0.legend((p1[0], p2[0], p3[0], p4[0]), ('Training', 'Endurance', 'Recovery', 'Outdoor'))
        plt.gcf().subplots_adjust(bottom=0.25)  # prevent the labels from being cut off

        return fig

    def plot_pie_charts(self):
        # plot pie chart to illustrate share of locations
        c = Counter(self.d[Constants.location_key])
        fracs = [c[x] for x in c.keys()]
        print fracs
        labels = ["%s - %d" % (key, c[key]) for key in c.keys()]  # percentage (c[x]*1.0)/sum(c.values())
        explode = (0, 0.05)  # has to be the same length as c.keys()

        # colors = ['b', 'g', 'r', 'c']
        #alternative style
        #plt.pie(fracs, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
        fig = plt.figure(figsize=(12, 3))
        ax5 = plt.subplot2grid((1, 2), (0, 0), colspan=1)
        patches, texts = ax5.pie(fracs, explode=explode, startangle=90)
        ax5.legend(patches, labels, loc="best")
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        ax5.axis('equal')
        ax5.set_title('Training locations')

        #plot pie chart to illustrate share of training
        key_list = [Constants.warmup_key, Constants.project_key, Constants.power_end_key, Constants.local_end_key,
                    Constants.campus_key, Constants.systemwall_key, Constants.fingerboard_key, Constants.core_key,
                    Constants.athletics_key]
        values = []
        for i, k in enumerate(key_list):
            values.append(sum(self.d[k]))

        fracs = values
        #colors_= list(six.iteritems(matplotlib_colors.cnames))

        #color_list = [c[0] for c in colors_]
        #color_list = color_list[:len(key_list)]
        ax6 = plt.subplot2grid((1, 2), (0, 1), colspan=1)
        plt.pie(fracs, labels=key_list, autopct='%1.1f%%', shadow=True, startangle=90)
        #ax6.legend(patches, key_list, loc="best")
        #Set aspect ratio to be equal so that pie is drawn as a circle.
        ax6.axis('equal')
        ax6.set_title('Share of training methods')

        return fig


    def create_combined_plot(self):
        d = self.d
        # plot bar graph, which visualizes the amount of training
        plt.style.use('bmh')
        dates = d[Constants.date_key]

        x = d[Constants.date_key]
        ind = np.arange(0, len(dates))

        y1 = d[Constants.total_training_key]
        y2 = d[Constants.endurance_key]
        y3 = d[Constants.total_recovery_key]
        y4 = d[Constants.total_outdoor_key]

        width = 1.0
        # fig, axes = plt.subplots(4,1,figsize=(12,18))
        # ax0,ax1,ax2,ax3= axes.ravel()

        fig = plt.figure(figsize=(12, 24))
        ax0 = plt.subplot2grid((6, 2), (0, 0), colspan=2)

        p1 = ax0.bar(ind, y1, width, color='r', alpha=0.75)
        p2 = ax0.bar(ind, y2, width, color='c', alpha=0.75, bottom=y1)
        p3 = ax0.bar(ind, y3, width, color='b', alpha=0.75, bottom=[a + b for a, b in zip(y1, y2)])
        p4 = ax0.bar(ind, y4, width, color='g', alpha=0.75, bottom=[a + b + c for a, b, c in zip(y1, y2, y3)])

        ax0.set_xlim([0, len(dates)])
        ax0.set_ylabel('Total time of training')
        ax0.set_title('Total time of training per day')
        ax0.axes.set_xticks(ind + width / 2)
        ax0.set_xticklabels(x, rotation='90')
        ax0.set_yticks(np.arange(0, 420, 30))
        ax0.grid(False)
        ax0.legend((p1[0], p2[0], p3[0], p4[0]), ('Training', 'Endurance', 'Recovery', 'Outdoor'))

        #-------------------------------------------------------------------------------------------
        # Tweak spacing between subplots to prevent labels from overlapping
        plt.subplots_adjust(hspace=0.65)

        y1 = self.match_list_length(x, d[Constants.skin_key])
        y2 = self.match_list_length(x, d[Constants.health_key])
        #y3 = match_list_length(x,d[workload_key])

        ax1 = plt.subplot2grid((6, 2), (1, 0), colspan=2)
        l1 = ax1.plot(ind, y1, 0, 10, color='r', alpha=0.75, linewidth=1.5, linestyle='-', marker='o')
        l2 = ax1.plot(ind, y2, color='b', alpha=0.75, linewidth=1.5, linestyle='-', marker='p')
        #l3 = ax1.plot(ind, y3,color='r', alpha=0.75, linewidth=1.5, linestyle='-', marker ='.')

        ax1.set_xlim([-width / 2, len(dates)])  #compensate the origin to match with bar chart from above
        ax1.set_ylabel('[0 = poor ... 10 = outstanding] ')
        ax1.set_title('State of skin and health')
        ax1.axes.set_xticks(ind)
        ax1.set_xticklabels(x, rotation='90')
        ax1.set_yticks(np.arange(0, 10, 1))
        ax1.grid(False)
        ax1.legend((l1[0], l2[0]), ('Skin', 'Health'))

        #-------------------------------------------------------------------------------------------
        y1 = self.match_list_length(x, d[Constants.form_key])
        y2 = self.match_list_length(x, d[Constants.motivation_key])

        ax2 = plt.subplot2grid((6, 2), (2, 0), colspan=2)
        l1 = ax2.plot(ind, y1, 0, 10, color='g', alpha=0.75, linewidth=1.5, linestyle='-', marker='o')
        l2 = ax2.plot(ind, y2, color='c', alpha=0.75, linewidth=1.5, linestyle='-', marker='p')

        ax2.set_xlim([-width / 2, len(dates)])  #compensate the origin to match with bar chart from above
        ax2.set_ylabel('[0 = poor ... 10 = outstanding] ')
        ax2.set_title('Form and Motivation')
        ax2.axes.set_xticks(ind)
        ax2.set_xticklabels(x, rotation='90')
        ax2.set_yticks(np.arange(0, 10, 1))
        ax2.grid(False)
        ax2.legend((l1[0], l2[0]), ('Form', 'Motivation'))

        #-------------------------------------------------------------------------------------------
        y1 = self.match_list_length(x, d[Constants.mental_fitness_key])
        y2 = self.match_list_length(x, d[Constants.sleep_key])
        print y1
        ax3 = plt.subplot2grid((6, 2), (3, 0), colspan=2)
        l1 = ax3.plot(ind, y1, 0, 10, color='m', alpha=0.75, linewidth=1.5, linestyle='-', marker='o')
        l2 = ax3.plot(ind, y2, color='y', alpha=0.75, linewidth=1.5, linestyle='-', marker='p')

        ax3.set_xlim([-width / 2, len(dates)])  #compensate the origin to match with bar chart from above
        ax3.set_ylabel('[0 = poor ... 10 = outstanding] ')
        ax3.set_title('Mental Fitness and sleep')
        ax3.axes.set_xticks(ind)
        ax3.set_xticklabels(x, rotation='90')
        ax3.set_yticks(np.arange(0, 10, 1))
        ax3.grid(False)
        ax3.legend((l1[0], l2[0]), ('Mental Fitness', 'Sleep'))


        #-------------------------------------------------------------------------------------------
        #plot area chart


        x = d[Constants.date_key]
        y = d[Constants.total_training_key]
        y1 = d[Constants.warmup_key]
        y2 = d[Constants.project_key]
        y3 = d[Constants.power_end_key]
        y4 = d[Constants.local_end_key]
        y5 = d[Constants.campus_key]
        y6 = d[Constants.systemwall_key]
        y7 = d[Constants.fingerboard_key]
        y8 = d[Constants.core_key]
        y9 = d[Constants.athletics_key]

        y_clean = [x for x in y if x != 0]
        y1_clean = self.remove_non_training_entries(y, y1)
        y2_clean = self.remove_non_training_entries(y, y2)
        y3_clean = self.remove_non_training_entries(y, y3)
        y4_clean = self.remove_non_training_entries(y, y4)
        y5_clean = self.remove_non_training_entries(y, y5)
        y6_clean = self.remove_non_training_entries(y, y6)
        y7_clean = self.remove_non_training_entries(y, y7)
        y8_clean = self.remove_non_training_entries(y, y8)
        y9_clean = self.remove_non_training_entries(y, y9)

        date = d['Date']
        dates_clean = self.clean_date_list(y, date)

        x = np.arange(len(dates_clean))
        y = np.row_stack((y1_clean, y2_clean, y3_clean, y4_clean, y5_clean, y6_clean, y7_clean, y8_clean, y9_clean))

        ax4 = plt.subplot2grid((6, 2), (4, 0), colspan=2)
        # make the stack plot
        stack_coll = ax4.stackplot(x, y)
        ax4.set_title('Share of training methods')
        ax4.set_ylabel('Time in minutes')
        ax4.set_xlim([0, len(dates)])
        ax4.axes.set_xticks(ind)
        ax4.set_xticklabels(dates_clean, rotation='90')
        # make proxy artists
        proxy_rects = [Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0]) for pc in stack_coll]
        # make the legend
        label_list = [Constants.warmup_key, Constants.project_key, Constants.power_end_key, Constants.local_end_key,
                      Constants.campus_key, Constants.systemwall_key, Constants.fingerboard_key, Constants.core_key,
                      Constants.athletics_key]
        ax4.legend(proxy_rects, label_list)
        ax4.grid(True)

        #-------------------------------------------------------------------------------------------
        #plot pie chart to illustrate share of locations
        c = Counter(d[Constants.location_key])
        fracs = [c[x] for x in c.keys()]
        print fracs
        labels = ["%s - %d" % (key, c[key]) for key in c.keys()]  #percentage (c[x]*1.0)/sum(c.values())
        explode = (0, 0.05)  # has to be the same length as c.keys()

        #colors = ['b', 'g', 'r', 'c']
        #alternative style
        #plt.pie(fracs, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
        ax5 = plt.subplot2grid((6, 2), (5, 0), colspan=1)
        patches, texts = ax5.pie(fracs, explode=explode, startangle=90)
        ax5.legend(patches, labels, loc="best")
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        ax5.axis('equal')
        ax5.set_title('Training locations')

        #-------------------------------------------------------------------------------------------
        #plot pie chart to illustrate share of training
        #key_list = [warmup_key, project_key, power_end_key, local_end_key,campus_key,systemwall_key,fingerboard_key,core_key,athletics_key]
        #values = []
        #for i,k in enumerate(key_list):
        #    values.append( sum(d[k]))

        #fracs = values
        #colors_= list(six.iteritems(matplotlib_colors.cnames))

        #color_list = [c[0] for c in colors_]
        #color_list = color_list[:len(key_list)]
        #ax6 = plt.subplot2grid((6,2), (5,1), colspan=1)
        #plt.pie(fracs, labels=key_list, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
        #ax6.legend(patches, key_list, loc="best")
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        #ax6.axis('equal')
        #ax6.set_title('Share of training methods')

        #plt.show()


        return fig


    @staticmethod
    def match_list_length(ref_list, list_to_match):
        matched_list = list_to_match
        diff = len(ref_list) - len(list_to_match)
        if (diff > 0):
            for i in range(len(ref_list) - diff, len(ref_list)):
                matched_list.append(0)
        if (diff < 0):
            for i in range(0, diff * -1):
                matched_list.pop();

        return matched_list

    @staticmethod
    def remove_non_training_entries(refList, list_to_clean):
        ref_clean = [x for x in refList if x != 0]
        cleaned_list = []  # [0 for x in ref_clean]
        ctr = 0
        for i, el in enumerate(refList):
            if (el != 0):
                if (i < len(list_to_clean)):
                    cleaned_list.append(list_to_clean[i])  # [ctr]=y1[i]
                else:
                    cleaned_list.append(0)  # [ctr]=0

                ctr += 1

        return cleaned_list

    @staticmethod
    def clean_date_list(refList, date_list):
        cleaned_dates = []
        for i, el in enumerate(refList):
            if (el != 0):
                cleaned_dates.append(date_list[i])
        return cleaned_dates