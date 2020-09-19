textplain
----------

```
Status - Planning
```

This is an application and library to provide tools to explain the elements inside a block of text that
are contributing to the output of a machine learning model.

### Initial Algorithm Idea

1. Score the original record as a benchmark
2. Identify which words and sentences contribute by iteratively removing them and
   re-scoring the record.
3. Taking the top 10 contributing words we then replace those words with synonyms
   and antnynms in order to evaluate the degree to which the word sense either
   as strength or meaning is contributing. 

### Resources & Dependencies

For Part of Speech Tagging we use [spacy](https://spacy.io/usage/spacy-101)

Note: After install you will need to get spaCy to download the English model.
```
sudo python3 -m spacy download en
```


