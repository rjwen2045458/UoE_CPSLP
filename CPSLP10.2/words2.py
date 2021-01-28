# modified version of the words.py module...

# Define phoneset and pronunciation support
phones = '''$>.> $>> $} $}.> $}.{ $}> $ * - . < <.< <.{ << <{ > >.> >.{ >> >{
@ @@r a aa ai b ch d dh e ei eir f g h i i@ ii iy jh k l l! lw m m! n n! ng
o oi oo ou ow p r s sh t th u uh ur uu uw v w y z zh { } }.< }.> }.{ }> }{ ~'''

phones = set(phones.split())

def is_in_phoneset(p):
    return p in phones


def check_pronunciation(pron):
    if not isinstance(pron, list):
        return False
    for phone in pron:
        if not is_in_phoneset(phone):
            return False
    return True


# Word base class
class Word:
    def __init__(self, name=None, pronunciation=None):
        self.set_name(name)
        if pronunciation is None:
            self.pronunciation = []
        else:
            if check_pronunciation(pronunciation):
                self.set_pronunciation(pronunciation)
            else:
                raise ValueError("Invalid pronunciation: {0}".format(pronunciation))
        self.count = 1

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_pronunciation(self, pron):
        self.pron = pron

    def get_pronunciation(self):
        return self.pron

    def increment_count(self):
        self.count += 1

    def get_count(self):
        return self.count

    def print_word(self):
        print("word: {0}".format(self.name))
        print("pronunciation: {0}".format(self.pron))
