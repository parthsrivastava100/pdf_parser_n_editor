import nltk


def npchunk_features(sentence, i, history):
    word, pos = sentence[i]
    
    # Detect the previous word and part of speech
    if i == 0:
        prev_word, prev_pos = "<START>", "<START>"
    else:
        prev_word, prev_pos = sentence[i - 1]
    
    # Detect the next word and part of speech
    if i == len(sentence) - 1:
        next_word, next_pos = "<END>", "<END>"
    else:
        next_word, next_pos = sentence[i + 1]
    return {
        "pos": pos,
        "prev_pos": prev_pos,
        "word": word,
        "next_pos": next_pos,
        "prev_pos_and_pos": f"{prev_pos}+{pos}",
        "pos_and_next_pos": f"{pos}+{next_pos}",
        "tags_since_dt": tags_since_dt(sentence, i)
    }


def tags_since_dt(sentence, i):
    tags = set()
    for word, pos in sentence[:i]:
        if pos == 'DT':
            tags = set()
        else:
            tags.add(pos)
    return '+'.join(sorted(tags))


class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_data):
        self.train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sentence)] for sentence in train_data]
        self.tagger = nltk.UnigramTagger(self.train_data)
    
    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag) in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


class BigramChunker(nltk.ChunkParserI):
    def __init__(self, train_data):
        self.train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sentence)] for sentence in train_data]
        self.tagger = nltk.BigramTagger(self.train_data)
    
    def parse(self, sentence):
        pos_tags = [pos for (word, pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word, pos), chunktag) in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


class ConsecutiveNPChunkTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history)
                train_set.append((featureset, tag))
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train(
            train_set, algorithm='IIS', trace=0)
    
    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)


class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        tagged_sents = [[((w, t), c) for (w, t, c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)
    
    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w, t, c) for ((w, t), c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)
