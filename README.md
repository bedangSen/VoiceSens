# VoiceSens - Adding Voice Biometrics to your Application

<b>VoiceSens</b> is a <i>text independent</i> voice biometric solution developed to combat some of the shortcomings of standard authentication techniques like passwords and pincodes, as well as current available voice biometric solutions. The solution is developed in Python and uses Watson Speech to Text (speech recognition).

<p align="center">
 <img src="https://i.imgur.com/PQPkGYo.gif" align="middle">
</p>

## Table of Content

+ [Getting Started](#getting-started)
+ [Configuring the Application](#configuring-the-application) 
+ [Running VoiceSens locally](#running-locally)
+ [Demo Screenshots](#demo)
+ [Key Components](#built-with)
+ [References (Further Reading)](#references)
+ [Future Additions](#to-do)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Install and set up Python 3.
1. Sign up for an [IBM Cloud account](https://ibm.biz/devfest2019).
   <p align="center">
    <img src="https://github.com/bedangSen/VoiceSens/blob/master/Images/Screenshot_2019-03-31%20Sign%20up%20for%20IBM%20Cloud.png?raw=true" width="800"  align="middle">
   </p>
  
1. Create an instance of the Speech to Text service and get your credentials:
    - Go to the [Speech to Text](https://console.bluemix.net/catalog/services/speech-to-text) page in the IBM Cloud Catalog.
    - Log in to your IBM Cloud account.
    - Click **Create**.
    - Click **Show** to view the service credentials.
    - Copy the `iam_apikey` and `url` values.
    
    <p align="center">
    <img src="https://i.imgur.com/Y0vZNHr.gif" align="middle">
   </p>

## Configuring the application


1. Open the `sample_config.py` file and change the username and password for the text to speech service. Then rename the file to `config.py` 

```python
APIKEY = "APIKEY"  
URL = "URL"  
```

## Running locally

1. Clone the repository. 

    ```
    git clone https://github.com/bedangSen/VoiceSens.git
    ```
    
1. Move into the project directory. 

    ```
    cd VoiceSens
    ```
 
1. (Optional) Running it in a virtual environment. 

   1. Downloading and installing _virtualenv_. 
   ```
   pip install virtualenv
   ```
   
   2. Create the virtual environment in Python 3.
   
   ```
    virtualenv -p path\to\your\python.exe test_env
    ```    
   
   3. Activate the test environment.     
   
        1. For Windows:
        ```
        test_env\Scripts\Activate
        ```        
        
        2. For Unix:
        ```
        source test_env/bin/activate
        ```    

1. Install all the required libraries, by installing the requirements.txt file.

    ```
    pip install -r requirements.txt
    ```

    
1. Run the application.

    ```
    python voice.py
    ```
    
1. Go to `http://localhost:8080`

## Demo

#### 1. VoiceSens Homepage

<p align="center">
 <a href="https://imgur.com/JuokbKe"><img src="https://i.imgur.com/JuokbKe.gif" title="source: imgur.com" /></a>
</p>

<br><br>

 The first thing that you see when you open the web page are two options:
 1. Enroll a new user
 1. Authenticate an existing user
 

#### 2. Enrollment Page

<p align="center">
 <a href="https://imgur.com/61CsyWO"><img src="https://i.imgur.com/61CsyWO.gif" title="source: imgur.com" /></a>
</p>

<br><br>

If you haven't created a voice sample, the first step is to create an account and enroll your voice samples. The model then generates a voice print on the voice samples provided. 

#### 3. Authentication Page

<p align="center">
 <a href="https://imgur.com/U3T3uVT"><img src="https://i.imgur.com/U3T3uVT.gif" title="source: imgur.com" /></a>
</p>

Once you have created an account, you can authenticate yourself by recording a voice sample, generating a voice print, and then comparing the voice print to the voice prints in the database

#### 4. Voice Biometrics Page

<p align="center">
 <a href="https://imgur.com/eVDHeSE"><img src="https://i.imgur.com/eVDHeSE.gif" title="source: imgur.com" /></a>
</p>

When you record your voice sample, the first thing you do is record the environmental sound. This creates a baseline for noise in the following recording, increasing the accuracy of your results. Once you are done with that you can proceed with reciting the randomly generated words. If the fuzzy matching ratio between the generated words and recognised words is less than 65, the recorded voice phrase will not be accepted, and you will be asked to record your voice sample again. 

## Key Components

* [IBM Watson Speech to Text](https://console.bluemix.net/catalog/services/speech-to-text) - The Speech to Text Service used. 
* [Scipy](https://www.scipy.org/) - SciPy is a Python-based ecosystem of open-source software for mathematics, science, and engineering. 
* [Speech Recognition](https://pypi.org/project/SpeechRecognition/) -  Library for performing speech recognition, with support for several engines and APIs, online and offline.
* [Python Speech Features](https://python-speech-features.readthedocs.io/en/latest/) - This library provides common speech features for ASR including MFCCs and filterbank energies. 
* [Fuzzy Wuzzy](https://github.com/seatgeek/fuzzywuzzy) - Fuzzy string matching like a boss. It uses Levenshtein Distance to calculate the differences between sequences in a simple-to-use package. 
* [Random Words](https://pypi.org/project/random-word/) - This is a simple python package to generate random english words. 
* [Skitlearn Gaussian Mixture Models](https://scikit-learn.org/stable/modules/mixture.html) - sklearn.mixture is a package which enables one to learn Gaussian Mixture Models

## References

* [Digital Signal Processing : Speeker Recognition Final Report](https://raw.githubusercontent.com/ppwwyyxxspeaker-recognition/master/doc/Final-Report-Complete.pdf)
* [MFCC](http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/)
* [Speech Recognition with Python](https://realpython.com/python-speech-recognition/)

## To Do

* Hashing the audio files and signing it with the clients private key, to prevent man in the middle attacks. 
* Improve the accuracy of the GMM model. 
* Add solution architecture.
* Storing the models in a secure Object storage
