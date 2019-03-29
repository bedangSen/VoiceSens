#!/uspeech_recognition/bin/env python3
"""
This is a demo for a voice biometrics application
"""

# ------------------------------------------------------------------------------------------------------------------------------------#
#                                                  Installing Packages Needed                                                         #
# ------------------------------------------------------------------------------------------------------------------------------------#


# This is used to dump the models into an object
import pickle
import datetime
import os                                               # For creating directories
import shutil                                           # For deleting directories
# from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
import scipy.cluster
import scipy.io.wavfile
# For the speech detection alogrithms
import speech_recognition
# For the fuzzy matching algorithms
from fuzzywuzzy import fuzz
# For using the MFCC feature selection
from python_speech_features import mfcc
# For generating random words
from random_words import RandomWords
from sklearn import preprocessing
# For using the Gausian Mixture Models
from sklearn.mixture import GaussianMixture

# Note: Is there a better way to do this?
# This is the file where the credentials are stored
import config

from flask import Flask, render_template, request, jsonify, url_for, redirect, abort, session

PORT = 8080
HOST = '0.0.0.0'  # Set to ‘0.0.0.0’ to have server available externally

# Global Variables
random_words = []
random_string = ""
username = ""
user_directory = "Users/Test"
filename = ""
filename_wav = ""

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/enroll', methods=["GET", "POST"])
def enroll():
    global username
    global user_directory

    if request.method == 'POST':
        data = request.get_json()

        username = data['username']
        password = data['password']
        repassword = data['repassword']

        user_directory = "Users/" + username + "/"

        # Create target directory & all intermediate directories if don't exists
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)
            print("[ * ] Directory ", username,  " Created ...")
        else:
            print("[ * ] Directory ", username,  " already exists ...")
            print("[ * ] Overwriting existing directory ...")
            shutil.rmtree(user_directory, ignore_errors=False, onerror=None)
            os.makedirs(user_directory)
            print("[ * ] Directory ", username,  " Created ...")

        return redirect(url_for('voice'))

    else:
        return render_template('enroll.html')


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    global username
    global user_directory
    global filename

    user_exist = False

    if request.method == 'POST':

        data = request.get_json()
        print(data)

        user_directory = 'Models/'
        username = data['username']
        password = data['password']

        print("[ DEBUG ] : What is the user directory at auth : ", user_directory)
        print("os.fsencode(user_directory : ", os.fsencode(user_directory))
        directory = os.fsencode(user_directory)
        print("directory : ", os.listdir(directory)[1:])

        for file in os.listdir(directory):
            print("file : ", file)
            filename = os.fsdecode(file)
            if filename.startswith(username):
                print("filename : ", filename)
                user_exist = True
                break
            else:
                pass

        if user_exist:
            print("[ * ] The user profile exists ...")
            return "User exist"

        else:
            print("[ * ] The user profile does not exists ...")
            return "Doesn't exist"

    else:
        print('its coming here')
        return render_template('auth.html')


@app.route('/vad', methods=['GET', 'POST'])
def vad():
    if request.method == 'POST':
        global random_words

        f = open('./static/audio/background_noise.wav', 'wb')
        f.write(request.data)
        f.close()

        background_noise = speech_recognition.AudioFile(
            './static/audio/background_noise.wav')
        with background_noise as source:
            speech_recognition.Recognizer().adjust_for_ambient_noise(source, duration=5)

        print("Voice activity detection complete ...")

        random_words = RandomWords().random_words(count=5)
        print(random_words)

        return "  ".join(random_words)

    else:
        background_noise = speech_recognition.AudioFile(
            './static/audio/background_noise.wav')
        with background_noise as source:
            speech_recognition.Recognizer().adjust_for_ambient_noise(source, duration=5)

        print("Voice activity detection complete ...")

        random_words = RandomWords().random_words(count=5)
        print(random_words)

        return "  ".join(random_words)


@app.route('/voice', methods=['GET', 'POST'])
def voice():
    global user_directory
    global filename_wav

    print("[ DEBUG ] : User directory at voice : ", user_directory)

    if request.method == 'POST':
        #    global random_string
        global random_words
        global username

        filename_wav = user_directory + "-".join(random_words) + '.wav'
        f = open(filename_wav, 'wb')
        f.write(request.data)
        f.close()

        speech = speech_recognition.AudioFile(filename_wav)
        with speech as source:
            audio = speech_recognition.Recognizer().record(source)

        # recognize speech using IBM Speech to Text
        try:
            recognised_words_ibm = speech_recognition.Recognizer().recognize_ibm(
                audio, username=config.IBM_USERNAME, password=config.IBM_PASSWORD)
            recognised_words = recognised_words_ibm

            print("IBM Speech to Text thinks you said : " + recognised_words_ibm)
            print("IBM Fuzzy partial score : " +
                  str(fuzz.partial_ratio(random_words, recognised_words_ibm)))
            print("IBM Fuzzy score : " +
                  str(fuzz.ratio(random_words, recognised_words_ibm)))

        except speech_recognition.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
            print("\nPlease try again ...")
            os.remove(filename_wav)
            return "fail"

        except speech_recognition.RequestError as e:
            print(
                "Could not request results from IBM Speech to Text service; {0}".format(e))
            print("\nPlease try again ...")
            os.remove(filename_wav)
            return "fail"

        # # recognize speech using Google Speech Recognition
        # try:
        #     # for testing purposes, we're just using the default API key
        #     # to use another API key, use `speech_recognition.Recognizer().recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        #     # instead of `speech_recognition.Recognizer().recognize_google(audio)`
        #     recognised_words_google = speech_recognition.Recognizer().recognize_google(audio)
        #     recognised_words = recognised_words_google
        #     print("Google Speech Recognition thinks you said : " + recognised_words_google)
        #     print("Google Fuzzy partial score : " + str(fuzz.partial_ratio(random_words, recognised_words_google)))
        #     print("Google Fuzzy score : " + str(fuzz.ratio(random_words, recognised_words_google)))

        # except speech_recognition.UnknownValueError:
        #     print("Google Speech Recognition could not understand audio")
        #     print("\nPlease try again ...")
        #     return "fail"

        # except speech_recognition.RequestError as e:
        #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
        #     print("\nPlease try again ...")
        #     return "fail"

        # # recognize speech using Microsoft Bing Voice Recognition
        # BING_KEY = "6198a48cf6db495198f0123f3ecb8754"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings

        # try:
        #     recognised_words_microsoft = speech_recognition.Recognizer().recognize_bing(audio, key=BING_KEY)
        #     recognised_words = recognised_words_microsoft
        #     print("Microsoft Bing Voice Recognition thinks you said : " + recognised_words_microsoft)
        # except speech_recognition.UnknownValueError:
        #     print("Microsoft Bing Voice Recognition could not understand audio")
        #     print("\nPlease try again ...")
        #     return "fail"
        # except speech_recognition.RequestError as e:
        #     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        #     print("\nPlease try again ...")
        #     return "fail"

        if fuzz.ratio(random_words, recognised_words) < 65:
            print(
                "\nThe words you have spoken aren't entirely correct. Please try again ...")
            os.remove(filename_wav)
            return "fail"
        else:
            pass

        return "pass"

    else:
        return render_template('voice.html')


@app.route('/biometrics', methods=['GET', 'POST'])
def biometrics():
    global user_directory
    print("[ DEBUG ] : User directory is : ", user_directory)

    if request.method == 'POST':
        pass
    else:
        # MFCC
        print("Into the biometrics route.")

        directory = os.fsencode(user_directory)
        features = numpy.asarray(())

        for file in os.listdir(directory):
            filename_wav = os.fsdecode(file)
            if filename_wav.endswith(".wav"):
                print("[biometrics] : Reading audio files for processing ...")
                (rate, signal) = scipy.io.wavfile.read(user_directory + filename_wav)

                extracted_features = extract_features(rate, signal)

                if features.size == 0:
                    features = extracted_features
                else:
                    features = numpy.vstack((features, extracted_features))

            else:
                continue

        # GaussianMixture Model
        print("[ * ] Building Gaussian Mixture Model ...")

        gmm = GaussianMixture(n_components=16,
                            max_iter=200,
                            covariance_type='diag',
                            n_init=3)

        gmm.fit(features)
        print("[ * ] Modeling completed for user :" + username +
            " with data point = " + str(features.shape))

        # dumping the trained gaussian model
        # picklefile = path.split("-")[0]+".gmm"
        print("[ * ] Saving model object ...")
        pickle.dump(gmm, open("Models/" + str(username) +
                            ".gmm", "wb"), protocol=None)
        print("[ * ] Object has been successfully written to Models/" +
            username + ".gmm ...")
        print("\n\n[ * ] User has been successfully enrolled ...")

        features = numpy.asarray(())

        return "User has been successfully enrolled ...!!"


@app.route("/verify", methods=['GET'])
def verify():
    global username
    global filename
    global user_directory
    global filename_wav

    print("[ DEBUG ] : user directory : " , user_directory)
    print("[ DEBUG ] : filename : " , filename)
    print("[ DEBUG ] : filename_wav : " , filename_wav)

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                   LTSD and MFCC                                                     #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    # (rate, signal) = scipy.io.wavfile.read(audio.get_wav_data())
    (rate, signal) = scipy.io.wavfile.read(filename_wav)

    extracted_features = extract_features(rate, signal)

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                          Loading the Gaussian Models                                                #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    gmm_models = [os.path.join(user_directory, user)
                  for user in os.listdir(user_directory)
                  if user.endswith('.gmm')]

    # print("GMM Models : " + str(gmm_models))

    # Load the Gaussian user Models
    models = [pickle.load(open(user, 'rb')) for user in gmm_models]

    user_list = [user.split("/")[-1].split(".gmm")[0]
                 for user in gmm_models]

    log_likelihood = numpy.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        scores = numpy.array(gmm.score(extracted_features))
        log_likelihood[i] = scores.sum()

    print("Log liklihood : " + str(log_likelihood))

    identified_user = numpy.argmax(log_likelihood)

    print("[ * ] Identified User : " + str(identified_user) +
          " - " + user_list[identified_user])

    auth_message = ""

    if user_list[identified_user] == username:
        print("[ * ] You have been authenticated!")
        auth_message = "success"
    else:
        print("[ * ] Sorry you have not been authenticated")
        auth_message = "fail"

    return auth_message


def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix
    (https://appliedmachinelearning.blog/2017/11/14/spoken-speaker-identification-based-on-gaussian-mixture-models-python-implementation/)"""

    print("[Delta] : Calculating delta")

    rows, cols = array.shape
    deltas = numpy.zeros((rows, 20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows - 1:
                second = rows - 1
            else:
                second = i+j
            index.append((second, first))
            j += 1
        deltas[i] = (array[index[0][0]]-array[index[0][1]] +
                     (2 * (array[index[1][0]]-array[index[1][1]]))) / 10
    return deltas


def extract_features(rate, signal):
    print("[extract_features] : Exctracting featureses ...")

    mfcc_feat = mfcc(signal,
                     rate,
                     winlen=0.020,  # remove if not requred
                     preemph=0.95,
                     numcep=20,
                     nfft=1024,
                     ceplifter=15,
                     highfreq=6000,
                     nfilt=55,

                     appendEnergy=False)

    mfcc_feat = preprocessing.scale(mfcc_feat)

    delta_feat = calculate_delta(mfcc_feat)

    combined_features = numpy.hstack((mfcc_feat, delta_feat))

    return combined_features


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
