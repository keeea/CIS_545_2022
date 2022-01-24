# -*- coding: utf-8 -*-
"""Copy of Spring 2022 Homework 0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kARe43pLfAkQWVdahCmwSiBlmoKt3zZM

# Homework 0: Getting Started (10 points)

## Due January 24, 2022 by 10pm

For this initial assignment, our primary goal is to familiarize you with the Jupyter/Python and Apache Spark "software stack" we will use through the semester.

**This class assumes you are comfortable programming in Python.**

We will be using **Google Colab** to do the majority of work in the class, since it offers a standard environment regardless of your personal machine. This very file is a Jupyter **notebook** that you can edit and use to run Python code. Its file extension is “.ipynb” for (I)nteractive (Py)thon (N)ote(b)ook. 

Notebooks are divided into Cells. Some Cells are text (written in Markdown). You won’t need to edit these. The other Cells are executable code and will have `[ ]` to the left of them. After running one of these Cells, a number will appear inside the brackets, indicating the order in which the Cells were run.


<br>

#### **Please make a COPY of this notebook!**

Please make a COPY of this notebook when you are getting started; nobody should have edit privileges which means that while you can type and run cells here, **it will NOT save**. Make a copy to your own Colab!

# Part 1: Cloud Environment Setup

If you've gotten to this point, you have already successfully logged into Google Colab!  Most likely you'll want to ``Save a Copy in Drive`` for your own use as you edit your code.  We suggest you don't rename the file as you do so.

Since this initial homework uses the whole "big data" stack, including Apache Spark, we will first need to do some software setup.

Generally speaking we will be running command-line options (eg to install software on the host machine) using the `!` operation, and we will be using `pip` to install Python libraries.

## 1.1 Installing Spark on Google Colab

For big data analysis on a cluster, we'll need to learn to use Apache Spark.  You don't need to fully follow the details here to install Spark on Colab, but you do need to execute the cell!

Select it and hit [Shift]-[Enter] to run, or click on the "play" triangle to the left.
"""

## Let's install Apache Spark on Colab

!wget https://downloads.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
!tar xf spark-3.2.0-bin-hadoop3.2.tgz
!pip install findspark

import os

os.environ["SPARK_HOME"] = "/content/spark-3.2.0-bin-hadoop3.2"

"""Good, the software should be installed.

Now you need to run three more Cells that configure Jupyter for Apache Spark, set up the environment, and connect to Spark.
"""

import findspark

findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql import SQLContext

try:
    if(spark == None):
        spark = SparkSession.builder.appName('Initial').getOrCreate()
        sqlContext=SQLContext(spark)
except NameError:
    spark = SparkSession.builder.appName('Initial').getOrCreate()
    sqlContext=SQLContext(spark)

"""## 1.2 Autograding and the PennGrader

<img align="right" src = "https://imgur.com/rNd3gIg.png" width= "200"/>

Next you'll need to set up the PennGrader, which we'll be using throughout the semester to help you with your homeworks.

PennGrader is not only **awesome**, but it was built by an equally awesome person: CIS 545 alumnus, Leo Murri, who later became a TA for the course.  Today Leo works as a data scientist at Amazon!

PennGrader was developed to provide students with *instant* feedback on their answer. You can submit your answer and know whether it's right or wrong instantly. We then record your most recent answer in our backend database.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install penngrader
#

"""Let's try it out! Fill in the cell below with your 8-digit Penn ID and then run the following cell to initialize the grader."""

#PLEASE ENSURE YOUR PENN-ID IS ENTERED CORRECTLY. IF NOT, THE AUTOGRADER WON'T KNOW WHO 
#TO ASSIGN POINTS TO YOU IN OUR BACKEND
STUDENT_ID = 938033441 # YOUR PENN-ID GOES HERE AS AN INTEGER#

import penngrader.grader

grader = penngrader.grader.PennGrader(homework_id = 'CIS545_Spring_2022_HW0', student_id = STUDENT_ID)

"""# Part 2: Your First CIS 545 Notebook

The rest of the assignment will try to illustrate a few aspects of data analytics...  Don't be concerned if you don't yet know all of the operations, libraries, etc. because that's what we'll be covering soon!

## 2.1 A Simple Program to Read from the Web and Invoke Spark

The cell below uses the **Pandas** library to read a table from the given web page (the Wikipedia information on films in the year 2010).  The code loads this into a list of **DataFrame**s called `films_2010`.  We then pull the table at index 3, then do some simple **data wrangling** on `top_films` to set up the appropriate types.

Select the Cell below and then select the Run button which appeared over the brackets.
"""

!pip install money-parser

import pandas as pd
from money_parser import price_dec

def extract_number(x):
  return round(price_dec(x) / 1000000, 2)

films_2010 = pd.read_html('https://en.wikipedia.org/wiki/2010_in_film')

top_films = films_2010[3]

top_films.set_index('Rank', inplace=True)

top_films['Revenue (millions)'] = top_films['Worldwide gross'].apply(extract_number)

top_films

"""Can we programmatically compute how many entries were scored as top films?"""

# You can use the Python len() function on a dataframe to figure out how many rows!

# TODO: Update dataframe_length with your code here!
dataframe_length = len(top_films)

# Run this cell to submit to PennGrader!

grader.grade(test_case_id = 'length_test', answer = dataframe_length)

"""Now we will copy the table over to **Apache Spark**, which is a big data engine capable of processing giant tables.

We will **query** the table to get top films from Disney.
"""

from pyspark.sql.types import *

# The 'schema' specifies the column names and data types
schema = StructType([StructField('Title', StringType(), nullable=True), \
            StructField('Distributor', StringType(), nullable=False), \
            StructField('Gross', StringType(), nullable=False), \
            StructField('Revenue_M', DecimalType(), nullable=False)])

# This loads a Pandas DataFrame into Apache Spark
top_films_spark = spark.createDataFrame(top_films, \
                                         schema=schema)

# Now use Spark to filter only those rows where the distributor is 'Disney'
disney_films = top_films_spark.filter(top_films_spark.Distributor == 'Disney')
display(disney_films.collect())

"""Congratulations, you have just run a very simple Spark program!

## 2.2 Something a Little More Fun
Running the cell below will create a scatter plot. 

**Your task is to edit this cell such that:***

1. The text (which says “CIS 545 student”) should be replaced with your full name.
2. The number of values sampled should be 500, and you should  change the figure title to match.

4. The x-axis should be labeled “Index”.

You may run this cell repeatedly to see the output.
"""

# Commented out IPython magic to ensure Python compatibility.
# We’ll be using Matplotlib to plot a visualization
# %matplotlib inline

import matplotlib.pyplot as plt
import numpy as np

# Create a Spark dataset with values 0 thru 499
rdd = spark.sparkContext.parallelize(range(500))

# TODO: change this line so we sample 500 values
# Sample 625 values from the RDD
y = np.array(rdd.takeSample(True, 500, 1))
# Create an array with the indices
x = np.array(range(len(y)))

# Create a plot with a caption, X and Y legends, etc
x_label = 'index'
y_label = 'Value'
student = 'Lan Xiao'

plt.title(str(len(y)) + ' random samples from the RDD')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.figtext(0.995, 0.01, student, ha='right', va='bottom')
# Scatter plot that fits within the box
plt.scatter(x, y)
plt.tight_layout()

# Now fit a trend line to the data and plot it over the scatter plot
m, c = np.polyfit(x, y, 1)
plt.plot(x, m*x + c)

# Save the SVG
plt.savefig('hw0.svg')

"""The following test cell prints your name and tests whether you followed the directions."""

print("Your name is:", student)

# Run this cell to submit to PennGrader!
grader.grade(test_case_id = 'name_test', answer = student)

"""Part 3: Submitting Your Homework

First, note that it's easy to "break" your notebook by changing something...  So you should *ALWAYS* clear output and re-run your code, just to make sure that hasn't happened.

When you are done, select the "Runtime" menu at the top of the window. Then, select "Restart and run all". Please make sure all cells complete!

## 3.1 Submission to Gradescope

Now go to the File menu and choose "Download .ipynb".  Go to [Gradescope](https://www.gradescope.com/courses/343777) and:

1. From "File" --> Download both .ipynb and .py files
1. Name these files `homework0.ipynb` and `homework0.py` respectively
1. Sign in using your Penn email address (if you are a SEAS student we recommend using the Google login) and ensure  your class is "SRS_CIS-545-001 2022A"
1. Select Homework 0
1. Upload both files
1. PLEASE CHECK THE AUTOGRADER OUTPUT TO ENSURE YOUR SUBMISSION IS PROCESSED CORRECTLY!

You should be set! Note that this assignment has 8 autograded points and 2 manually graded points! The autograded points will show upon submission, but the manually graded portion will be graded by your TAs after the deadline has passed.
"""