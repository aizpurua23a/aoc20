

#Cryptographic handshake
# start with one
# subject number
# loop size
# remainder after dividing by 20201227

# transmitting public keys

# calculating the same encryption key in both situations.

class CryptoDoor_1:
    def __init__(self):
        # reading input
        self.card_public_key = 10705932
        self.door_public_key = 12301431

        # constants
        self.subject_number = 7
        self.divisor = 20201227

    def guess_card_loop_size(self):
        loop_size = 0
        result = None
        public_key_candidate = 1

        while public_key_candidate != self.card_public_key:
            public_key_candidate = public_key_candidate * self.subject_number
            public_key_candidate = public_key_candidate % self.divisor

            loop_size += 1

        return loop_size

    def guess_door_loop_size(self):
        loop_size = 0
        result = None
        public_key_candidate = 1

        while public_key_candidate != self.door_public_key:
            public_key_candidate = public_key_candidate * self.subject_number
            public_key_candidate = public_key_candidate % self.divisor

            loop_size += 1

        return loop_size

    def transform(self, subject_number, loop_size):
        public_key_candidate = 1
        for _ in range(loop_size):
            public_key_candidate = public_key_candidate * subject_number
            public_key_candidate = public_key_candidate % self.divisor

        return public_key_candidate


if __name__ == '__main__':
    cd = CryptoDoor_1()
    print(cd.transform(cd.door_public_key, cd.guess_card_loop_size()))
