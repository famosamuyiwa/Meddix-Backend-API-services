import enum

class PaymentStatus(enum.Enum):

    INITIATED = 'INITIATED'
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    DECLINED = 'DECLINED'
    NA = "NA"

    def __repr__(self):
        return str(self.value)