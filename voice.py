#!/uspeech_recognition/bin/env python3
"""
This is a demo for a voice authentication application
"""

__author__ = "Bedang Sen"
__version__ = "0.1.0"
__license__ = "none"

import os                                                               #For creating directories
import shutil                                                           #For deleting directories
import numpy
import scipy.io.wavfile
import config                                                           #This is the file where the credentials are stored
import cPickle                                                          #This is used to dump the models into an object

# import sounddevice
import speech_recognition                                               #For the speech detection alogrithms
import matplotlib.pyplot as plt
import datetime
import scipy.cluster

from collections import defaultdict
from ltsd import ltsd_main_function                                     #Implementation of LTSD function from https://github.com/shunsukeaihara/pyssp/blob/master/pyssp/vad/ltsd.py
from fuzzywuzzy import fuzz                                             #For the fuzzy matching algorithms
from random_words import RandomWords                                    #For generating random words
from python_speech_features import mfcc                                 #For using the MFCC feature selection
from sklearn.mixture import GaussianMixture                             #For using the Gausian Mixture Models
from sklearn import preprocessing

# import sys
# import matplotlib.pyplot as plt
# import numpy as np
# from pyssp.util import get_frame, read_signal
# from six.moves import xrange

user_directory = 'Testing/test/'
username = "test"

WINSIZE = 2048
fs = 48000
# sounddevice.default.samplerate = fs
# sounddevice.default.channels = 2

def main():
    """ Main entry point of the app """
    menu_option()
    

def menu_option():
    """ Prompts the user for a menu option. Options include creating a new account or logging in to an existing account. """

    
    account_option = input("\nWould you like to login(L) or create a new account(C)? ")

    if account_option=="L" or account_option=="l":
        print("You are logging in now...")
        account_login()

    elif account_option=="C" or account_option=="c":
        print("You are creating a new account...")
        create_account()

    else:
        print("You entered the wrong input...")
        menu_option()

def create_account():
    """ The Create Account Module : Allows user to create a user profile to store the voice """ 

    features_dictionary = defaultdict(list)                             #Creating a default dictionary. dict subclass that calls a factory function to supply missing values.


    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                      Prompting for Username                                                         #
    # ------------------------------------------------------------------------------------------------------------------------------------#
    # username = input("[ * ] Please enter your username : ")
    # # print("Username : " + username)

    # user_directory = "Testing\\" + username + "\\"

    # # Create target directory & all intermediate directories if don't exists
    # if not os.path.exists(user_directory):
    #     os.makedirs(user_directory)
    #     print("[ * ] Directory " , username ,  " Created ...")
    # else:    
    #     print("[ * ] Directory " , username ,  " already exists ...")
    #     print("[ * ] Overwriting existing directory ...")
    #     shutil.rmtree(user_directory, ignore_errors=False, onerror=None)
    #     os.makedirs(user_directory)
    #     print("[ * ] Directory " , username ,  " Created ...")    

    # # ------------------------------------------------------------------------------------------------------------------------------------#
    # #                                                      Recording background sound                                                     #   ---> Not used!!! 
    # # ------------------------------------------------------------------------------------------------------------------------------------#

    # print("[ * ] Scanning environmental sound. Please remain silent ...")

    # duration = 5  # seconds
    # background_recording = sounddevice.rec(int(duration * fs))
    # print("[ * ] Scanning ...")
    
    # # Recording completed
    # sounddevice.wait()
    # print("[ * ] Scanning complete ...")

    # # input("[ DEBUG ] : Enter to proceed ...")
    # # print("[ DEBUG ] : Playing back recorded sound ...")
    # # sounddevice.play(background_recording)
    # # sounddevice.wait()
    # # print("[ DEBUG ] : Playback complete ...")

    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                      Generating random passphrases for enrollment                                   #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    # print("\n[ * ] Generating random passphrase ...")

    # number_of_samples = 3                                                               #Represents the number of voice samples that the application is going to collect. 
    # speech_recognition.Recognizer().pause_threshold = 5.5                               #Represents the minimum length of silence (in seconds) that will register as the end of a phrase. 
    # # speech_recognition.Recognizer().energy_threshold = 500                            #Represents the energy level threshold for sounds. Values below this threshold are considered silence, and values above this threshold are considered speech
    # speech_recognition.Recognizer().dynamic_energy_threshold = True                     #Represents whether the energy level threshold (see recognizer_instance.energy_threshold) for sounds should be automatically adjusted based on the currently ambient noise level while listening. 
    
    # for count in range(number_of_samples):                                                              
    #     print("\nPassphrase [ " + str(count + 1) + " ]")
    #     audio = generate_words()

    #     with open(user_directory + "passphrase-microphone-results-" + str(count + 1) + ".wav", "wb") as f:
    #         f.write(audio.get_wav_data())


    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                   LTSD and MFCC                                                     #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    directory = os.fsencode(user_directory)
    features = np.asarray(())
    # print(directory)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # print(filename) #debug
        if filename.endswith(".wav"):
            # pass
            # print(filename) #debug
            (rate, signal) = scipy.io.wavfile.read(user_directory + filename)

            extracted_features = extract_features(rate, signal)

            if features.size == 0:
                features = mfcc_feat
            else:
                features = np.vstack((features, mfcc_feat))


            if features.size == 0:
                features = mfcc_feat
            else:
                features = np.vstack((features, mfcc_feat))           

            # features_dictionary[username].extend(mfcc_feat)
        else:
            continue

    #-------------------------------------------------------------------------------------------------------------------------------------#
    #----------------------------------------------------------DUBUG : LTSD and MFCC -----------------------------------------------------#                                                     #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    # # DEBUG
    # # print(features_dictionary)
    # with open(user_directory + "features-dictionary.txt", 'at' ) as features:
    #     features.write(str(features_dictionary))


    # # debug
    # audio_file = user_directory + "passphrase-microphone-results-1.wav"                                  #For testing purposes. 
    # result, ltsds = ltsd_main_function(audio_file)

    # # debug
    # with open(user_directory + "passphrase-microphone-results-after_ltsd.txt", "wt") as f:
    #     f.write(str(ltsds))

    # # (rate,signal) = scipy.io.wavfile.read(audio_file)

    # # debug
    # with open(user_directory + "passphrase-microphone-results-rate.txt", "wt") as f:
    #     f.write(str(rate))

    # # debug
    # with open(user_directory + "passphrase-microphone-results-signal.txt", "wt") as f:
    #     f.write(str(signal))

    # # print(signal.shape)
    # # print(rate)
    # # print(mfcc_feat.shape)

    # # debug
    # with open(user_directory + "passphrase-microphone-results-mfcc.txt", "w") as f:
    #     f.write(str(mfcc_feat[0]))
    #     f.write(str(mfcc_feat.shape))

    


    










    


    


def account_login():
    print("Test you have entered login menu")
    

def generate_words():
    # obtain audio from the microphone

    with speech_recognition.Microphone() as source:

        random_words = RandomWords().random_words(count=5)

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

        print(random_words)

        print("[ * ] Scanning environmental sound. Please remain silent ...")
        speech_recognition.Recognizer().adjust_for_ambient_noise(source, duration = 5)      #Adjusts the energy threshold dynamically using audio from source (an AudioSource instance) to account for ambient noise.
        print("[ * ] Scanning complete ...")
        print("[ * ] Recite the passphrase to train the voice model ...")
        
        audio = speech_recognition.Recognizer().listen(source, timeout = 10)            
        
        # print("Type : " + str(type(audio))) test

    # recognize speech using IBM Speech to Text
    try:
        recognised_words_ibm = speech_recognition.Recognizer().recognize_ibm(audio, username=config.IBM_USERNAME, password=config.IBM_PASSWORD)
        print("IBM Speech to Text thinks you said : " + recognised_words_ibm)
        print("IBM Fuzzy partial score : " + str(fuzz.partial_ratio(random_words, recognised_words_ibm)))
        print("IBM Fuzzy score : " + str(fuzz.ratio(random_words, recognised_words_ibm)))

        if fuzz.ratio(random_words, recognised_words_ibm) < 65:
            print("\nThe words you have spoken aren't entirely correct. Please try again ...")
            audio = generate_words()
            # print("This means that the function returned from the if condition : type - [" + str(type(audio)) + "]")
        else:
                # print("This means that the function returned the first time : type - [" + str(type(audio)) + "]")
                # return audio
                pass

        # print("This means that the function returned not the first time : type - [" + str(type(audio)) + "]")
        # return audio     

    except speech_recognition.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
        print("\nPlease try again ...")
        audio = generate_words()
    except speech_recognition.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
        print("\nPlease try again ...")
        audio = generate_words()

    return audio

    # # recognize speech using Google Speech Recognition
    # try:
    #     # for testing purposes, we're just using the default API key
    #     # to use another API key, use `speech_recognition.Recognizer().recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    #     # instead of `speech_recognition.Recognizer().recognize_google(audio)`
    #     recognised_words_google = speech_recognition.Recognizer().recognize_google(audio)
    #     print("Google Speech Recognition thinks you said : " + recognised_words_google)
    #     print("Google Fuzzy partial score : " + str(fuzz.partial_ratio(random_words, recognised_words_google)))
    #     print("Google Fuzzy score : " + str(fuzz.ratio(random_words, recognised_words_google)))
        
    # except speech_recognition.UnknownValueError:
    #     print("Google Speech Recognition could not understand audio")
    # except speech_recognition.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))


    # if fuzz.ratio(random_words, recognised_words_ibm) < 65 or fuzz.ratio(random_words, recognised_words_google) < 65:
    #     print("\nThe words you have spoken aren't entirely correct. Please try again ...")
    #     generate_words()
    # else:
    #     return audio
             
    

    # # recognize speech using Microsoft Bing Voice Recognition
    # BING_KEY = "6198a48cf6db495198f0123f3ecb8754"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    # try:
    #     recognised_words_microsoft = speech_recognition.Recognizer().recognize_bing(audio, key=BING_KEY)
    #     print("Microsoft Bing Voice Recognition thinks you said : " + recognised_words_microsoft)
    # except speech_recognition.UnknownValueError:
    #     print("Microsoft Bing Voice Recognition could not understand audio")
    # except speech_recognition.RequestError as e:
    #     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix 
    (https://appliedmachinelearning.blog/2017/11/14/spoken-speaker-identification-based-on-gaussian-mixture-models-python-implementation/)"""
 
    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j  rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(rate, signal):
    
    mfcc_feat = mfcc(signal,
                     rate,
                    #  winlen=0.030,               #remove if not requred
                     preemph=0.95,
                     numcep=20,
                     ceplifter=15,
                     highfreq=6000,
                     nfilt=55,
                     appendEnergy = False)
                     )

            mfcc_feat = preprocessing.scale(mfcc_feat)

            delta_feat = calculate_delta(mfcc_feat)

            combined_features = np.hstack((mfcc_feat,delta_feat))

            return combined_features

            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # ax.plot(combined_features)
            # plt.show()

            
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
