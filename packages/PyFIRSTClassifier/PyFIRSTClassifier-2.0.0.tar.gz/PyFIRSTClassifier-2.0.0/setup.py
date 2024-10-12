from setuptools import setup, find_packages

setup(
    name='PyFIRSTClassifier',
    version='2.0.0',
    description='Automated morphological classification of Compact and Extended radio sources using Deep Convolutional Neural Networks',
    long_description="""
    ## FIRST Classifier: Compact and Extended Radio Galaxies Classification using Deep Convolutional Neural Networks

    The FIRST Classifier is a tool for the automated morphological classification of radio sources based on data from the FIRST radio survey. Developed by Wathela Alhassan et al. 2018, this system leverages a trained Deep Convolutional Neural Network to classify radio galaxies into Compact, BENT, FRI, and FRII categories with high accuracy. It can predict the morphological class of single or multiple sources, achieving an overall classification accuracy of 97%.
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
    """,
    long_description_content_type='text/markdown',
    author='Wathela Alhassan',
    author_email='wathelahamed@gmail.com',
    url='https://github.com/wathela/FIRSTClassifier', 
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pandas==2.0.3',
        'numpy==1.24.3',
        'matplotlib==3.7.5',
        'scipy==1.10.1',
        'astropy==5.2.2',
        'pyvo==1.5.2',
        'scikit-image==0.21.0',
        'keras==2.13.1',
        'tensorflow==2.13.1'
    ],
    entry_points={
        'console_scripts': [
            'first_classifier=PyFIRSTClassifier.FIRSTClassifier:main',
        ],
    },
)

