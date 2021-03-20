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
        self.impact = baseline_score - null_score
        self.abs_impact = abs(self.impact)
        self.sentences = break_into_sentences(textblock)
        

    def get_sentences(self):
        return self.sentences

    def break_into_sentences(textvalue):
        """
        Utility function to split a block of text into its constituent sentences. 
        """
        sentences = re.split( "[.?!\n]", textvalue )
        sentences = [x.strip() for x in sentences]
        if "" in sentences:
            sentences.remove("")
        return sentences



