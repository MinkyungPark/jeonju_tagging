import re
import unicodedata


def unicode_norm(sent):
    normalized = unicodedata.normalize("NFC", sent)
    return normalized


def cleaning(sent):
    if sent:
        sent = unicode_norm(sent)
        cleaned = re.sub(r"\W", " ", sent)  # 특수문자
        cleaned = re.sub(r"[0-9]", " ", cleaned)  # 숫자
        #         cleaned = re.sub(r"[^ a-z|A-Z|가-힣]+", " ", cleaned.lower()) # 영어, 한글 아닌 것
        #         cleaned = re.sub(r"\s[a-z]{1,2}\s", " ", cleaned) # 한글자 영어
        cleaned = re.sub(r"[^ 가-힣]+", " ", cleaned)  # 한글 아닌 것
        cleaned = cleaned.replace("\n", " ")
        cleaned = cleaned.replace("\u200d", " ")
        cleaned = re.sub(r"[\s]{2,}", " ", cleaned)  # 공백 한개로
        cleaned = cleaned.strip()
        return cleaned
    else:
        return None


def clean_symbol(text):
    text = re.sub(
        r"[-=+,#/\?;:^$@*\"“”’※~&%ㆍ.!!』_\\‘|\(\)\[\]\<\>`'…》]", " ", text
    )  # .
    return text


def remove_html(text):
    re_patterns = [r"<\/?[a-z]+\s*[^>]*?\/?>", "&(nbsp|amp|lt|gt|quot);"]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " ", text)
    return text


def phone_number_filter(text):
    re_pattern = r"\d{2,3}[-\.\s]*\d{3,4}[-\.\s]*\d{4}(?!\d)"
    new_text = re.sub(re_pattern, " tel ", text)
    re_pattern = r"\(\d{3}\)\s*\d{4}[-\.\s]??\d{4}"
    new_text = re.sub(re_pattern, " tel ", new_text)
    return new_text


def url_filter(text):
    re_patterns = [
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),|]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        r"www.+",
    ]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " url ", text)

    return text


def price_filter(text):
    text = unicode_norm(text)
    re_patterns = [
        r"\d{1,3}[,\.]\d{1,3}[만\천]?\s?[원]|\d{1,5}[만\천]?\s?[원]",
        r"[일/이/삼/사/오/육/칠/팔/구/십/백][만\천]\s?[원]",
        r"(?!-)\d{2,4}[0]{2,4}(?!년)(?!.)|\d{1,3}[,/.]\d{3}",
    ]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " money ", text)

    re_patterns = [r"\d{1,2}\s?[인]"]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " numofpeople ", text)

    return text


def time_filter(text):
    text = unicode_norm(text)
    re_patterns = [
        r"\d{2,4}[.|-|_]\d{1,2}[.|-|_]\d{1,2}",
        r"\d{1,2}[월]\s?\d{1,2}[일]",
        r"[일/월/화/수/목/금/토](요일)",
        r"d{2,4}[년]",
        r"d{1,2}[월]",
        r"d{1,2}[일]",
    ]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " datetime ", text)

    re_patterns = [r"\d{1,2}\s?[박]", r"\d{1,2}\s?[박]\s?\d{1,2}\s?[일]"]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " nighttime ", text)

    re_patterns = [
        r"\d{1,2}\s?[시]",
        r"\d{1,2}\s?[분]",
        r"\d{1,2}[:]\d{1,2}[시]?\s?[분]?",
        r"[한/두/세/네/열][시]",
        r"(다섯|여섯|일곱|여덟|아홉|열한|열두)[시]",
        r"[일/이/삼/사/오/육/칠/팔/구/십]\s?[일/이/삼/사/오/육/칠/팔/구/십]?\s?[분]",
    ]
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, " time ", text)

    return text


def remove_emoji(text):
    #     emoji_pattern = re.compile("["
    #                        u"\U0001F600-\U0001F64F"  # emoticons
    #                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    #                        u"\U00002702-\U000027B0"
    #                        "]+", flags=re.UNICODE)
    only_BMP_pattern = re.compile("[" u"\U00010000-\U0010FFFF" "]+", flags=re.UNICODE)
    text = only_BMP_pattern.sub(r"", text)  # BMP characters만
    return text


def normalization(text):
    re_patterns = [r"[ㅋ]{2,}", r"[ㅎ]{2,}", r"[ㅠ]{2,}", r"[ㅜ]{2,}"]
    changes = ["ㅋ", "ㅎ", "ㅠ", "ㅜ"]
    for change, re_pattern in zip(changes, re_patterns):
        text = re.sub(re_pattern, change, text)
    text = re.sub(r"[.]+", ".", text)
    return text


def ad_check(text):
    check = True
    if " DM " in text and " 문의 " in text:
        check = False
    if " 원 데이 " in text and " 클래스 " in text:
        check = False
    if " 속눈썹 " in text and " 연장 " in text:
        check = False
    if " 필라테스 " in text and " 문의 " in text:
        check = False

    return check


def remove_one_char(text):
    text = text.replace("ㅋ", " ")
    text = text.replace("ㅎ", " ")
    text = text.replace("ㅠ", " ")
    text = text.replace("ㅜ", " ")
    return text
