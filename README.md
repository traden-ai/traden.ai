<h1 align="center">traden.ai</h1>

<div align="center">
  <img align="center" src="images/traden_ai.jpg" alt="Traden" width="200">
</div>

<p align="center">
  <a href="#about">About</a> •
  <a href="#technologies">Technologies</a> •
  <a href="#installation">Installation</a> •
  <a href="#run">Run</a> •
  <a href="#demo">Demo</a> •
  <a href="#contributing">Contributing</a>
  </p>

# About
<br/>

Our plataform allows users to create different models for stock trading, namely the creation of arbitrary tecniques to buy or sell a stock derived from a given understanding of the behavior of the stock's price. 
<br/>
 
After the creation of models, the user can see how the model would perform for a given period time, and for a given number of specified stocks. 
<br/>

In the traden ecosystem you can also find some very interesting mechanisms to combine different models, which then can be tested using backtesting techniques.  


# Technologies

* Require download
  * [Python3](https://www.python.org/)
  * [TensorFlow](https://www.tensorflow.org/)
  * [Keras](https://keras.io/)
  * [Scikit-Learn](https://scikit-learn.org/stable/)
* No download required
  * [Amazon Web Services](https://aws.amazon.com/)

# Installation

1. Clone the repository into your local computer
2. Install Python3
3. Install Python Libraries
    <br/>
    3.1 Boto3 (pip3 install boto3)
    <br/>
    3.2 TensorFlow (pip3 install tensorflow)
    <br/>
    3.3 Keras (pip3 install keras)
    <br/>
    3.4 Json Encoder (pip3 install json-encoder)
    <br/>
    3.5 Scikit-Learn (pip3 install scikit-learn)
    <br/>
<br/>

4. (Optional) Set the PYTHONPATH environment variable to the StockTradingSimulator directory in the source file of your operating system (for example bashrc in some linux operating systems)

Note: You can use the commands in parentheses, to install the respetive dependencies in the command line (assuming you have pip3 installed).


# Run

1. Set the PYTHONPATH environment variable to the StockTradingSimulator directory
2. Run the app file using a python interpreter

Note: We recommend the use of IDE such as [PyCharm](https://www.jetbrains.com/pycharm/) with running features already integrated which automatically set the environment variables.

# Demo

This is a demo for a model simulation:

1. Starting the app

<img src="images/demo_1.png" alt="Traden" width="400">

2. Selecting a Simulation

<img src="images/demo_2.png" alt="Traden" width="400">

3. Seeing the Results

<img src="images/demo_3.png" alt="Traden" width="400">

4. Extra Details
    <br/>
    4.1 Graph

    <img src="images/demo_4_1.png" alt="Traden" width="400">

    4.2 Simulation History
    
    <img src="images/demo_4_2.png" alt="Traden" width="400">

# Contributing

Your contributions are always welcome! Please have a look at the contribution guidelines first.
