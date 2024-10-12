Visualization
+++++++++++++

This sub package provides different helper functions for visualizing data using plots.

**Examples**

The following code cell will plot a classification report of true labels versus predicted labels.

.. code-block:: 

    from helperfns.visualization import plot_complicated_confusion_matrix, plot_images, plot_images_predictions, plot_simple_confusion_matrix,
    plot_classification_report, plot_wordcloud

    # plotting classification report
    fig, ax = plot_classification_report(labels, preds,
                        title='Classification Report',
                        figsize=(10, 5), dpi=70,
                        target_names = classes)


The ``plot_classification_report`` takes the following arguments:

+-------------+-------------------------------------------------+------+
| Argument    | Description                                     | Type |
+=============+=================================================+======+
| images      | List of images to plot                          | list |
+-------------+-------------------------------------------------+------+
| labels_true | True labels                                     | list |
+-------------+-------------------------------------------------+------+
| labels_pred | Predicted labels                                | list |
+-------------+-------------------------------------------------+------+
| classes     | List of class labels (default: [])              | list |
+-------------+-------------------------------------------------+------+
| cols        | Number of columns in the plot (default: 5)      | int  |
+-------------+-------------------------------------------------+------+
| rows        | Number of rows in the plot (default: 3)         | int  |
+-------------+-------------------------------------------------+------+
| fontsize    | Font size for labels (default: 16)              | int  |
+-------------+-------------------------------------------------+------+
| save_path   | The path to save a plotted figure (default:None)| str  |
+-------------+-------------------------------------------------+------+





The ``plot_images_predictions`` plots the image predictions. This functions is very useful when you are doing image classification.

.. code-block:: 

    # plot predicted image labels with the images
    plot_images_predictions(images, true_labels, preds, classes=["dog", "cat"] ,cols=8)


Here is the table of arguments for the ``plot_images_predictions``

.. rst-class:: my_table

+-------------+-------------------------------------------------+------+
| Argument    | Description                                     | Type |
+=============+=================================================+======+
| images      | List of images to plot                          | list |
+-------------+-------------------------------------------------+------+
| labels_true | True labels                                     | list |
+-------------+-------------------------------------------------+------+
| labels_pred | Predicted labels                                | list |
+-------------+-------------------------------------------------+------+
| classes     | List of class labels (default: [])              | list |
+-------------+-------------------------------------------------+------+
| cols        | Number of columns in the plot (default: 5)      | int  |
+-------------+-------------------------------------------------+------+
| rows        | Number of rows in the plot (default: 3)         | int  |
+-------------+-------------------------------------------------+------+
| fontsize    | Font size for labels (default: 16)              | int  |
+-------------+-------------------------------------------------+------+
| save_path   | The path to save a plotted figure (default:None | str  |
+-------------+-------------------------------------------------+------+

The ``plot_images`` functions is used to visualize images.

.. code-block:: 

    # plot the images with their labels
    plot_images(images[:24], true_labels[:24], cols=8)



The ``plot_images`` takes the following as arguments:

+-----------+-------------------------------------------------+------+
| Argument  | Description                                     | Type |
+===========+=================================================+======+
| images    | List of images to plot                          | list |
+-----------+-------------------------------------------------+------+
| labels    | List of labels corresponding to images          | list |
+-----------+-------------------------------------------------+------+
| cols      | Number of columns in the plot (default: 5)      | int  |
+-----------+-------------------------------------------------+------+
| rows      | Number of rows in the plot (default: 3)         | int  |
+-----------+-------------------------------------------------+------+
| fontsize  | Font size for labels (default: 16)              | int  |
+-----------+-------------------------------------------------+------+
| save_path | The path to save a plotted figure (default:None | str  |
+-----------+-------------------------------------------------+------+




The ``plot_simple_confusion_matrix`` is used to plot a less more verbose confusion matrix of real labels against predicted labels.

.. code-block:: 

    # plot a simple confusion matrix
    y_true = [random.randint(0, 1) for _ in range (100)]
    y_pred = [random.randint(0, 1) for _ in range (100)]
    classes =["dog", "cat"]
    plot_simple_confusion_matrix(y_true, y_pred, classes)


This function takes in the following in the following as arguments.

+-----------+-------------------------------------------------+-------+
| Argument  | Description                                     | Type  |
+===========+=================================================+=======+
| y_true    | True labels                                     | list  |
+-----------+-------------------------------------------------+-------+
| y_pred    | Predicted labels                                | list  |
+-----------+-------------------------------------------------+-------+
| classes   | List of class labels (default: [])              | list  |
+-----------+-------------------------------------------------+-------+
| figsize   | Size of the figure (default: (10, 10))          | tuple |
+-----------+-------------------------------------------------+-------+
| fontsize  | Font size for labels (default: 15)              | int   |
+-----------+-------------------------------------------------+-------+
| save_path | The path to save a plotted figure (default:None | str   |
+-----------+-------------------------------------------------+-------+


The ``plot_complicated_confusion_matrix`` is used to plot a more verbose confusion matrix of real labels against predicted labels.

.. code-block:: 

    # plot a confusion matrix with percentage value of confusion
    y_true = [random.randint(0, 1) for _ in range (100)]
    y_pred = [random.randint(0, 1) for _ in range (100)]
    classes =["dog", "cat"]
    plot_complicated_confusion_matrix(y_true, y_pred, classes)


This function takes in the following as arguments.

+-----------+-------------------------------------------------+-------+
| Argument  | Description                                     | Type  |
+===========+=================================================+=======+
| y_true    | True labels                                     | list  |
+-----------+-------------------------------------------------+-------+
| y_pred    | Predicted labels                                | list  |
+-----------+-------------------------------------------------+-------+
| classes   | List of class labels (default: [])              | list  |
+-----------+-------------------------------------------------+-------+
| figsize   | Size of the figure (default: (5, 5))            | tuple |
+-----------+-------------------------------------------------+-------+
| fontsize  | Font size for labels (default: 20)              | int   |
+-----------+-------------------------------------------------+-------+
| title     | Title of the plot (default: "Confusion Matrix") | str   |
+-----------+-------------------------------------------------+-------+
| xlabel    | Label for x-axis (default: "Predicted label")   | str   |
+-----------+-------------------------------------------------+-------+
| ylabel    | Label for y-axis (default: "True label")        | str   |
+-----------+-------------------------------------------------+-------+
| save_path | The path to save a plotted figure (default:None | str   |
+-----------+-------------------------------------------------+-------+


The ``plot_wordcloud`` function generates and plots a word cloud based on the provided corpus.

.. code-block:: 

    # Generate a word cloud from a sample text
    corpus = "This is a sample text for generating word clouds"
    plot_wordcloud(corpus, max_words=500, mask="wine")


This function takes in the following as arguments.

.. rst-class:: my__table

+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
| Argument          | Description                                             | Type                                                              |
+===================+=========================================================+===================================================================+
|| corpus           || The text or dictionary of word frequencies to generate || str or dict                                                      |
||                  || the word cloud from.                                   ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| max_words        || Maximum number of words to include in the word cloud,  || int                                                              |
||                  || default is 1,000.                                      ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
| title             | Title of the plot, default is "Word Cloud".             | str                                                               |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| mask             || The shape mask for the word cloud. Options are         || Union[Literal["head", "chicken", "wine", "apple", "tree"], None] |
||                  || "head", "chicken", "wine", "apple", "tree" or None,    ||                                                                  |
||                  || default is "tree".                                     ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| background_color || The background color of the word cloud,                || str                                                              |
||                  || default is "#E4E0E1".                                  ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| contour_width    || Width of the contour around the word cloud,            || int                                                              |
||                  || default is 1.                                          ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| contour_color    || Color of the contour around the word cloud,            || str                                                              |
||                  || default is "#D6C0B3".                                  ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| figsize          || The figure size of the word cloud plot,                || tuple                                                            |
||                  || default is (10, 10).                                   ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| fontsize         || Font size for the plot title,                          || int                                                              |
||                  || default is 15.                                         ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
|| save_path        || The path to save the plotted figure                    || str or None                                                      |
||                  || (default: None).                                       ||                                                                  |
+-------------------+---------------------------------------------------------+-------------------------------------------------------------------+
