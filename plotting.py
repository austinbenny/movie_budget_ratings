
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
import itertools

def linear_trendline(x,y):
    ''' 
    Calculates y equation and R_squared from: 
    (https://medium.com/@mjfstanford/simple-linear-regression-in-python-905b759ef0e6)
    '''
    denominator = x.dot(x) - x.mean()*x.sum()
    m = (x.dot(y) - y.mean()*x.sum())/denominator
    b = (y.mean() * x.dot(x) - x.mean() * x.dot(y))/denominator
    y_pred = m*x + b
    res = y - y_pred
    tot = y - y.mean()
    R_squared = 1. - res.dot(res)/tot.dot(tot)
    return y_pred, R_squared, m, b

def rand_color():
    ''' get random color '''

    # tab_colors = ('tab:blue', 'tab:orange', 'tab:green', 'tab:red', \
    #     'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan')
    
    # return np.random.choice(tab_colors)

    #rand floats from 0 - 0.9 because higher floats are lighter
    r = 0.70*np.random.rand()
    g = 0.70*np.random.rand()
    b = 0.70*np.random.rand()
    color = (r,g,b)
    if len(set(color)) == 3:
        return color
    else:
        rand_color()

def get_markers(num):
    ''' generate specified amount of markers '''

    markers = itertools.cycle(('o','^','s','x','*','D'))
    return [next(markers) for marker in range(num)]

def master_plot(x,y,xlabel='x',ylabel='y',label='_' , title=False,filename='python_figure', \
    savefig=True, extension = 'eps', color = 'xkcd:blue', marker = '', linestyle='-', \
        boxoff=False, linewidth='0.5', alpha=1, trendline=False, legend=True, \
            leg_frameon = True, ar_equal = True,loc='best',\
                generate_markers = False,draw_eqn = False):

    '''
            INPUTS: 
            (x = x values for line(s), for >1 line, use [x1,x2,...])
            (y = y values for line(s), for >1 line, use [y1,y2,...])
            (xlabel = xtitle, put r before for LaTeX math)
            (ylabel = ylabel, put r before for LaTeX math)
            (label = label for legend)
            (title = title, put r before for LaTeX math)
            (extension = file extension type)
            (boxoff = no top or right border)
            (color = marker and line color)
            (marker = shape of marker)
            (linewidth = width of line)
            (linestyle = style of line)
            (savefig = false to not save figure)
            (alpha = change transparency)
            (trendline = calculate trendline)
            (filename = name of output file, default=title)
            (legend = show legend)
            (leg_frameon = remove bounding box from legend)
            (ar_equal = turn false to show plot with custome generated aspect ratio)
            (loc = change location of legend from 'best')
            (generate_markers = let program generate x amount of markers for lines)
            (draw_eqn = to draw trendline eqn on plot)

        NOTE: desiered multiple saved plots, just 
            master_plot(args1) -> saved as plot1
            master_plot(args2) -> saved as plot2
            master_plot(args3) -> saved as plot3
            .
            .
            .
    '''
    
    # error checking
    x = np.array(x)
    y = np.array(y)
    # dim = 0, only a number
    # dim = 1, list
    # dim = 2, list of lists
    if (x.ndim > 0 and y.ndim > 0):
        if x.shape == y.shape:
            dim = x.ndim
        else:
            print('ERROR: x and y values must be same size')
            print('x = {} and y = {}'.format(x.shape,y.shape))
            sys.exit()
    else:
        print('ERROR: x and y values must be same dim')
        print('x = {} and y = {}'.format(x.ndim,y.ndim))
        sys.exit()

    # change plot stuff for every case
    fig_line_width = 0.5
    mpl.rcParams['patch.linewidth'] = fig_line_width # legend linewidth
    plt.rcParams['axes.linewidth'] = fig_line_width
    plt.rcParams["legend.framealpha"] = 1.0
    plt.rcParams["legend.frameon"] = leg_frameon

    latex = False # to use latex font numbering, turn true - matplotlib latex is kinda weird
    if latex == True:
        plt.rcParams['text.usetex'] = True
    else:
        plt.rcParams['font.sans-serif'] = 'Arial'
        plt.rcParams['font.size'] = 9
    
    if generate_markers == True:
        if dim == 1:
            marker = 1
        else:
            marker = get_markers(len(x)) #output list
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if ar_equal == True:
        print('Aspect ratio of plot is on equal, make "ar_equal=False" to make regular')
        ax.set_aspect(aspect='equal')
    else:
        ax.set_aspect(aspect='auto')

    if (dim > 1):
        color = np.asarray(color)
        markers = np.asarray(marker)
        if color.ndim == 0:
            if markers.ndim == 0:
                for x, y in zip(x,y):
                    plt.plot(x,y,linestyle=linestyle, marker=marker, color=rand_color(), \
                        markersize=6, fillstyle='none', linewidth=linewidth, alpha=alpha)
            else:
                for x, y, marker in zip(x,y,markers):
                    plt.plot(x,y,linestyle=linestyle, marker=marker, color=rand_color(), \
                        markersize=6, fillstyle='none', linewidth=linewidth, alpha=alpha)
        elif (color.ndim > 0):
            if markers.ndim == 0:
                for x, y,color in zip(x,y,color):
                    plt.plot(x,y,linestyle=linestyle, marker=marker, color=color, \
                        markersize=6, fillstyle='none', linewidth=linewidth, alpha=alpha) 
            else:
                for x, y,color, marker in zip(x,y,color,markers):
                    plt.plot(x,y,linestyle=linestyle, marker=marker, color=color, \
                        markersize=6, fillstyle='none', linewidth=linewidth, alpha=alpha)
    else:
        plt.plot(x,y,linestyle=linestyle, marker=marker, color=color, \
            markersize=6, fillstyle='none', linewidth=linewidth, alpha=alpha)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if title != False:
        plt.title(title,color='k',fontweight='bold')

    if boxoff == True:
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

    if trendline == True:
        if dim > 1:
            print('WARNING: Result likely incorrect, asking for trendline on more than one line')
        y_pred,r_squared, m, b = linear_trendline(x,y)
        plt.plot(x,y_pred,linestyle='dashed',linewidth=1,color='xkcd:black')
        if draw_eqn == True:
            textstr = 'y = {0:.2E}x + {1:.2f} \nR-squared = {2:.2f}'.format(m,b,r_squared)
            plt.text(0.5,0.0, textstr, fontsize=14, transform=plt.gcf().transFigure, horizontalalignment='center')
            plt.subplots_adjust(bottom=0.2)
        else:
            print('NOTE: To draw equations on picture, do "draw_eqn = True"')
            print('y = {0:.2E}x + {1:.2f} \nR-squared = {2:.2f}'.format(m,b,r_squared))

    if legend == True:
        if (len(label) == 1 or type(label) == str) and (label != '_'):
            if trendline == True:
                label = [label] + ['Linear Regression']
                plt.legend(label,loc=loc,edgecolor='black')
            else:
                plt.legend([label],loc=loc,edgecolor='black')
        elif (label == '_'):
            if dim > 1: 
                label = ['y_' + str(i) for i in range(len(x))]
                if trendline == True:
                    print('WARNING: Trendline doesnt make sense here since data for more than one line given')
            else: 
                label = ['y']
                if trendline == True:
                    label = label + ['Linear Regression']
            plt.legend(label,loc=loc,edgecolor='black')
        else:
            plt.legend(label,loc=loc,edgecolor='black')
            if trendline == True:
                print('WARNING: Trendline doesnt make sense here since data for more than one line given')

    if savefig == True:
        plot_num = plt.gcf().number
        if plot_num == 1:
            plt.savefig(filename + '.' + extension, format=extension, bbox_inches='tight')
            print('Plot saved to current directory as {}.{}'.format(filename,extension))
        else:
            number = str(plot_num)
            plt.savefig(filename + number + '.' + extension, format=extension, bbox_inches='tight')
            print('Plot saved to current directory as {}{}.{}'.format(filename,number,extension))


    # restore global defaults
    #mpl.rcParams.update(mpl.rcParamsDefault)
