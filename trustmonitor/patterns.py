pattern1 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"upos":"VERB"},
    {"norm_ner":"PER"},
]

pattern2 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"upos":"VERB"},
    #{"norm_ner":"PER"},
]

pattern3 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"upos":"VERB"},
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
]

pattern4 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"text":[",", ":"]},
    {"upos":"VERB"},
]

pattern5 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"text":[",", ":"]},
    {"upos":"VERB"},   
    {"norm_ner":"PER"},
]

pattern6 = [
    {"text":"“"},
    "*",
    {"text":"”"},
    {"text":[",", ":"]},
    {"upos":"VERB"},
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
]

pattern7 = [
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":"“"},
    "*",
    {"text":"”"}
]

pattern8 = [
    {"upos":"VERB"},
    {"text":"“"},
    "*",
    {"text":"”"}
    #{"norm_ner":"PER"},
]

pattern9 = [
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":"“"},
    "*",
    {"text":"”"}
]

pattern10 = [
    {"upos":"VERB"},
    {"text":[",", ":"]},
    {"text":"“"},
    "*",
    {"text":"”"},
]

pattern11 = [
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":[",", ":"]},
    {"text":"“"},
    "*",
    {"text":"”"}
]

pattern12 = [
    {"norm_ner":"PER"},
    {"norm_ner":"PER"},
    {"upos":"VERB"},
    {"text":[",", ":"]},
    {"text":"“"},
    "*",
    {"text":"”"}
]

patterns = {"QVP":pattern1, 
            "QV":pattern2, 
            "QVPP":pattern3, 
            "Q.V":pattern4, 
            "Q.VP":pattern5,
            "Q.VPP":pattern6,
            "PVQ":pattern7,
            "VQ":pattern8,
            "PPVQ":pattern9,
            "V.Q":pattern10,
            "PV.Q":pattern11,
            "PPV.Q":pattern12
            }