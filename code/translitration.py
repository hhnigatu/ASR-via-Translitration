"""
This script includes functions for transliterating 
Latin and Arabic script sentences to Ge'ez script 
with the Amharic language phonetic representation. 
"""
import string
import re 

from google.transliteration import transliterate_word


# Dictionary mapping for Arabic Transliteration

vowelidx={" َ  ": 0,   " ُ  ":1, "  ِ  ":2}
vowelidx={k.strip():v for k, v in vowelidx.items()} # due to encoding issues


arabic2amharic={
    "ا":"እ",
    "ى": "አ",
    "أ":"አ",
    "إ": "ኢ",
    "ب":"ብ",
    "ت":"ት",
    "ث":"ት",
    "ج":"ጅ",
    "ح" :"ሕ",
    "خ":"ኽ",
    "د":"ድ",
    "ذ":"ድ",
    "ر":"ር",
    "ز" :"ዝ",
    "س" :"ስ",
    "ش":"ሽ",
    "ص" :"ሥ",
    "ض": "ድ",
    "ظ":"ዝ",
    "ع": "ዕ",
    "غ": "ግ",
    "ف": "ፍ",
    "ق": "ቅ",
    "ك": "ክ",
    "ل": "ል",
    "م": "ም",
    "ن": "ን",
    "ه": "ህ",
    "و": "ው",
    "ي": "ይ",
    "ء": "አ",
    "ة":"አተ",
    "؟": "?",
    "ط": "ጥ",
	" ً ".strip(): "ን",
    "  ِ  ".strip(): "ኢ",
	" ُُ ".strip(): "ኡ",
	"  َ    ".strip(): "ኣ",
}

letter2family={
"እ": "ኣ ኡ ኢ".split(),
"ብ": "ባ ቡ ቢ".split(),

"ድ": "ዳ ዱ ዲ".split(),
"ጅ": "ጃ ጁ ጂ".split(),
"ፍ": "ፋ ፉ ፊ".split(),
"ህ": "ሃ ሁ ሂ".split(),
"ሕ": "ሓ ሑ ሒ".split(),
"ይ":  "ያ ዩ ዪ".split(),
"ክ":  "ካ ኩ ኪ".split(),
"ል": "ላ ሉ ሊ".split(),
"ን": "ና ኑ ኒ".split(),
"ም":  "ማ ሙ ሚ".split(),
"ቅ":  "ቃ ቁ ቂ".split(),
"ር": "ራ ሩ ሪ".split(),
"ስ":  "ሳ ሱ ሲ".split(),
"ሥ": "ሣ ሡ ሢ".split(),
"ሽ": "ሻ ሹ ሺ".split(),
"ት": "ታ ቱ ቲ".split(),
"ጥ": "ጣ ጡ ጢ".split(),
"ው": "ዋ ዉ ዊ".split(),
"ኽ": "ኻ ኹ ኺ".split(),
"ግ": "ጋ ጉ ጊ".split(),
"ዝ": "ዛ ዙ ዚ".split(),
"ዕ":"ዓ ዑ ዒ".split(),
        }

xhosa2amharic={
"a": "ኣ ", 
"b": "ብ",
"c": "ጽ",
"d": "ድ",
"e": "ኧ",
"f": "ፍ",
"g": "ግ",
"h": "ሀ",
"i": "ኢ",
"j": "ጅ",
"k": "ቅ",
"l": "ለ",
"m": "ም",
"n": "ን",
"o": "ኦ",
"p": "ጵ",
"q": "ጠ",
"r": "ር",
"s": "ስ",
"t": "ጥ",
"u": "ኡ",
"v": "ቭ",
"w": "ው",
"x": "ጭ",
"y": "ይ",
"z": "ዝ"
}

def replace_accented_characters(sentence):
    """Replace accented characters with their non-accented versions using Spanish and French pronunciation sources. Note that transliteration is an approximation and may not represent the exact phoneme.

    Args:
        sentence (str): Original transcription

    Returns:
        str: Transcription with accents replaced by their non-accented versions. 
    """
    sentence=re.sub(r'[^\w\s]', '',sentence)
    sentence=re.sub('é','e', sentence)
    sentence=re.sub('è','eh', sentence)
    sentence=re.sub('ù','ou', sentence)
    sentence=re.sub('à','a', sentence)
    sentence=re.sub('ç','s', sentence)
    sentence=re.sub('â','ah', sentence)
    sentence=re.sub('ê','eh', sentence)
    sentence=re.sub('ô','o', sentence)
    sentence=re.sub('û','u', sentence)
    sentence=re.sub('ë','e', sentence)
    sentence=re.sub('ï','i', sentence)
    sentence=re.sub('ü','u', sentence)
    sentence=re.sub('á','a', sentence)
    sentence=re.sub('í','i', sentence)
    sentence=re.sub('ú','u', sentence)
    sentence=re.sub('ó','o', sentence)
    sentence=re.sub('ñ','ny', sentence)
    
    return sentence

def latin_rule_based_transliteration(transcription):
    """Rule based mapping of Latin characters to Ge'ez characters.

    Args:
        transcription (Str): Transcription in Latin script. 

    Returns:
        Str : Transcription transliterated to Ge'ez characters.
    """
    transliterated=''
    for idx in range(len(transcription)):
        if transcription[idx].lower()>='a' and transcription[idx].lower()<='z': #check the char is in the Latin alphabet (exclusive of accents as those are replaced)
                transliterated+=xhosa2amharic[transcription[idx]] # fall back relies on the Xhosa-Amharic phonetic mapping.
        else:
            transliterated+=transcription[idx] # to account for numbers etc
            
    return transliterated

def arabic_rule_based_transliteration(transcription):
    """Rule based mapping of Arabic characters to Ge'ez characters. 

    Args:
        transcription (str): transcription in Arabic script

    Returns:
        str: transcription transliterated to Ge'ez script. 
    """
    transliterated=''
    
    for idx in range(len(transcription)):
        if idx+1==len(transcription):
            if transcription[idx] in [x.strip() for x in vowelidx.keys()]:
                continue
            elif transcription[idx]==" ً ".strip():
                transliterated+="ን"
            else:
                try:
                    transliterated+=arabic2amharic[transcription[idx]]
                except:
                    transliterated+=""
        else:
            if transcription[idx+1] in [x.strip() for x in vowelidx.keys()]:
                try:
                    transliterated+=letter2family[arabic2amharic[transcription[idx]]][vowelidx[transcription[idx+1].strip()]]
                except:
                    transliterated+=""
            elif transcription[idx] in [x.strip() for x in vowelidx.keys()]:
                continue
            elif transcription[idx]==' ':
                transliterated+=transcription[idx]
            elif transcription[idx]==" ً ".strip():
                transliterated+="ን"
            else:
                try:
                    transliterated+=arabic2amharic[transcription[idx]]
                except:
                    transliterated+=""
    

    return transliterated


def transliterate(transcription, script="latin"):
    """Function to transliterate Latin and Arabic script transcripts to Ge'ez. Uses the Google transliterate API for Latin script and falls back to rule based transliteration if the API does not transliterate. For Arabic script, uses rule based system.

    Args:
        original_transcription (Str): Transcription in Latin script. 

    Returns:
        Str : Transcription transliterated to Ge'ez characters.
    """
    
    if script=="latin": # for Latin script transcriptions (Xhosa, French, Spanish)
        transcription= replace_accented_characters(transcription)
        if len(transliterate_word(transcription, 'am'))>0: #check if API returns transliterations
            transliterated=transliterate_word(transcription, "am")[0]
        else:
            transliterated=latin_rule_based_transliteration(transcription) #fall back to rule based system
    elif script=="arabic":
        transcription=arabic_rule_based_transliteration(transcription)
        
        return transliterated