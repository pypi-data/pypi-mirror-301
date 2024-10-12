    ## FIRST Classifier: Compact and Extended Radio Galaxies Classification using Deep Convolutional Neural Networks

    The FIRST Classifier is a tool for the automated morphological classification of radio sources based on data from the FIRST radio survey. Developed by Wathela Alhassan et al., this software leverages a trained Deep Convolutional Neural Network to classify radio galaxies into Compact, BENT, FRI, and FRII categories with high accuracy. It can predict the morphological class of single or multiple sources, achieving an overall classification accuracy of 97%.
    - **Accuracy**: 97%
    - **Recall**: Compact (98%), BENT (100%), FRI (98%), FRII (93%)

    ## How to use:

        ```python
        from PyFIRSTClassifier import FIRSTClassifier

        classifier = FIRSTClassifier.Classifiers()

        # Example for single source classification
        ra = 223.47337
        dec = 26.80928

        # Call the classification function
        fits_file_link, predicted_class, probability, image = classifier.single_source(ra, dec, plot=False)

        # Example for multi-source classification
        input_file = "test.csv"
        output_file = "results.csv"
        classifier.multi_sources(file=input_file, ra_col=0, dec_col=1, output_file=output_file)
    
    For more information, see the associated research paper:
    - MNRAS: https://academic.oup.com/mnras/advance-article/doi/10.1093/mnras/sty2038/5060783
    - Astro-ph: https://arxiv.org/abs/1807.10380

<img src="https://github.com/wathela/FIRST-CLASSIFIER/blob/master/Diagram.png" width=493px>



### How to cite:
@article{Alhassan2018,

author = {Alhassan, Wathela and Taylor, A R and Vaccari, Mattia},

doi = {10.1093/mnras/sty2038},

issn = {0035-8711},

journal = {Monthly Notices of the Royal Astronomical Society},

month = {jul},

title = {{The FIRST Classifier: Compact and Extended Radio Galaxy Classification using Deep Convolutional Neural Networks}},

url = {https://academic.oup.com/mnras/advance-article/doi/10.1093/mnras/sty2038/5060783},

year = {2018}

}
