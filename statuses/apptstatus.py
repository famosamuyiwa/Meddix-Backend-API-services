import enum

class ApptStatus(enum.Enum):

    PENDING = 'PENDING'
    SCHEDULED = 'SCHEDULED'
    RESCHEDULED = 'RESCHEDULED'
    CANCELED = 'CANCELED'
    COMPLETED ='COMPLETED'
    DONE = 'DONE'

    

    def __repr__(self):
        return str(self.value)