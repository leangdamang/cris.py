**Goal:**  Create a recipe recommender based off images of items in your fridge. 

** Purpose:** I focused of healthy and fresh ingredients typically found in fridges because they’re often the items people have most difficulty cooking. they’re also the most prone to waste. Over 50% of all produce in American is thrown out annually. This equates to 160 Billion dollars wasted.

Cris.py empowers home chefs to cook any day of the week and minimizes the waste they generate.


Data: 4500 images of foods scraped from Google Images and tagged with VoTT and over 5,500 recipes scraped from SeriousEats.com


How does Cris.py work? When an image is uploaded, regions of interests (ROIs) are generated using selective search. These are areas in the picture that most likely have an object in them.

Excessive ROIs are filtered out using non-maxima suppression for efficiency sake. 

Each remaining ROI is inputted into a convolutional neural net to classify the object.

On the recipe side, I extract the nouns and adjectives from the text and create bigrams and trigrams using genism phraser. After some cleaning, these are the ingredients for each recipe

I then vectorize the ingredients

And calculate the cosine similarity between the ingredients for each recipe and the ingredients detected in the image to create the recommendation. 

Challenges & Process 

I first tried using Fast R-CNN, a process designed for quick multiple object detection originally created by Ross Gershick at Microsoft (https://github.com/rbgirshick/fast-rcnn). It does this by creating a convolutional feature map based off the pooled conv layers, then for each object proposal, a feature vector is extracted from the feature map; these vectors are fed into additional layers which produce a softmax prob for each class plus bounding coordinates for each of the classes.

I essentially took all the tagged food images and threw them into the model to train but got horrible results. It could only precisely detect 22% of the foods. 

The problem with Fast R-CNN is that while it’s a great generalized model, i needed someone more specialized to differentiate the nuances between kale and spinach. I decided to train my own food classification model using transfer learning. I took a model great at feature extraction, ResNet 18 and retrained it so that instead of detecting roses it could detect tomatoes. 

With my own classification model, I could apply it to each ROI to determine the individual ingredient within the image.

The result had a huge jump in performance. If you upload a picture of an apple to Cris.py, it can detect it accurate 93% of the time. When you give it a picture of something with multiple objects, it can detect about half of the food items precisely.  

**Results:** 50% F1 Score for detected objects, 91% F1 score for training object detection
