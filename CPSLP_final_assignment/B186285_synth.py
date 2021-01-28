from pathlib import Path
from nltk.corpus import cmudict
import simpleaudio
import argparse
import wave
import re
import numpy as np
import struct
import os


class Synth:
    def __init__(self, wav_folder):
        """
        Load diphone database and creates a dictionary.
        :param wav_folder: the name of diphone files` folder
        """
        if not os.path.exists(wav_folder):
            raise FileNotFoundError("The folder '" + wav_folder + "' does not exist.")
        
        self.diphone_database = {}
        all_diphone_wav_files = (str(item) for item in Path(wav_folder).glob('*.wav') if item.is_file())
        file_names = list(all_diphone_wav_files)
        for wav_file in file_names:
            diphone = re.search(r'\/.+\.', wav_file).group()[1:-1]
            self.diphone_database[diphone] = wav_file

    def get_single_diphone_content(self, diphone, emphasis=False):
        """
        Load data of a single diphone or load corresponding silence to punctuation
        :param diphone: name of the target diphone to load
        :param emphasis: whether the diphone is an emphasis makeup
        :return: the data of a single diphone in form of numpy array
        """
        if diphone in ',':
            num_samples = 200 * (16000 / 1000)
            diphone_data = np.array([0] * int(num_samples))
        elif diphone in '.:?!':
            num_samples = 400 * (16000 / 1000)
            diphone_data = np.array([0] * int(num_samples))
        elif diphone not in self.diphone_database.keys():
            raise KeyError("'" + diphone + "' can not be found in the diphone database")
        else:
            filename = self.diphone_database[diphone]
            file = wave.open(filename, 'rb')
            nframes = file.getnframes()
            diphone_data = file.readframes(nframes)
            diphone_data = np.frombuffer(diphone_data, np.int16)
            if emphasis: diphone_data = diphone_data * 4 # half amplitude
            file.close()
        return diphone_data

    def get_diphone_seq_concatenation(self, diphone_seq, out_filename,
                                      signal_r=False, emphasis_i=None, crossfade=False):
        """
        Contatenate diphones to a output wav file
        :param diphone_seq: given diphones to concatenate
        :param out_filename: the name of output wav file
        :param signal_r: whether to perform signal reverse
        :param emphasis_i: the start and end indexes of the emphasis diphone in form of tuple
        :param crossfade: whether to perform smoother concatenation
        """
        total_data = np.array([])
        for d_i in range(len(diphone_seq)):
            if emphasis_i and emphasis_i[0] <= d_i < emphasis_i[1]:
                data = self.get_single_diphone_content(diphone_seq[d_i], emphasis=True)
            else:
                data = self.get_single_diphone_content(diphone_seq[d_i])

            if crossfade:
                if total_data.size == 0:
                    total_data = np.append(total_data, data)
                else:
                    overlap_left = total_data[-160:]
                    overlap_right = data[0:160]
                    temp_right = data[160:]
                    overlap = np.array([])
                    for i in range(160):
                        overlap = np.append(overlap, np.int16(overlap_left[i]*(160-i)/160 + overlap_right[i]*i/160))
                    total_data = np.append(total_data[:-160], overlap)
                    total_data = np.append(total_data, temp_right)
            else:
                total_data = np.append(total_data, data)

        total_data = np.int16(total_data)
        total_data = struct.pack('h' * len(total_data), *total_data)

        if signal_reverse:
            total_data = total_data[::-1]

        path = out_filename
        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(total_data)
        wf.close()


class Utterance:
    def __init__(self, source, fromfile=False):
        """
        Initialise necessary variables
        :param source: the input phrase as a phrase or filename
        :param fromfile: indicate whether source is phrase or from file
        """
        self.source = source
        self.normalised_words_list = []
        self.emphasis = ''
        self.e_start_i = 0
        self.e_end_i = 0
        self.file_input(source) if fromfile else self.input_normalise(source)

    def input_normalise(self, phrase):
        """
        Process the input phrase, detect whether exists emphasis makeup
        :param phrase: the input phrase
        :return: the normalised phrase
        """
        emphasis_search = re.search(r'\{.*\}', phrase)
        if emphasis_search: self.emphasis = emphasis_search.group(0)[1:-1]

        words_list = phrase.split(' ')
        for word in words_list:
            word_temp = ''
            for c in word:
                if c.isalpha():
                    word_temp += c.lower()
                if c in ',.:?!{}':
                    if word_temp: self.normalised_words_list.append(word_temp)
                    self.normalised_words_list.append(c)
                    word_temp = ''
            if word_temp: self.normalised_words_list.append(word_temp)

    def file_input(self, filename):
        """
        Extract phrase from given file and call input_normalise to process it
        :param filename: the name of file
        """
        input_s = ''
        for line in open(filename):
            input_s += (' ' + line)
        self.input_normalise(input_s)

    def get_diphone_seq(self, word_list=[], words_r=False, phones_r=False):
        """
        Transfer normalised phrase to diphone sequence
        :param word_list: support function get_spell_diphone_seq designed for spelling
        :param words_r: whether to reverse words
        :param phones_r: whether to reverse phones
        :return: the diphone sequence
        """
        if word_list:
            word_list_to_transfer = word_list
        else:
            word_list_to_transfer = self.normalised_words_list

        # to reverse words
        if words_r:
            word_list_to_transfer = word_list_to_transfer[::-1]

        # transfer phrase to phone sequence
        phone_seq = []
        for n_word in word_list_to_transfer:
            if n_word in ',.:?!{}':
                phone_seq.append(n_word)
            elif n_word in list(cmudict.dict().keys()):
                phone_seq.append(cmudict.dict()[n_word][0])
            else:
                raise ValueError("The word '" + n_word +
                                 "' in the input '" + self.source + "' cannot find corresponding phones.")

        # to reverse phones
        if phones_r:
            phone_seq_temp = []
            for index in range(len(phone_seq)):
                phone_seq_temp.append(phone_seq[len(phone_seq) - 1 - index][::-1])
            phone_seq = phone_seq_temp

        # transfer phone sequence to diphone sequence
        diphone_seq = []
        emphasis_signal = False
        for phone_of_word in phone_seq:
            if type(phone_of_word) is str and phone_of_word in ',.:?!':
                diphone_seq.append(phone_of_word)
            elif type(phone_of_word) is str and phone_of_word in '{}':
                if not emphasis_signal:
                    self.e_start_i = len(diphone_seq)
                    emphasis_signal = not emphasis_signal
                else:
                    self.e_end_i = len(diphone_seq)
                    emphasis_signal = not emphasis_signal
                #emphasis_signal = not emphasis_signal
            else:
                # if emphasis_signal:
                #     self.e_start_i = len(diphone_seq)
                for n in range(len(phone_of_word) + 1):
                    if n == 0:
                        diphone = 'pau' + '-' + ''.join(list(filter(str.isalpha, phone_of_word[n].lower())))
                    elif n == len(phone_of_word):
                        diphone = ''.join(list(filter(str.isalpha, phone_of_word[-1].lower()))) + '-' + 'pau'
                    else:
                        diphone = ''.join(list(filter(str.isalpha, phone_of_word[n - 1].lower()))) + '-' + ''.join(
                            list(filter(str.isalpha, phone_of_word[n].lower())))
                    diphone_seq.append(diphone)
                # if emphasis_signal:
                #     self.e_end_i = len(diphone_seq)

        return diphone_seq

    def get_spell_diphone_seq(self, words_r=False, phones_r=False):
        """
        Transfer phrase to spelling form
        :param words_r: whether to reverse word order
        :param phones_r: whether to revese phone order
        :return: the phrase in spelling form
        """
        original_word_list = self.normalised_words_list
        processed_word_list = []
        for word in original_word_list:
            for char in word:
                processed_word_list.append(char)
        return self.get_diphone_seq(word_list=processed_word_list, words_r=words_r, phones_r=phones_r)

    def emphasis_markup(self):
        return (self.e_start_i, self.e_end_i) if 0 <= self.e_start_i < self.e_end_i else None


# NOTE: DO NOT CHANGE ANY OF THE ARGPARSE ARGUMENTS - CHANGE NOTHING IN THIS FUNCTION
def process_commandline():
    parser = argparse.ArgumentParser(
        description='A basic text-to-speech app that synthesises speech using diphone concatenation.')

    # basic synthesis arguments
    parser.add_argument('--diphones', default="./diphones",
                        help="Folder containing diphone wavs")
    parser.add_argument('--play', '-p', action="store_true", default=False,
                        help="Play the output audio")
    parser.add_argument('--outfile', '-o', action="store", dest="outfile",
                        help="Save the output audio to a file", default=None)
    parser.add_argument('phrase', nargs='?',
                        help="The phrase to be synthesised")

    # Arguments for extension tasks
    parser.add_argument('--volume', '-v', default=None, type=int,
                        help="An int between 0 and 100 representing the desired volume")
    parser.add_argument('--spell', '-s', action="store_true", default=False,
                        help="Spell the input text instead of pronouncing it normally")
    parser.add_argument('--reverse', '-r', action="store", default=None, choices=['words', 'phones', 'signal'],
                        help="Speak backwards in a mode specified by string argument: 'words', 'phones' or 'signal'")
    parser.add_argument('--fromfile', '-f', action="store", default=None,
                        help="Open file with given name and synthesise all text, which can be multiple sentences.")
    parser.add_argument('--crossfade', '-c', action="store_true", default=False,
                        help="Enable slightly smoother concatenation by cross-fading between diphone units")

    args = parser.parse_args()

    if (args.fromfile and args.phrase) or (not args.fromfile and not args.phrase):
        parser.error('Must supply either a phrase or "--fromfile" to synthesise (but not both)')

    return args


if __name__ == "__main__":
    args = process_commandline()
    utt = Utterance(args.fromfile, fromfile=True) if args.fromfile else Utterance(args.phrase)

    words_reverse = False
    phones_reverse = False
    signal_reverse = False
    if args.reverse == 'words':
        words_reverse = True
    elif args.reverse == 'phones':
        phones_reverse = True
    elif args.reverse == 'signal':
        signal_reverse = True

    if args.spell:
        phone_seq = utt.get_spell_diphone_seq(words_r=words_reverse, phones_r=phones_reverse)
    else:
        phone_seq = utt.get_diphone_seq(words_r=words_reverse, phones_r=phones_reverse)

    diphone_synth = Synth(wav_folder=args.diphones)

    output_filename = args.outfile if args.outfile else 'out_file.wav'

    diphone_synth.get_diphone_seq_concatenation(phone_seq, output_filename, signal_r=signal_reverse,
                                                emphasis_i=utt.emphasis_markup(), crossfade=args.crossfade)

    out = simpleaudio.Audio()
    out.load(output_filename)

    if args.volume:
        if args.volume < 0 or args.volume > 100:
            raise ValueError("Expected volume value between 0 and 100.")
        out.rescale(args.volume / 100)

    if args.play: out.play()

