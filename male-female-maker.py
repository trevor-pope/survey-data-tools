from pprint import pprint

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

TOTAL = 1919
#F5D580
# COLOR PALETTE

BGCOLOR = "black"
TEXTCOLOR = "white"
TEXTCOLOR2 = "black"
BARCOLOR = "#EEB211"  # Gold
M_COLOR = '#EEB211'
F_COLOR = '#F5D580'
DUAL_COLORS = ["#EEB211", "#F5D580"]  # Gold, Darkblue
TRI_COLORS = ["#EEB211", "#F5D580", "#B3A369"]  # Gold, Light Chrome Gold, Chrome Gold

# All darkest to brightest, https://coolors.co/003057-edb92e-eeb211-f5d580-b3a369
LIKERT_COLORS = {
'2_M': ["#EEB211", '#F2C751'],
'3_M': ["#EEB211", '#F1C03C', '#F4CE67'],

'2_F': ["#f4d06e", '#F7E0A2'],
'3_F': ["#f4d06e", '#F6DC97', '#F8E4AE'],
}

#'2_F': ["#F5D580", '#F7E0A2'],
#'3_F': ["#F5D580", '#F6DC97', '#F8E4AE'],
LIKERT_SCALE_AGREE_2 = ["Disagree", "Agree"]
LIKERT_SCALE_AGREE_3 = ["Disagree", "Neutral", "Agree"]

LIKERT_SCALE_SATISFACTION_2 = ["Dissatisfied", "Satisfied"]
LIKERT_SCALE_SATISFACTION_5 = ["Dissatisfied", "Neutral", "Satisfied"]

LIKERT_SCALE_OTHER = ["Never True", "Sometimes True", "Always True"]
LIKERT_SCALE_OTHER_2 = ["Uncompetitive", "Somewhat Competitive", "Competitive"]
DF = pd.read_csv('surveydata.csv', low_memory=False)


def create_hbar(cols, labels, title, xlabel='N=', width=.3):

    fig = plt.figure()  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes

    df = DF[cols]
    fems = df.loc[DF['sex_birth'] == 1]
    males = df.loc[DF['sex_birth'] == 2]

    fdata = {label: 0 for label in labels}  # Initialize each label to have a count of 0
    fdata = pd.Series(fdata)  # Turns the dict to a Series

    mdata = {label: 0 for label in labels}  # Initialize each label to have a count of 0
    mdata = pd.Series(mdata)  # Turns the dict to a Series

    c = 0
    for col in fems:  # Sums the counts in each column of the csv
        fdata[c] += fems[col].sum()
        c += 1

    c = 0
    for col in males:  # Sums the counts in each column of the csv
        mdata[c] += males[col].sum()
        c += 1

    fdata.sort_values(inplace=True, ascending=True)
    mdata, fdata = mdata.align(fdata, axis=0, join='right')
    print(f"FEMALE\n{fdata}\n\nMALE\n{mdata}")



    fdata.plot(kind='barh', ax=ax, figsize=(10, 5.7), color=F_COLOR, rot=0, fontsize=10, zorder=2,
               width=width, position=0)  # Draws Graph
    mdata.plot(kind='barh', ax=ax, figsize=(10, 5.7), color=M_COLOR, rot=0, fontsize=10, zorder=2,
               width=width, position=1)  # Draws Graph

    locs, labs = plt.xticks()
    xscale = locs[1]-locs[0]
    max_len = max([i.get_width() for i in ax.patches])
    ax.set_xlim(0, max_len + xscale/2)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_ylim(-.5 - width/2, ax.patches[-1].get_y() + .5 + width)
    ax.set_title(title, fontsize=18)
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_facecolor(BGCOLOR)
    ax.grid(zorder=0, axis='x', color='dimgrey')  # Draws axis lines for more
    ax.legend(loc='lower right', framealpha=1, labels=['Female', 'Male'])

    ftotal = count_unique(cols=cols, df=fems)
    mtotal = count_unique(cols=cols, df=males)

    for x, i in enumerate(ax.patches):
        if x < len(ax.patches) / 2:
            ax.text(i.get_width(), i.get_y() + i.get_height() / 2,  # Females
                    f"{int(round((i.get_width() / ftotal) * 100))}%",
                    color=TEXTCOLOR, verticalalignment='center',
                    fontsize=9)

        else:
            ax.text(i.get_width(), i.get_y() + i.get_height() / 2,  # Males
                    f"{int(round((i.get_width() / mtotal) * 100))}%",
                    color=TEXTCOLOR, verticalalignment='center',
                    fontsize=9)

    return fig


def create_bar(col, key, title="TITLE", chronological=False, ylabel="N=", xlabel="", width=.4, align=None):
    fig = plt.figure()  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes
    fems = DF.loc[DF['sex_birth'] == 1][col]
    males = DF.loc[DF['sex_birth'] == 2][col]

    fdata = fems.value_counts()
    mdata = males.value_counts()

    if chronological:
        fdata.sort_index(inplace=True, ascending=True)
        mdata.sort_index(inplace=True, ascending=True)

    else:
        mdata, fdata = mdata.align(fdata, axis=0, join='right')

    mdata.rename(index=key, inplace=True)
    fdata.rename(index=key, inplace=True)
    print(f"Females\n{fdata}\n\nMales\n{mdata}")

    fdata.plot(kind='bar', figsize=(10, 5.7), color=F_COLOR, rot=0, ax=ax, position=1, width=width)
    mdata.plot(kind='bar', figsize=(10, 5.7), color=M_COLOR, rot=0, ax=ax, position=0, width=width)
    ax.set_title(title, fontsize=18)
    ax.set_ylabel(ylabel, fontsize=18)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_xlabel(xlabel)
    ax.set_facecolor(BGCOLOR)
    ax.set_xlim(ax.patches[0].get_x() - .65, ax.patches[-1].get_x() + 1)
    ax.legend(framealpha=1, labels=['Females', 'Males'])

    locs, labs = plt.yticks()
    scale = locs[2]-locs[1]
    ftotal = sum(fdata)
    mtotal = sum(mdata)

    for x, i in enumerate(ax.patches):
        if i in ax.patches[:len(ax.patches) // 2]:
            ax.text(i.get_x() + i.get_width() if not align else i.get_x() + i.get_width()/2, i.get_height() + .04*scale,
                    f"{int((i.get_height() / ftotal) * 100)}%", #Females
                    color=TEXTCOLOR, horizontalalignment='right' if not align else align)

        else:
            ax.text(i.get_x() if not align else i.get_x() + i.get_width()/2, i.get_height() + .04*scale,  # Males
                    f"{int((i.get_height() / mtotal) * 100)}%",
                    color=TEXTCOLOR, horizontalalignment='left' if not align else align)

    return fig


def create_likert(cols, labels, title, legend, width=.4,
                  ylabel="", flip_legend=False):

    fig = plt.figure()  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes

    m_scales = {}
    f_scales = {}

    for c, col in enumerate(cols):
        fems = DF.loc[DF['sex_birth'] == 1][col].value_counts(normalize=True)
        males = DF.loc[DF['sex_birth'] == 2][col].value_counts(normalize=True)

        if len(fems) == 5:
            males = pd.Series({1: males[1] + males[2], 2: males[3], 3: males[4] + males[5]})
            fems = pd.Series({1: fems[1] + fems[2], 2: fems[3], 3: fems[4] + fems[5]})

        elif len(fems) == 6:
            males = pd.Series({1: males[1] + males[2] + males[3], 2: males[4] + males[5] + males[6]})
            fems = pd.Series({1: fems[1] + fems[2] + fems[3], 2: fems[4] + fems[5] + fems[6]})

        else:
            males = pd.Series({1: males[1] + males[2] + males[3], 2: males[4], 3: males[5] + males[6] + males[7]})
            fems = pd.Series({1: fems[1] + fems[2] + fems[3], 2: fems[4], 3: fems[5] + fems[6] + fems[7]})

        m_scales[labels[c]] = males.sort_index(ascending=not flip_legend)
        f_scales[labels[c]] = fems.sort_index(ascending=not flip_legend)

    m_df = pd.DataFrame(m_scales).transpose()
    f_df = pd.DataFrame(f_scales).transpose()
    print(f"MALES\n{m_df}\nFEMALES\n{f_df}")

    f_df.plot(figsize=(10, 5.7), kind='bar', rot=0, stacked=True, color=LIKERT_COLORS[f'{len(legend)}_F'],
              width=width, fontsize=10, ax=ax, position=0)
    m_df.plot(figsize=(10, 5.7), kind='bar', rot=0, stacked=True, color=LIKERT_COLORS[f'{len(legend)}_M'],
              width=width, fontsize=10, ax=ax, position=1)

    ax.set_title(title, fontsize=18)
    ax.set_facecolor(BGCOLOR)
    ax.set_xlim(ax.patches[0].get_x() - .65, ax.patches[-1].get_x() + 1)
    ax.set_ylabel(ylabel=ylabel, fontsize=18)
    ax.get_legend().remove()
    plt.yticks([])
    highest_bar_height = max([max(patch.get_extents().y1, patch.get_extents().y0) for patch in ax.patches])

    for c, i in enumerate(ax.patches):  # c goes from left to right, bottom to top, starting at 0.

        #print(f"{c}: {i.get_verts()}")
        if i.get_height() > 0:
            if i.get_y() == 0:
                text = legend[2]

            elif i.get_y() + i.get_height() >= 1:
                print(i)
                text = legend[0]

            else:
                text = legend[1]
            t1 = ax.text(i.get_x() + i.get_width()/2,
                         i.get_y() + i.get_height() - .02 if i.get_y() + i.get_height() - .02 > 0 else 0,
                         text, fontsize=8,
                         color=TEXTCOLOR2, horizontalalignment='center')

            t2 = ax.text(i.get_x() + i.get_width()/2,
                         t1._y - .03,
                         f"{int((i.get_height()) * 100)}%", fontsize=9,
                         color=TEXTCOLOR2, horizontalalignment='center')

        try: # If any two percent labels overlap, this will automatically shift them so they no longer overlap.
            for text in ax.texts[:-2]:
                bb2 = text.get_window_extent(fig.canvas.get_renderer())
                bb = t1.get_window_extent(fig.canvas.get_renderer())

                while bb.overlaps(bb2):
                    print("OVERLAP")
                    t1.set_y(t1._y + .02)
                    bb = t1.get_window_extent(fig.canvas.get_renderer())
        except IndexError:
            # Throws index error if there are <2 texts already made.
            pass

        if round(i.get_extents().y1) == round(highest_bar_height):
            if i in ax.patches[len(ax.patches)//2:]:
                ax.text(i.get_x() + i.get_width()/2, 1+.008, "Males",
                        fontsize=11, color='w', horizontalalignment='center')
            else:
                ax.text(i.get_x() + i.get_width() / 2, 1 + .008, "Females",
                        fontsize=11, color='w', horizontalalignment='center')

    return fig


def create_histogram(col="", title="TITLE", ylabel="Occurrence", bins=0, total=True):
    fig = plt.figure()  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes

    fdata = DF.loc[DF['sex_birth'] == 1][col].sort_values()
    mdata = DF.loc[DF['sex_birth'] == 2][col].sort_values()

    if bins != 0:
        fdata.plot(kind='hist', rot=0, color=F_COLOR, bins=bins, figsize=(10, 5.7), position=0, ax=ax)
        fdata.plot(kind='hist', rot=0, color=M_COLOR, bins=bins, figsize=(10, 5.7), position=1, ax=ax)

    else:
        fdata.plot(kind='hist', rot=0, color=F_COLOR, figsize=(10, 5.7), ax=ax)
        mdata.plot(kind='hist', rot=0, color=M_COLOR, figsize=(10, 5.7), ax=ax)

    ax.set_alpha(0.4)
    ax.set_title(title, fontsize=18)
    ax.set_facecolor(BGCOLOR)
    ax.set_ylabel(ylabel, fontsize=18)

    totals = []

    for i in ax.patches:
        totals.append(i.get_height())

    if total:
        total = TOTAL

    else:
        total = sum(totals)

    for i in ax.patches:
        ax.text(i.get_x() + i.get_width() / 2, i.get_height() + .5,
                str(round((i.get_height() / total) * 100, 2)) + '%', fontsize=9,
                color=TEXTCOLOR, horizontalalignment='center')

    return fig


def create_pie(col="", title="TITLE", labels=(), colors=DUAL_COLORS, explode=(0, 0)):
    fig = plt.figure()  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes

    fems = DF.loc[DF['sex_birth'] == 1][col].value_counts()
    males = DF.loc[DF['sex_birth'] == 2][col].value_counts()

    fems.plot(kind='pie', ax=ax, figsize=(10, 5.7), explode=explode, colors=colors, labels=labels, autopct='%1.1f%%')
    males.plot(kind='pie', ax=ax, figsize=(10, 5.7), explode=explode, colors=colors, labels=labels, autopct='%1.1f%%')
    ax.set_alpha(0.4)
    ax.set_title(title, fontsize=18)
    ax.set_facecolor(BGCOLOR)
    ax.set_ylabel(ylabel="", fontsize=18)

    return fig


def count_unique(cols=[], total=TOTAL, df=DF):
    count = 0
    query = df[cols].transpose()

    for i in range(total - 1):
        try:
            if 1.0 in query[i].unique():
                count += 1
        except:
            pass

    print(f"Unique Responses: {count}")
    return count


plt.show()