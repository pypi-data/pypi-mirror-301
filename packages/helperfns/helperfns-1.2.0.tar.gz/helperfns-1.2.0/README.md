### `helperfns`

🎀 This is a python package that contains some helper functions for machine leaning.

<p align="center">
   <img src="https://github.com/CrispenGari/helperfns/blob/main/images/logo.png?raw=true" alt="logo" width="60%"/>
</p>

---

<p align="center">
  <a href="https://pypi.python.org/pypi/helperfns"><img src="https://badge.fury.io/py/helperfns.svg"></a>
  <a href="https://github.com/crispengari/helperfns/actions/workflows/CI.yml"><img src="https://github.com/crispengari/helperfns/actions/workflows/CI.yml/badge.svg"></a>
  <a href="/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green"></a>
  <a href="https://pypi.python.org/pypi/helperfns"><img src="https://img.shields.io/pypi/pyversions/helperfns.svg"></a>
</p>

### Table of Contents

- [`helperfns`](#helperfns)
- [Table of Contents](#table-of-contents)
- [Getting started](#getting-started)
- [Usage](#usage)
- [tables](#tables)
- [text](#text)
- [utils](#utils)
- [visualization](#visualization)
- [Contributing to `helperfns`.](#contributing-to-helperfns)
- [Documentation](#documentation)
- [License](#license)

### Getting started

To start using `helperfns` in your project you run the following command:

```shell
pip install helperfns
```

Or if you wan to install it in notebooks such as jupyter notebooks you can run the code cell with the following code:

```shell
!pip install helperfns
```

### Usage

The `helperfns` package is made up of different sub packages such as:

1. tables
2. text
3. utils
4. visualization

### tables

In the tables sub package you can print your data in tabular form for example:

```python
from helperfns.tables import tabulate_data

column_names = ["SUBSET", "EXAMPLE(s)", "Hello"]
row_data = [["training", 5, 4],['validation', 4, 4],['test', 3, '']]
tabulate_data(column_names, row_data)

```

Output:

```shell
Table
+------------+------------+-------+
| SUBSET     | EXAMPLE(s) | Hello |
+------------+------------+-------+
| training   |          5 |     4 |
| validation |          4 |     4 |
| test       |          3 |       |
+------------+------------+-------+
```

The following is the table of arguments for the `tabulate_data` helper function

| Argument       | Description          | Type   |
| -------------- | -------------------- | ------ |
| `column_names` | List of column names | `list` |
| `data`         | Data to be tabulated | `list` |
| `title`        | Title of the table   | `str`  |

### text

The text package offers two main function which are `clean_sentence`, `de_contract`, `generate_ngrams` and `generate_bigrams`

```python
from helperfns.text import *

# cleans the sentence
print(clean_sentence("text 1 # https://url.com/bla1/blah1/"))

```

Here is the table of arguments for the `clean_sentence` helper function.

| Argument | Description                                   | Type   |
| -------- | --------------------------------------------- | ------ |
| `sent`   | Input sentence                                | `str`  |
| `lower`  | Flag to convert to lower case (default: True) | `bool` |

You can get the list of english words as follows:

```py
# list of all english words
print(english_words)
```

You can use the `de_contract` to de-contact strings as follows

```py
# converts strings like `I'm` to 'I am'
print(de_contract("I'm"))

```

Here is the table of arguments for the `de_contract` function.

| Argument | Description         | Type  |
| -------- | ------------------- | ----- |
| `word`   | Word to de-contract | `str` |

The `generate_bigrams` is responsible for generating bi grams from list of words. Here is how you can use the function

```py
# generate bigrams from a list of word
print(text.generate_bigrams(['This', 'film', 'is', 'terrible']))
```

Here is the table of arguments for the `generate_bigrams` function:

| Argument | Description            | Type   |
| -------- | ---------------------- | ------ |
| `x`      | List of input elements | `list` |

The `generate_ngrams` generate the n-grams from a list of words, here is an example on how you can use this function

```py
# generates n-grams from a list of words
print(text.generate_ngrams(['This', 'film', 'is', 'terrible']))

```

Here is the table of arguments for the `generate_ngrams` function:

| Argument | Description                                         | Type   |
| -------- | --------------------------------------------------- | ------ |
| `x`      | List of input elements                              | `list` |
| `grams`  | Number of grams for generating n-grams (default: 3) | `int`  |

### utils

utils package comes with a simple helper function for converting seconds to hours, minutes and seconds.

Example:

```python
from helperfns.utils import hms_string

start = time.time()
for i in range(100000):
   pass
end = time.time()

print(hms_string(end - start))
```

Output:

```shell
'0:00:00.01'
```

The `hms_string` takes in the following as arguments.

| Argument      | Description                     | Type  |
| ------------- | ------------------------------- | ----- |
| `sec_elapsed` | Time in seconds to be converted | `Any` |

### visualization

This sub package provides different helper functions for visualizing data using plots.

Examples:

The following code cell will plot a classification report of true labels versus predicted labels.

```python
from helperfns.visualization import plot_complicated_confusion_matrix, plot_images, plot_images_predictions, plot_simple_confusion_matrix,
plot_classification_report

# plotting classification report
fig, ax = plot_classification_report(labels, preds,
                    title='Classification Report',
                    figsize=(10, 5), dpi=70,
                    target_names = classes)
```

The `plot_classification_report` takes the following arguments:

| Argument        | Description                                          | Type            |
| --------------- | ---------------------------------------------------- | --------------- |
| `y_true`        | True labels                                          | `list`          |
| `y_pred`        | Predicted labels                                     | `list`          |
| `title`         | Title of the plot (default: "Classification Report") | `str`           |
| `figsize`       | Size of the figure (default: (10, 5))                | `tuple`         |
| `dpi`           | Resolution of the figure (default: 70)               | `int`           |
| `save_fig_path` | Path to save the figure (default: None)              | `Any` or `None` |
| \*\*kwargs      | Additional keyword arguments                         | `Any`           |

The `plot_images_predictions` plots the image predictions. This functions is very useful when you are doing image classification.

```py
# plot predicted image labels with the images
plot_images_predictions(images, true_labels, preds, classes=["dog", "cat"] ,cols=8)
```

Here is the table of arguments for the `plot_images_predictions`.

| Argument      | Description                                | Type   |
| ------------- | ------------------------------------------ | ------ |
| `images`      | List of images to plot                     | `list` |
| `labels_true` | True labels                                | `list` |
| `labels_pred` | Predicted labels                           | `list` |
| `classes`     | List of class labels (default: [])         | `list` |
| `cols`        | Number of columns in the plot (default: 5) | `int`  |
| `rows`        | Number of rows in the plot (default: 3)    | `int`  |
| `fontsize`    | Font size for labels (default: 16)         | `int`  |

The `plot_images` functions is used to visualize images.

```py
# plot the images with their labels
plot_images(images[:24], true_labels[:24], cols=8)

```

The `plot_images` takes the following as arguments:

| Argument   | Description                                | Type   |
| ---------- | ------------------------------------------ | ------ |
| `images`   | List of images to plot                     | `list` |
| `labels`   | List of labels corresponding to images     | `list` |
| `cols`     | Number of columns in the plot (default: 5) | `int`  |
| `rows`     | Number of rows in the plot (default: 3)    | `int`  |
| `fontsize` | Font size for labels (default: 16)         | `int`  |

The `plot_simple_confusion_matrix` is used to plot a less more verbose confusion matrix of real labels against predicted labels.

```py
# plot a simple confusion matrix
y_true = [random.randint(0, 1) for _ in range (100)]
y_pred = [random.randint(0, 1) for _ in range (100)]
classes =["dog", "cat"]
plot_simple_confusion_matrix(y_true, y_pred, classes)


```

This function takes in the following in the following as arguments.

| Argument   | Description                            | Type    |
| ---------- | -------------------------------------- | ------- |
| `y_true`   | True labels                            | `list`  |
| `y_pred`   | Predicted labels                       | `list`  |
| `classes`  | List of class labels (default: [])     | `list`  |
| `figsize`  | Size of the figure (default: (10, 10)) | `tuple` |
| `fontsize` | Font size for labels (default: 15)     | `int`   |

The `plot_complicated_confusion_matrix` is used to plot a more verbose confusion matrix of real labels against predicted labels.

```py
# plot a confusion matrix with percentage value of confusion
y_true = [random.randint(0, 1) for _ in range (100)]
y_pred = [random.randint(0, 1) for _ in range (100)]
classes =["dog", "cat"]
plot_complicated_confusion_matrix(y_true, y_pred, classes)
```

This function takes in the following as arguments.

| Argument   | Description                                     | Type    |
| ---------- | ----------------------------------------------- | ------- |
| `y_true`   | True labels                                     | `list`  |
| `y_pred`   | Predicted labels                                | `list`  |
| `classes`  | List of class labels (default: [])              | `list`  |
| `figsize`  | Size of the figure (default: (5, 5))            | `tuple` |
| `fontsize` | Font size for labels (default: 20)              | `int`   |
| `title`    | Title of the plot (default: "Confusion Matrix") | `str`   |
| `xlabel`   | Label for x-axis (default: "Predicted label")   | `str`   |
| `ylabel`   | Label for y-axis (default: "True label")        | `str`   |

The `plot_wordcloud` function generates and plots a word cloud based on the provided corpus.

```python
# Generate a word cloud from a sample text
corpus = "This is a sample text for generating word clouds"
plot_wordcloud(corpus, max_words=500, mask="wine")

```

This function takes in the following as arguments.

| Argument           | Description                                                                                                           | Type                                                               |
| ------------------ | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `corpus`           | The text or dictionary of word frequencies to generate the word cloud from.                                           | `str` or `dict`                                                    |
| `max_words`        | Maximum number of words to include in the word cloud, default is 1,000.                                               | `int`                                                              |
| `title`            | Title of the plot, default is "Word Cloud".                                                                           | `str`                                                              |
| `mask`             | The shape mask for the word cloud. Options are "head", "chicken", "wine", "apple", "tree" or None, default is "tree". | `Union[Literal["head", "chicken", "wine", "apple", "tree"], None]` |
| `background_color` | The background color of the word cloud, default is "#E4E0E1".                                                         | `str`                                                              |
| `contour_width`    | Width of the contour around the word cloud, default is 1.                                                             | `int`                                                              |
| `contour_color`    | Color of the contour around the word cloud, default is "#D6C0B3".                                                     | `str`                                                              |
| `figsize`          | The figure size of the word cloud plot, default is (10, 10).                                                          | `tuple`                                                            |
| `fontsize`         | Font size for the plot title, default is 15.                                                                          | `int`                                                              |
| `save_path`        | The path to save the plotted figure (default: None).                                                                  | `str` or `None`                                                    |

### Contributing to `helperfns`.

To contribute to `helperfns` read the [CONTRIBUTION.md](https://github.com/CrispenGari/helperfns/blob/main/CONTRIBUTION.md) file.

### Documentation

You can read the full [documentation](https://helperfns.readthedocs.io/en/latest/) here.

### License

This project is licensed under the MIT License - see the [LICENSE](/LISENSE) file for details.
