# VoiceSens

<b>VoiceSens</b> is a <i>text independent</i> voice biometric solution developed to combat some of the shortcomings of standard authentication techniques like passwords and pincodes, as well as current available voice biometric solutions. The solution is developed in Python and uses Watson Speech to Text (speech recognition).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

1. Sign up for an [IBM Cloud account](https://console.bluemix.net/registration/).
1. Create an instance of the Speech to Text service and get your credentials:
    - Go to the [Speech to Text](https://console.bluemix.net/catalog/services/speech-to-text) page in the IBM Cloud Catalog.
    - Log in to your IBM Cloud account.
    - Click **Create**.
    - Click **Show** to view the service credentials.
    - Copy the `username` and `password` values.

## Configuring the application


1. Open the sample_config.py file and change the username and password for the text to speech service. Then rename the file to config.py 

```
IBM_USERNAME = "USERNAME"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
IBM_PASSWORD = "PASSWORD"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
```

## Running locally

1. Run the application.

    ```
    python voice.py
    ```

## Built With

* [IBM Watson Speech to Text](https://console.bluemix.net/catalog/services/speech-to-text) - The Speech to Text Service used. 
* [Numpy](http://www.numpy.org/) - NumPy is the fundamental package for scientific computing with Python.
* [Scipy](https://www.scipy.org/) - SciPy (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering. 
* [Speech Recognition](https://pypi.org/project/SpeechRecognition/) -  Library for performing speech recognition, with support for several engines and APIs, online and offline.
* [Python Speech Features]() - 
* [Fuzzy Wuzzy]() - 
* [Random Words]() - 
* [Skitlearn Gaussian Mixture Models](https://scikit-learn.org/stable/modules/mixture.html) - sklearn.mixture is a package which enables one to learn Gaussian Mixture Models

## References

* [Digital Signal Processing : Speeker Recognition Final Report](https://raw.githubusercontent.com/ppwwyyxxspeaker-recognition/master/doc/Final-Report-Complete.pdf)
