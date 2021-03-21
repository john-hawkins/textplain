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
        self.create_sentence_punctuation_arrays(textblock)        

    def get_sentences(self):
        return self.sentences

    def break_into_sentences(self, textvalue):
        """
        Utility function to split a block of text into its constituent sentences. 
        """
        sentences = re.split( "[.?!\n]", textvalue )
        sentences = [x.strip() for x in sentences]
        if "" in sentences:
            sentences.remove("")
        return sentences

    def create_sentence_punctuation_arrays(self, textvalue):
        """
        Utility function. We want the text block broken into arrays of 
        both sentences and punctuation
        """
        self.allsent = re.split( "([.?!\n]+[ \t]*)", textvalue )
        self.punct = {}
        self.sents = {}
        for i,sent in enumerate(self.allsent):
            if self.is_punct(sent):
                self.punct[i] = sent
            else:
                self.sents[i] = sent

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
        result = ""
        for i,sent in enumerate(self.allsent):
            if index==i:
                result = result + replacement
            else:
                result = result + sent
        return result


