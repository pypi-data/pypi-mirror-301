import os
import matplotlib.pyplot as plt
import itertools
import numpy as np
import pandas as pd
import seaborn as sns
import wordcloud as wc
import pathlib
import matplotlib as mpl
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
)
from PIL import Image
from typing import Union, Literal



this = os.path.dirname(__file__)


def plot_simple_confusion_matrix(
    y_true: list,
    y_pred: list,
    classes: list = [],
    figsize: tuple = (10, 10),
    fontsize: int = 15,
    save_path: str | None = None,
):
    """
    Plot Complicated Confusion Matrix

    This function simply plots a confusion matrix.

    Parameters
    ----------
    y_true : list
        Takes in a collection of true labels.
    y_pred : list
        Takes in a collection of predicted labels.

    Keyword Args
    ------------
    classes : list
        A list of class name e.g ['dog', 'cat'] default is y_true.
    figsize : tuple
        The figsize of the confusion matrix plot default is (10, 10);
    fontsize : int
        Font size for the contents of the confusion matrix, default is 15.
    save_path : str | None
        The path to save the plot, default is None.
    save_path : str | None, defaut=None
        Full path where to save the plot. Will generate the folders if they don't exist already.

    Returns
    -------
    None

    See Also
    --------
    plot_wordcloud: Plots a word cloud from text or word frequencies.
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_images: Plots the images and display them.
    plot_images_predictions: Plots the images with their predictions and display them.
    plot_classification_report: Plots the classification report.

    Examples
    --------
    >>> y_true = [random.randint(0, 1) for _ in range (100)]
    >>> y_pred = [random.randint(0, 1) for _ in range (100)]
    >>> classes =["dog", "cat"]
    >>> plot_complicated_confusion_matrix(y_true, y_pred, classes)
    """
    assert (
        len(y_true) == len(y_pred)
    ), f"The length of predicted and real labels must be equal, received {len(y_pred)} and {len(y_true)}."

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    cm = confusion_matrix(y_true, y_pred)

    if len(classes) == 0:
        classes = list(set(y_true))

    cm = ConfusionMatrixDisplay(cm, display_labels=classes)
    cm.plot(values_format="d", cmap="Blues", ax=ax)

    if save_path is not None:
        plt.savefig(save_path)
    plt.xticks(rotation=20, color="black", fontsize=fontsize)
    plt.yticks(rotation=20, color="black", fontsize=fontsize)
    plt.show()


def plot_complicated_confusion_matrix(
    y_true: list,
    y_pred: list,
    classes: list = [],
    figsize: tuple = (5, 5),
    fontsize: int = 20,
    title: str = "Confusion Matrix",
    xlabel: str = "Predicted label",
    ylabel: str = "True label",
    save_path: str | None = None,
):
    """
    Plot Complicated Confusion Matrix

    This function simply plots a confusion matrix with some percentage(%) of confusion between class labels.

    Parameters
    ----------
    y_true : list
        Takes in a collection of true labels.
    y_pred : list
        Takes in a collection of predicted labels.

    Keyword Args
    ------------
    classes : list
        A list of class name e.g ['dog', 'cat'].
    figsize : turple
        The figsize of the confusion matrix plot
    title : str
        The title to display for the confusion matrix, default is 'Confusion Matrix' .
    xlabel : str
        The x-axis label, default is 'True label'.
    ylabel : str
        The y-axis label, default is 'Predicted label'.
    fontsize : int
        Font size for the contents of the confusion matrix, default is 20.
    save_path : str | None, defaut=None
        Full path where to save the plot. Will generate the folders if they don't exist already.

    Returns
    -------
    None

    See Also
    --------
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images: Plots the images and display them.
    plot_images_predictions: Plots the images with their predictions and display them.
    plot_classification_report: Plots the classification report.
    plot_wordcloud: Plots a word cloud from text or word frequencies.

    Examples
    --------
    >>> y_true = [random.randint(0, 1) for _ in range (100)]
    >>> y_pred = [random.randint(0, 1) for _ in range (100)]
    >>> classes =["dog", "cat"]
    >>> plot_simple_confusion_matrix(y_true, y_pred, classes)
    """

    assert (
        len(y_true) == len(y_pred)
    ), f"The length of predicted and real labels must be equal, received {len(y_pred)} and {len(y_true)}."
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    n_classes = cm.shape[0]

    fig, ax = plt.subplots(figsize=figsize)
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    fig.colorbar(cax)

    if len(classes):
        labels = classes
    else:
        labels = np.arange(cm.shape[0])

    ax.set(
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        xticks=np.arange(n_classes),
        yticks=np.arange(n_classes),
        xticklabels=labels,
        yticklabels=labels,
    )
    ax.yaxis.label.set_color("green")
    ax.xaxis.label.set_color("green")

    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()

    threshold = (cm.max() + cm.min()) / 2.0
    # Plot the text on each cell
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
            horizontalalignment="center",
            color="white" if cm[i, j] > threshold else "black",
            size=fontsize,
        )
    if save_path is not None:
        plt.savefig(save_path)
    plt.show()


def plot_images(
    images: list,
    labels: list,
    cols: int = 5,
    rows: int = 3,
    fontsize: int = 16,
    save_path: str | None = None,
) -> None:
    """
    Plot images

    This function simply plots Images with their labels.

    Parameters
    ----------
    images : list
        Takes in a collection of images.
    labels : list
        Takes in a collection of image labels.

    Keyword Args
    ------------
    cols : int
        Number of columns for images, default is 5.
    rows : int
        Number of rows for images, default is 3
    fontsize : int
        Font size for labels, default is 16.
    save_path : str | None, defaut=None
        Full path where to save the plot. Will generate the folders if they don't exist already.

    Returns
    -------
    None

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images_predictions: Plots the images with their predictions and display them.
    plot_classification_report: Plots the classification report.
    plot_wordcloud: Plots a word cloud from text or word frequencies.

    Examples
    --------
    >>> plot_images(images[:24], true_labels[:24], cols=8)
    """

    assert (
        len(images) == len(labels)
    ), f"The length for images and labels must match but got {len(images)} {len(labels)}"

    fig = plt.figure()
    fig.set_size_inches(cols * 2, rows * 2)
    for i, (image, label) in enumerate(zip(images, labels)):
        plt.subplot(rows, cols, i + 1)
        plt.axis("off")
        plt.imshow(image, cmap="gray")
        plt.title(label, color="g", fontsize=fontsize)

    if save_path is not None:
        path = pathlib.Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path)
    plt.show()


def plot_images_predictions(
    images: list,
    labels_true: list,
    labels_pred: list,
    classes: list = [],
    cols: int = 5,
    rows: int = 3,
    fontsize: int = 16,
    save_path: str | None = None,
) -> None:
    """
    Plot images predictions

    This function simply plots predicted images. Images with wrongly predicted labels their
    labels will be red and green otherwise.

    Parameters
    ----------
    images : list
        Takes in a collection of images.
    labels_true : list
        Takes in a collection of correct labels.
    labels_pred : list
        Takes in a collection of predicted labels.

    Keyword Args
    ------------
    classes : list
        Takes in a collection  of class labels example can be ['cat', 'dog'] if
        not passed then labels_pred will be used.
    cols : int
        Number of columns for images, default is 5.
    rows : int
        Number of rows for images, default is 3
    fontsize : int
        Font size for labels, default is 16.
    save_path : str | None, defaut=None
        Full path where to save the plot. Will generate the folders if they don't exist already.

    Returns
    -------
    None

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images: Plots the images and display them.
    plot_classification_report: Plots the classification report.
    plot_wordcloud: Plots a word cloud from text or word frequencies.

    Examples
    --------
    >>> plot_images_predictions(images, true_labels, preds, classes=["dog", "cat"] ,cols=8)

    """
    assert (
        len(images) == len(labels_true) == len(labels_pred)
    ), f"The image classes, true labels and predicted labels must be equal but received {len(images)}, {len(labels_true)} and {len(labels_pred)}."

    fig = plt.figure()
    fig.set_size_inches(cols * 2, rows * 2)
    if len(classes):
        classes = classes
    else:
        classes = list(set(labels_pred))

    for i, (image, label_true, label_pred) in enumerate(
        zip(images, labels_true, labels_pred)
    ):
        plt.subplot(rows, cols, i + 1)
        plt.axis("off")
        plt.imshow(image, cmap="gray")
        plt.title(
            classes[label_true],
            color="g" if label_true == label_pred else "r",
            fontsize=fontsize,
        )

    if save_path is not None:
        path = pathlib.Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path)
    plt.show()


def plot_classification_report(
    y_true: list,
    y_pred: list,
    title: str = "Classification Report",
    figsize: tuple = (10, 5),
    dpi: int = 70,
    save_path: str | None = None,
    **kwargs,
):
    """
    Plot Classification Report

    Parameters
    ----------
    y_true : pandas.Series or list of shape (n_samples,)
        Targets.
    y_pred : pandas.Series or list of shape (n_samples,)
        Predictions.
    title : str, default = 'Classification Report'
        Plot title.
    fig_size : tuple, default = (10, 5)
        Size (inches) of the plot.
    dpi : int, default = 70
        Image DPI.
    save_path : str | None, defaut=None
        Full path where to save the plot. Will generate the folders if they don't exist already.
    **kwargs : attributes of classification_report class of sklearn

    Returns
    -------
        fig : Matplotlib.pyplot.Figure
            Figure from matplotlib
        ax : Matplotlib.pyplot.Axe
            Axe object from matplotlib

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_simple_confusion_matrix : Plots a simple confusion matrix.
    plot_images: Plots the images and display them.
    plot_images_predictions: Plots the images with their predictions and display them.
    plot_wordcloud: Plots a word cloud from text or word frequencies.

    Examples
    --------
    >>> fig, ax = plot_classification_report(labels, preds,
                    title='Classification Report',
                    figsize=(10, 5), dpi=70,
                    target_names = classes)
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    clf_report = classification_report(y_true, y_pred, output_dict=True, **kwargs)
    keys_to_plot = [
        key
        for key in clf_report.keys()
        if key not in ("accuracy", "macro avg", "weighted avg")
    ]
    df = pd.DataFrame(clf_report, columns=keys_to_plot).T
    # the following line ensures that dataframe are sorted from the majority classes to the minority classes
    df.sort_values(by=["support"], inplace=True)

    # first, let's plot the heatmap by masking the 'support' column
    _rows, cols = df.shape
    mask = np.zeros(df.shape)
    mask[:, cols - 1] = True
    ax = sns.heatmap(
        df,
        mask=mask,
        annot=True,
        cmap="Blues",
        fmt=".3g",
        vmin=0.0,
        vmax=1.0,
        linewidths=2,
        linecolor="white",
    )

    # then, let's add the support column by normalizing the colors in this column
    mask = np.zeros(df.shape)
    mask[:, : cols - 1] = True

    ax = sns.heatmap(
        df,
        mask=mask,
        annot=True,
        cbar=False,
        linewidths=2,
        linecolor="white",
        fmt=".0f",
        vmin=df["support"].min(),
        vmax=df["support"].sum(),
        norm=mpl.colors.Normalize(vmin=df["support"].min(), vmax=df["support"].sum()),
    )

    plt.title(title)
    plt.xticks(rotation=45)
    plt.yticks(rotation=360)

    if save_path is not None:
        path = pathlib.Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path)
    return fig, ax


def plot_wordcloud(
    corpus: str | dict,
    max_words: int = 1_000,
    title: str = "Word Cloud",
    mask: Union[Literal["head", "chicken", "wine", "apple", "tree"], None] = "tree",
    background_color: str = "#E4E0E1",
    contour_width: int = 1,
    contour_color: str = "#D6C0B3",
    figsize: tuple = (10, 10),
    fontsize: int = 15,
    save_path: str | None = None,
) -> None:
    """
    Plot Word Cloud

    This function generates and plots a word cloud based on the provided corpus.
    It allows the use of different masks (shapes), word limits, and customizable
    colors and appearance.

    Parameters
    ----------
    corpus : str | dict
        The text or dictionary of word frequencies to generate the word cloud from.
    max_words : int, optional
        Maximum number of words to include in the word cloud, default is 1,000.
    title : str, optional
        Title of the plot, default is "Word Cloud".
    mask : Literal["head", "chicken", "wine"] | None, optional
        The shape mask for the word cloud. Options are "head", "chicken", "wine", "apple", "tee" or None,
        default is "tree".
    background_color : str, optional
        The background color of the word cloud, default is "#E4E0E1".
    contour_width : int, optional
        Width of the contour around the word cloud, default is 1.
    contour_color : str, optional
        Color of the contour around the word cloud, default is "#D6C0B3".
    figsize : tuple, optional
        The figure size of the word cloud plot, default is (10, 10).
    fontsize : int, optional
        Font size for the plot title, default is 15.
    save_path : str | None, optional
        Path to save the plot image. If None, the plot is not saved, default is None.

    Returns
    -------
    None

    See Also
    --------
    plot_complicated_confusion_matrix : Plots a confusion matrix with some percentage(%) of confusion.
    plot_images: Plots the images and display them.
    plot_images_predictions: Plots the images with their predictions and display them.
    plot_classification_report: Plots the classification report.
    plot_simple_confusion_matrix : Plots a simple confusion matrix.

    Examples
    --------
    >>> corpus = "This is a sample text for generating word clouds"
    >>> plot_wordcloud(corpus, max_words=500, mask="wine")
    """

    assert isinstance(corpus, dict) or isinstance(
        corpus, str
    ), "The corpus can be either a string or a dictionary of words."
    assert mask in [
        "head",
        "chicken",
        "wine",
        "apple",
        "tree",
    ], "The mask can be either 'head', 'chicken', 'wine', 'apple', 'tree'."

    mask = Image.open(f"{this}/../static/images/{mask}.png")
    n_dim = len(np.array(mask).shape)
    mask = (
        np.array(mask).astype(np.int32)
        if n_dim == 2
        else np.array(mask.convert("L")).astype(np.int32)
    )

    for i in range(len(mask)):
        mask[i] = list(map(lambda x: 255 if x == 0 else x, mask[i]))

    image = (
        wc.WordCloud(
            background_color=background_color,
            max_words=max_words,
            mask=mask,
            width=800,
            height=800,
            contour_width=contour_width,
            contour_color=contour_color,
        ).generate_from_frequencies(corpus)
        if isinstance(corpus, dict)
        else wc.WordCloud(
            background_color=background_color,
            max_words=max_words,
            mask=mask,
            width=800,
            height=800,
            contour_width=contour_width,
            contour_color=contour_color,
        ).generate_from_text(corpus)
    )

    plt.figure(figsize=figsize)
    plt.title(title, color="k", fontsize=fontsize)
    plt.imshow(image)
    plt.axis("off")

    if save_path is not None:
        path = pathlib.Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.show()


__all__ = [
    plot_classification_report,
    plot_complicated_confusion_matrix,
    plot_simple_confusion_matrix,
    plot_images_predictions,
    plot_images,
    plot_wordcloud,
]
