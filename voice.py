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

random_words = []
random_string = ""
username = ""
user_directory = "Users/PercyJackson"

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
    if request.method == 'POST':

        data = request.get_json()

        username = data['username']
        password = data['password']

        print(data)
        return redirect(url_for('voice'))

        # if True:
        #     return redirect(url_for('voice'))
        # else:
        #     return abort(401)
    else:
        return render_template('auth.html')


@app.route('/vad', methods=['GET', 'POST'])
def VAD():
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

    if request.method == 'POST':
        #    global random_string
        global random_words
        global username

    #    print("random strings in voice : ", random_string)
    #    print("randome workds in voice : ", random_words)

        filename = user_directory + "-".join(random_words) + '.wav'
        f = open(filename, 'wb')
        f.write(request.data)
        f.close()

        speech = speech_recognition.AudioFile(filename)
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
            os.remove(filename)
            return "fail"

        except speech_recognition.RequestError as e:
            print(
                "Could not request results from IBM Speech to Text service; {0}".format(e))
            print("\nPlease try again ...")
            os.remove(filename)
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
            os.remove(filename)
            return "fail"
        else:
            pass

        return "pass"

    else:
        return render_template('voice.html')


app.route('/biometrics', methods=['GET'])


def biometrics():
    
    # MFCC
    
    directory = os.fsencode(user_directory)
    features = numpy.asarray(())

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".wav"):

            (rate, signal) = scipy.io.wavfile.read(user_directory + filename)

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


def account_login():
    print("Test you have entered login menu")

    user_directory = "Models/"
    username = "test"  # Test only!
    user_exist = False

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                      Prompting for Username                                                         #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    username = input("[ * ] Please enter your username : ")

    directory = os.fsencode(user_directory)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.startswith(username):
            user_exist = True
            break
        else:
            pass

    if user_exist:
        print("[ * ] The user profile exists ...")
    else:
        print("[ * ] The user profile does not exists ...")
        return

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                  Generating random passphrases for Authentication                                   #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    print("\n[ * ] Generating random passphrase ...")

    # Represents the minimum length of silence (in seconds) that will register as the end of a phrase.
    speech_recognition.Recognizer().pause_threshold = 5.5
    # speech_recognition.Recognizer().energy_threshold = 500                            #Represents the energy level threshold for sounds. Values below this threshold are considered silence, and values above this threshold are considered speech
    # Represents whether the energy level threshold (see recognizer_instance.energy_threshold) for sounds should be automatically adjusted based on the currently ambient noise level while listening.
    speech_recognition.Recognizer().dynamic_energy_threshold = True

    print("\n[ Authentication Passphrase ]")
    audio = generate_words()

    with open(user_directory + "passphrase-authentication-results.wav", "wb") as f:
        f.write(audio.get_wav_data())

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                   LTSD and MFCC                                                     #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    # (rate, signal) = scipy.io.wavfile.read(audio.get_wav_data())
    (rate, signal) = scipy.io.wavfile.read(
        user_directory + "passphrase-authentication-results.wav")

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

    if user_list[identified_user] == username:
        print("[ * ] You have been authenticated!")
    else:
        print("[ * ] Sorry you have not been authenticated")


def generate_words():
    # obtain audio from the microphone

    # Represents the minimum length of silence (in seconds) that will register as the end of a phrase.
    speech_recognition.Recognizer().pause_threshold = 5.5
    # speech_recognition.Recognizer().energy_threshold = 500                            #Represents the energy level threshold for sounds. Values below this threshold are considered silence, and values above this threshold are considered speech
    speech_recognition.Recognizer().dynamic_energy_threshold = True

    with speech_recognition.Microphone() as source:

        # random_words = RandomWords().get_random_words(
        #     hasDictionaryDef="true",
        #     includePartOfSpeech="noun,verb",
        #     # minCorpusCount=80,
        #     # maxCorpusCount=100,
        #     minDictionaryCount=25,
        #     maxDictionaryCount=35,
        #     minLength=3,
        #     maxLength=10,
        #     # sortBy="count",
        #     # sortOrder="asc",
        #     limit=5)

        print("[ * ] Scanning environmental sound. Please remain silent ...")
        # Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
        speech_recognition.Recognizer().adjust_for_ambient_noise(source, duration=5)
        print("[ * ] Scanning complete ...")
        print("[ * ] Recite the passphrase to train the voice model ...")

        random_words = RandomWords().random_words(count=5)

        print("\n")
        print(random_words)

        audio = speech_recognition.Recognizer().listen(source, timeout=10)

        # print("Type : " + str(type(audio))) test

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
        audio = generate_words()
    except speech_recognition.RequestError as e:
        print(
            "Could not request results from IBM Speech to Text service; {0}".format(e))
        print("\nPlease try again ...")
        audio = generate_words()

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
    #     audio = generate_words()
    # except speech_recognition.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))
    #     print("\nPlease try again ...")
    #     audio = generate_words()

    # # recognize speech using Microsoft Bing Voice Recognition
    # BING_KEY = "6198a48cf6db495198f0123f3ecb8754"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings

    # try:
    #     recognised_words_microsoft = speech_recognition.Recognizer().recognize_bing(audio, key=BING_KEY)
    #     recognised_words = recognised_words_microsoft
    #     print("Microsoft Bing Voice Recognition thinks you said : " + recognised_words_microsoft)
    # except speech_recognition.UnknownValueError:
    #     print("Microsoft Bing Voice Recognition could not understand audio")
    #     print("\nPlease try again ...")
    #     audio = generate_words()
    # except speech_recognition.RequestError as e:
    #     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
    #     print("\nPlease try again ...")
    #     audio = generate_words()

    if fuzz.ratio(random_words, recognised_words) < 65:
        print("\nThe words you have spoken aren't entirely correct. Please try again ...")
        generate_words()
    else:
        pass

    return audio


def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix
    (https://appliedmachinelearning.blog/2017/11/14/spoken-speaker-identification-based-on-gaussian-mixture-models-python-implementation/)"""

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

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(combined_features)
    # plt.show()


# if __name__ == "__main__":
#     """ This is executed when run from the command line """
#     main()

## Main ##


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
