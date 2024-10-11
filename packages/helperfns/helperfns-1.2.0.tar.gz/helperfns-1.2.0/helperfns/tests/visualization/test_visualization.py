class TestVisualization:
    def test_plot_word_cloud_confusion_matrix(self):
        from helperfns.visualization import plot_wordcloud
        import pytest

        with pytest.raises(AssertionError) as exc_info:
            plot_wordcloud(corpus=6)
        assert (
            str(exc_info.value)
            == "The corpus can be either a string or a dictionary of words."
        )

        with pytest.raises(AssertionError) as exc_info:
            plot_wordcloud(corpus="this is a dog", mask="dog")
        assert (
            str(exc_info.value)
            == "The mask can be either 'head', 'chicken', 'wine', 'apple', 'tree'."
        )

    def test_plot_simple_confusion_matrix(self):
        from helperfns.visualization import plot_simple_confusion_matrix
        import pytest

        with pytest.raises(ValueError) as exc_info:
            plot_simple_confusion_matrix([], [])

        assert (
            str(exc_info.value)
            == "zero-size array to reduction operation maximum which has no identity"
        )

    def test_plot_complicated_confusion_matrix(self):
        from helperfns.visualization import plot_complicated_confusion_matrix
        import pytest
        import matplotlib

        matplotlib.use("Agg")  #

        with pytest.raises(ValueError) as exc_info:
            plot_complicated_confusion_matrix([], [])

        assert (
            str(exc_info.value)
            == "zero-size array to reduction operation maximum which has no identity"
        )

    def test_plot_classification_report(self):
        from helperfns.visualization import plot_classification_report
        import pytest

        with pytest.raises(KeyError) as exc_info:
            plot_classification_report([], [])

        assert str(exc_info.value) == "'support'"
