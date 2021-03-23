import re

class Textplain:
    """
    Texplain Class.
    This is a data structure to contain the explanation of contributions
    from a specific block of text.
    """

    def __init__(self, textblock, baseline, null_score):
        """
        Initialise a text explanation with the textblock and scores.

        :param textblock: The text block that we want to explain. 
        :type textblock: string, required

        :param baseline: The baseline score for the record.
        :type baseline: float, required

        :param null_score: The score when all text is removed.
        :type null_score: float, required

        :return: Null
        :rtype: Null
        """
        self.baseline = baseline
        self.textblock = textblock
        self.null_score = null_score
        self.impact = baseline - null_score
        self.abs_impact = abs(self.impact)
        self.sentences = self.break_into_sentences(textblock)


    def get_sentences(self):
        """
        Retrieve the list of sentences
        """
        return self.sentences


    def break_into_sentences(self, textvalue):
        """
        Utility function to split a block of text into its constituent sentences. 
        """
        self.create_sentence_punctuation_arrays(textvalue)
        return self.sents


    def create_sentence_punctuation_arrays(self, textvalue):
        """
        Utility function. We want the text block broken into arrays of 
        both sentences and punctuation. Then we want to populate class
        variables that are used to manipulate and re-create the textblock.

        :param textvalue: The text to break into parts.
        :type textvalue: string, required

        :return: Null
        :rtype: Null
        """
        self.allsent = re.split( "([.?!\n]+[ \t]*)", textvalue )
        if "" in self.allsent:
            self.allsent.remove("")
        self.punct = []
        self.sents = []
        self.explanations= []
        self.index_translator = []
        for i,sent in enumerate(self.allsent):
            if self.is_punct(sent):
                self.punct.append(sent)
            else:
                self.sents.append(sent)
                self.index_translator.append(i)
                self.explanations.append( ([],[],[]) )

    def is_punct(self, textvalue):
        """
        Utility function so that the class can determine if one of the
        split sentences is a punctuation group, or text

        :param textvalue: The text to test for punctuation.
        :type textvalue: string, required

        :return: Indication as to whether the text is a punctuation block.
        :rtype: boolean
        """
        pattern = re.compile("\\.|\\?|\\!|\\n")
        if len( pattern.findall(textvalue) ) > 0 :
            return True
        else:
            return False

    def generate_modified_textblock(self, replacement, index):
        """
        Generate a modified version of the text block by modifying
        the sentence at a specific index.

        :param replacement: The text that will replace the target sentence.
        :type replacement: string, required

        :param index: The index of the sentence in the textblock
        :type index: int, required

        :return: Modified textblock with replacement inserted
        :rtype: String
        """
        blockindex = self.index_translator[index]
        result = ""
        for i,sent in enumerate(self.allsent):
            if blockindex==i:
                result = result + replacement
            else:
                result = result + sent
        return result

    def add_sentence_explanation(self, index, spec, comp, poly):
        """
        Add the explanations of the contributions of each individual word in a
        sentence. Indexed by the sentence order in the text block. The explanation
        arrays should be equal to the number of words in the sentence.

        :param index: The index of the sentnce to explain.
        :type index: int, required

        :param spec: The specificity contribution to the explanations.
        :type spec: Array(float), required 

        :param comp: The complexity contribution to the explanations
        :type comp: Array(float), required

        :param poly: The polarity contribution to the explanations 
        :type poly: Array(float), required

        :return: Null
        :rtype: Null
        """
        words = self.sents[index].split(" ")
        if len(words) == len(spec) == len(comp) == len(poly):
            self.explanations[index] = (spec, comp, poly)
        else:
            raise Exception('Word level explanations not equal to number of words')


