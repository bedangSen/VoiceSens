#!/uspeech_recognition/bin/env python3
"""
This is a demo for a voice authentication application
"""

__author__ = "Bedang Sen"
__version__ = "0.1.0"
__license__ = "none"

import numpy
import scipy.io.wavfile
import sounddevice
import speech_recognition
import datetime
from fuzzywuzzy import fuzz
from random_words import RandomWords

fs = 48000
sounddevice.default.samplerate = fs
sounddevice.default.channels = 2

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
    # # ------------------------------------------------------------------------------------------------------------------------------------#
    # #                                                      Prompting for Username                                                         #
    # # ------------------------------------------------------------------------------------------------------------------------------------#
    # username = input("[ * ] Please enter your username : ")
    # # print("Username : " + username)

    # # ------------------------------------------------------------------------------------------------------------------------------------#
    # #                                                      Recording background sound                                                     #
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

    print("\n[ * ] Generating random passphrase ...")

    speech_recognition.Recognizer().pause_threshold = 5.5                               #Represents the minimum length of silence (in seconds) that will register as the end of a phrase. 
    # speech_recognition.Recognizer().energy_threshold = 500                              #Represents the energy level threshold for sounds. Values below this threshold are considered silence, and values above this threshold are considered speech
    speech_recognition.Recognizer().dynamic_energy_threshold = True                     #Represents whether the energy level threshold (see recognizer_instance.energy_threshold) for sounds should be automatically adjusted based on the currently ambient noise level while listening. 
    
    for count in range(3):
        print("\nPassphrase [ " + str(count + 1) + " ]")
        audio = generate_words()

        with open("passphrase-microphone-results-" + str(count + 1) + ".wav", "wb") as f:
            f.write(audio.get_wav_data())

        # with open("log-microphone-results.txt", "at") as logs:
        #     logs.write("\n\n" + str(datetime.datetime.now()) + "\n[ DEBUG ] : Audio file - " + str(audio.get_wav_data()))


    # ------------------------------------------------------------------------------------------------------------------------------------#
    #                                                                   VAD and LTSD                                                      #
    # ------------------------------------------------------------------------------------------------------------------------------------#

    


    


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
    IBM_USERNAME = "acdae4c1-2f72-483e-8448-3bcd3ee34aec"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    IBM_PASSWORD = "p3CjDDb6hbaj"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
    try:
        recognised_words_ibm = speech_recognition.Recognizer().recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        print("IBM Speech to Text thinks you said : " + recognised_words_ibm)
        # print("IBM Fuzzy partial score : " + str(fuzz.partial_ratio(random_words, recognised_words_ibm)))
        print("IBM Fuzzy score : " + str(fuzz.ratio(random_words, recognised_words_ibm)))

        if fuzz.ratio(random_words, recognised_words_ibm) < 65:
            print("\nThe words you have spoken aren't entirely correct. Please try again ...")
            generate_words()
        else:
                return audio     

    except speech_recognition.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
        print("\nPlease try again ...")
        generate_words()
    except speech_recognition.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))
        print("\nPlease try again ...")
        generate_words()

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

    # # recognize speech using Microsoft Bing Voice Recognition
    # BING_KEY = "6198a48cf6db495198f0123f3ecb8754"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
    # try:
    #     recognised_words_microsoft = speech_recognition.Recognizer().recognize_bing(audio, key=BING_KEY)
    #     print("Microsoft Bing Voice Recognition thinks you said : " + recognised_words_microsoft)
    # except speech_recognition.UnknownValueError:
    #     print("Microsoft Bing Voice Recognition could not understand audio")
    # except speech_recognition.RequestError as e:
    #     print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
