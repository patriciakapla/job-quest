from enum import Enum


class Status(Enum):
    SAVED = 'saved'
    APPLIED = 'applied'
    SCREENING = 'screening'
    INTERVIEW = 'interview'
    TECHNICAL_TEST = 'technical_test'
    OFFER = 'offer'
    REJECTED = 'rejected'
    WITHDRAWN = 'withdrawn'
