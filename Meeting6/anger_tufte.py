from __future__ import division
from random import choice
from collections import defaultdict
import matplotlib.pyplot as plt
from math import log


def make_microbiome(total=10000000,common=0.70,uncommon=0.25,rare=0.04,very_rare=0.004,\
    uber_rare=0.0004,most_rare=0.00001):
    """Simulate a very simple, easy to interpret microbiome
    NOTE: this is just a simple demo real simulations would use a 
    specific distribution of rare vs. abundant species
    
    """
    microbiome = ['OTU1']*int(common*total)+\
      ['OTU2']*int(uncommon*total)+\
      ['OTU3']*int(rare*total)+\
      ['OTU4']*int(very_rare*total)+\
      ['OTU5']*int(very_rare*total)+\
      ['OTU6']*int(uber_rare*total)+\
      ['OTU7']*int(uber_rare*total)+\
      ['OTU8']*int(uber_rare*total)+\
      ['OTU9']*int(uber_rare*total)+\
      ['OTU10']*int(uber_rare*total)+\
      ['OTU11']*int(most_rare*total)
    
    return microbiome

def sample_microbiome(microbiome,depth):
    """Sample a list of OTUs
    microbiome -- a list of strings representing OTUs
    depth -- depth to sample as int
    """
    counts = defaultdict(int)
    for i in range(depth):
        read = (choice(microbiome)) 
        counts[read] += 1
    return counts

def obs_species(counts):
    """Returns the number of observed species
    counts -- defaultdict of species counts"""
    return(len(counts))

def rarefaction_graph(x,y,outfile="rarefaction.png",fontsize=16,font="Arial"):
    """Graph species vs. sampling effort
    x -- a list of x values
    y -- a list of y values
    outfile -- path to save the graph.  Note that the .png extension is important, as matplotlib 
    guesses output filetype based on suffix

    Hat tip to Stack Overflow on an elegant stategy for adjusting font sizes: 
    http://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    """
    ax =plt.subplot()
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontname(font)
        #Randomly adjust the label size 
        label.set_fontsize(fontsize + choice(([5,2,1,-1,-2,-5]))) 

    # Set the font dictionaries (for plot title and axis titles)
    title_font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal',
              'verticalalignment':'bottom'} 
    x_axis_font = {'fontname':'Arial', 'size':'8'}
    y_axis_font = {'fontname':'Times New Roman', 'size':'22'}
    
    #Plot the results with a thick yellow dot-dashed line
    plt.plot(x,y,c='yellow',linestyle='-.',linewidth=3.0)
    
    #Add heavy black and yellow gridlines
    plt.grid(b=True, which='major', color='y', linestyle='-',linewidth=4.0)
    
    #Turn on minor ticks so you can see our minor gridlines
    plt.minorticks_on()
    #Now make some beautfiful thick minor gridlines
    plt.grid(b=True, which='minor', color='pink', linestyle='-',linewidth=2.0)
 
    #Set y-axis limits
    ax.set_ylim([0,12])

    #Fill the area between the line and the x-axis 
    ax.fill_between(x,y,hatch='*',facecolor='r',edgecolor='none')
    
    #Change two axes to be colorful
    ax.spines['top'].set_color('pink') 
    ax.spines['right'].set_color('blue')
    
    #Set the background color
    ax.set_axis_bgcolor('purple')
    
    #Show ticks just on bottom left
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    #Set unique font styles for x and y axis
    plt.ylabel('Observed OTUs',**y_axis_font)
    plt.xlabel('Sampling Depth',**x_axis_font)
    plt.savefig(outfile)    

if __name__ == "__main__":
    #This script simulates sampling from microbiomes of various
    #depths, then makes horrible graphs representing them.
    #Your task is to fix the rarefaction_graph function so that 
    #the graphs are less awful.

    #Generate a list of strings representing a microbiome
    microbiome = make_microbiome(total=1000000)
    
    
    graph_depths = [50,500,1000]
    sampling_depths = range(10,1010,10)
    x = []
    y = []
    iterations = 5
    for sampling_depth in sampling_depths: 
        curr_counts = []
        for i in range(iterations):
            microbiome_sample = sample_microbiome(microbiome,sampling_depth)
            curr_count = obs_species(microbiome_sample)
            curr_counts.append(curr_count)
        counts = sum(curr_counts)/len(curr_counts)
        x.append(sampling_depth)
        y.append(counts)
        if sampling_depth in graph_depths:
            rarefaction_graph(x,y,outfile="rarefaction_%i"%sampling_depth)
            print("Outputing chart: rarefaction_%i"%sampling_depth) 
