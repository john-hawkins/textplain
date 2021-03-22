import re

class Textplain:
    """
    Texplain Class.
    This is a data structure to contain the explanation of contributions
    from a specific block of text.
    """

    def __init__(self, textblock, baseline, null_score):
        """
        Initialise a text explanation from the textblock and scores.
        """
        self.baseline = baseline
        self.textblock = textblock
        self.null_score = null_score
        self.impact = baseline - null_score
        self.abs_impact = abs(self.impact)
        self.sentences = self.break_into_sentences(textblock)


    def get_sentences(self):
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
        """
        blockindex = self.index_translator[index]
        result = ""
        for i,sent in enumerate(self.allsent):
            if blockindex==i:
                result = result + replacement
            else:
                result = result + sent
        return result

    def add_sentence_explanation(self, index, specificity, complexity, polarity):
        """
        Add the explanations of the contributions of each individual word in a
        sentence. Indexed by the sentence order in the text block. The explanation
        arrays should be equal to the number of words in the sentence.
        """
        self.explanations[index] = (specificity, complexity, polarity)

