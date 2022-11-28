
# Detecting and Segmentation of Lungs infected with SARS-CoV-2 virus using  U-NET

### Dataset: 
The X-ray images used in this work have been collected from a radiography dataset developed by researchers from Qatar University, Doha, Qatar and the University of Dhaka, Bangladesh along with their collaborators from Pakistan and Malaysia. It has 3616 chest X-ray images each for COVID positive cases along with 10,192 Normal, 6012 Lung Opacity (Non-COVID lung infection), and 1345 Viral Pneumonia images and corresponding lung masks. The dataset also provided us with masks to segment the lung regions. These masks were generated automatically!

This is how a lung mask looks:


![COVID-7](https://user-images.githubusercontent.com/34234829/204313023-99566ed1-8511-4fc5-95b1-8e22bdfd5c29.png)

The corresponding X-ray looks like:


![COVID-7](https://user-images.githubusercontent.com/34234829/204314400-921c11c6-3bca-4570-9bd3-6dff518daba0.png)

## DETECTING  OF COVID AND NON-COVID CASES

This is the first stage of our research. The detection was done using a general CNN. Tensorflow and Sequential from Keras were used. The Sequential API adds on one layer at a time, starting from the input. The most important part are the convolutional layers Conv2D. Here they have 16-32 filters that use nine weights each to transform a pixel to a weighted average of itself and its eight neighbors. As the same nine weights are used over the whole image, the net will pick up features that are useful everywhere. As it is only nine weights, we can stack many convolutional layers on top of each other without running out of memory/time.

### Training the model: 
45 epochs with a batch size of 6 were used. One epoch occurs when a dataset is just once passed through the neural network in both directions, whereas batch size refers to the total number of training samples in a single batch. As our loss function, we use logloss which is called "binary_crossentropy" in Keras. Metrics is only used for evaluation. As optimizer, we could have used rmsprop, but Adam is faster. At the end of training, we plot a graph of accuracy and loss.

<img width="216" alt="image" src="https://user-images.githubusercontent.com/34234829/204315099-b7ef456e-644e-488c-895c-3d8caea6648f.png">
<img width="211" alt="image" src="https://user-images.githubusercontent.com/34234829/204315202-95a4d168-3206-46de-afb3-3e3cc2f9d993.png">

## SEGMENTATION OF COVID CHEST X-RAYS

Four Python scripts were created - the model, metrics, evaluation and training scripts. The training script calls all the other scripts and their functions. The dataset was imported through Google Drive to Colab. The X-ray images and corresponding masks were split into training, validation and testing sets. A function that uses OpenCV to resize the images bitwise is used before training.

## Training: 
10 epochs with a batch size of 2 is being done for training. 

## Evaluation criteria: 
Intersection over union, Dice coefficient and Dice loss are the three metrics used to evaluate.




