# Lists with words for names processing


FLAG_EXECUTIVE_NAME_WORDS = [
    "ceo",
    "cfo",
    "cbo",
    "cto",
    "cso",
    "cro",
    "cho",
    "ir",
    "svp",
    "vice"
    "president",
    "chief",
    "financial",
    "officer",
    "executive",
    "director",
    "member",
    "chairman",
    "founder",
    "cofounder",
    "senior",
    "manager",
    "head",
    "principal"
]

FLAG_ANALYST_NAME_WORDS = [
    "division",
    "ltd",
    "research",
    "company",
    "bank",
    "inc",
    "co",
    "group",
    "llc"
]

FLAG_COMPANY_NAME_WORDS = [
    "morgan",
    "goldman",
    "citi",
    "morning",
    "hsbc"
]

FLAG_NAME_WORDS = FLAG_EXECUTIVE_NAME_WORDS + FLAG_ANALYST_NAME_WORDS

STOP_NAME_WORDS = [
    "okay",
    "thank",
    "you",
    "thanks",
    "bye",
    "hello",
    "good",
    "afternoon",
    "evening",
    "morning",
    "night",
    "welcome",
    "yes",
    "when",
    "that",
    "but",
    "about",
    "we",
    "me",
    "our",
    "us",
    "have",
    "are",
    "is",
    "were",
    "was",
    "been"
]

DROP_STOP_WORDS = [
    "of",
    "and",
    "the",
    "a"
]

ALL_STOP_WORDS = STOP_NAME_WORDS + DROP_STOP_WORDS

