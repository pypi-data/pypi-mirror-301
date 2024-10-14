import datetime as dt

n2wdict_de = {
    1: "eins",
    2: "zwei",
    3: "drei",
    4: "vier",
    5: "fünf",
    6: "sechs",
    7: "sieben",
    8: "acht",
    9: "neun",
    10: "zehn",
    11: "elf",
    12: "zwölf",
}

n2wdict_en = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
}


n2wdict_fr = {
    1: "une",
    2: "deux",
    3: "trois",
    4: "quatre",
    5: "cinq",
    6: "six",
    7: "sept",
    8: "huit",
    9: "neuf",
    10: "dix",
    11: "once",
    12: "douze",
}


def num2word(number: int, language: str = "de") -> str:
    match language.lower():
        case "de":
            if number < 13:
                return n2wdict_de[number]
        case "en":
            if number < 13:
                return n2wdict_en[number]
        case "fr":
            if number < 13:
                return n2wdict_fr[number]
    return str(number)


def hour2word(hour: int, language: str = "de"):
    hour = hour % 12
    if hour == 0:
        hour = 12
    match language.lower():
        case "de":
            return n2wdict_de[hour]
        case "en":
            return n2wdict_en[hour]
        case "fr":
            return n2wdict_fr[hour]
        case _:
            return "unbekannte Sprache"

def clocksays(t: dt.datetime, language: str="de", prefix: str='', suffix: str='') -> str:
    return prefix + time2words(t=t, language=language) + suffix

def time2words(t: dt.datetime, language: str="de") -> str:
    if t.minute in (1, 16, 31, 46):
        return shortly_past(minute=t.minute, hour=t.hour, languague=language)
    if t.minute in (14, 29, 44, 59):
        return shortly_before(minute=t.minute, hour=t.hour, languague=language)
    if t.minute in (0, 15, 30, 45):
        return quarter_hours(minute=t.minute, hour=t.hour, languague=language)
    if t.minute < 21:
        return minutes_past(minute=t.minute, hour=t.hour, languague=language)
    if 20 < t.minute < 30:
        return minutes_to_half(minute=t.minute, hour=t.hour, languague=language)
    if 30 < t.minute < 40:
        return minutes_past_half(minute=t.minute, hour=t.hour, languague=language)
    if t.minute == 40:
        return minutes_to(minute=t.minute, hour=t.hour, languague=language)
    if 47 < t.minute < 60:
        return minutes_to(minute=t.minute, hour=t.hour, languague=language)
    return minute_time(minute=t.minute, hour=t.hour, languague=language)


def minute_time(minute: int, hour: int, languague: str = "de") -> str:
    match languague.lower():
        case "de":
            return f"{hour2word(hour=hour, language=languague)} Uhr {num2word(minute, language=languague)}"
        case "en":
            if minute == 1:
                return f"{hour2word(hour=hour, language=languague)} o'clock and {num2word(minute, language=languague)} minute"
            return f"{hour2word(hour=hour, language=languague)} o'clock and {num2word(minute, language=languague)} minutes"
        case "fr":
            if hour == 1:
                return f"{hour2word(hour=hour, language=languague)} heure {num2word(minute, language=languague)}"
            return f"{hour2word(hour=hour, language=languague)} heures {num2word(minute, language=languague)}"
        case _:
            return "unbekannte Sprache"


def minutes_past(minute: int, hour: int, languague: str = "de") -> str:
    match languague:
        case "de":
            return f"{num2word(number=minute, language=languague)} nach {hour2word(hour=hour, language=languague)}"
        case "en":
            return f"{num2word(number=minute, language=languague)} past {hour2word(hour=hour, language=languague)}"
        case "fr":
            if hour == 1: 
                return f"{hour2word(hour=hour, language=languague)} heure {num2word(number=minute, language=languague)}"
            return f"{hour2word(hour=hour, language=languague)} heures {num2word(number=minute, language=languague)}"
        case _:
            return "unbekannte Sprache"


def minutes_to(minute: int, hour: int, languague: str = "de") -> str:
    minutes = 60 - minute
    match languague:
        case "de":
            return f"{num2word(number=minutes, language=languague)} vor {hour2word(hour=hour+1, language=languague)}"
        case "en":
            return f"{num2word(number=minutes, language=languague)} to {hour2word(hour=hour+1, language=languague)}"
        case "fr":
            return f"{hour2word(hour=hour+1, language=languague)} moins {num2word(number=minutes, language=languague)}"
        case _:
            return "unbekannte Sprache"


def minutes_to_half(minute: int, hour: int, languague: str = "de") -> str:
    minutes = 30 - minute
    match languague:
        case "de":
            return f"{num2word(number=minutes, language=languague)} vor halb {hour2word(hour=hour+1, language=languague)}"
        case "en":
            return f"{num2word(number=minutes, language=languague)} to half past {hour2word(hour=hour, language=languague)}"
        case "fr":
            if hour == 1:
                return f"{hour2word(hour=hour, language=languague)} heure moins {num2word(number=minutes, language=languague)}"
            return f"{hour2word(hour=hour, language=languague)} heures moins {num2word(number=minutes, language=languague)}"
        case _:
            return "unbekannte Sprache"


def minutes_past_half(minute: int, hour: int, languague: str = "de") -> str:
    minute = minute - 30
    match languague:
        case "de":
            return f"{num2word(number=minute, language=languague)} nach halb {hour2word(hour=hour+1, language=languague)}"
        case "en":
            return f"{num2word(number=minute, language=languague)} past half past {hour2word(hour=hour, language=languague)}"
        case "fr":
            if minute == 1:
                if hour == 1:
                    return f"{hour2word(hour=hour+1, language=languague)} heure et demie et {num2word(number=minute, language=languague)} minute"
                return f"{hour2word(hour=hour+1, language=languague)} heures et demie et {num2word(number=minute, language=languague)} minute"
            else:
                if hour == 1:
                    return f"{hour2word(hour=hour+1, language=languague)} heure et demie et {num2word(number=minute, language=languague)} minutes"
            return f"{hour2word(hour=hour+1, language=languague)} heures et demie et {num2word(number=minute, language=languague)} minutes"
        case _:
            return "unbekannte Sprache"


def quarter_hours(minute: int, hour: int, languague: str = "de") -> str:
    match languague:
        case "de":
            if minute == 0:
                return f"{hour2word(hour=hour, language=languague)} Uhr"
            elif minute == 15:
                return f"viertel nach {hour2word(hour=hour, language=languague)}"
            elif minute == 30:
                return f"halb {hour2word(hour=hour+1, language=languague)}"
            elif minute == 45:
                return f"viertel vor {hour2word(hour=hour+1, language=languague)}"
        case "en":
            if minute == 0:
                return f"{hour2word(hour=hour, language=languague)} o'clock"
            elif minute == 15:
                return f"a quarter past {hour2word(hour=hour, language=languague)}"
            elif minute == 30:
                return f"half past {hour2word(hour=hour, language=languague)}"
            elif minute == 45:
                return f"a quarter to {hour2word(hour=hour+1, language=languague)}"
        case "fr":
            if minute == 0:
                if hour == 1:
                    return f"{hour2word(hour=hour, language=languague)} heure"
                return f"{hour2word(hour=hour, language=languague)} heures"
            elif minute == 15:
                if hour==1:
                    return f"{hour2word(hour=hour, language=languague)} heure et quart"
                return f"{hour2word(hour=hour, language=languague)} heures et quart"
            elif minute == 30:
                if hour==1:
                    return f"{hour2word(hour=hour, language=languague)} heure et demie"
                return f"{hour2word(hour=hour, language=languague)} heures et demie"
            elif minute == 45:
                return f"a quarter to {hour2word(hour=hour+1, language=languague)}"
        case _:
            return "unbekannte Sprache"


def shortly_past(minute: int, hour: int, languague: str = "de") -> str:
    match languague:
        case "de":
            if minute < 15:
                return f"kurz nach {hour2word(hour=hour, language=languague)}"
            elif minute < 30:
                return f"kurz nach viertel nach {hour2word(hour=hour, language=languague)}"
            elif minute < 45:
                return f"kurz nach halb {hour2word(hour=hour+1, language=languague)}"
            elif minute < 60:
                return f"kurz nach viertel vor {hour2word(hour=hour+1, language=languague)}"
        case "en":
            if minute < 15:
                return f"shortly past {hour2word(hour=hour, language=languague)}"
            elif minute < 30:
                return f"shortly past a quarter past {hour2word(hour=hour, language=languague)}"
            elif minute < 45:
                return f"shortly past half past {hour2word(hour=hour, language=languague)}"
            elif minute < 60:
                return f"shortly past a quarter to {hour2word(hour=hour+1, language=languague)}"
        case "fr":
            if minute < 15:
                if hour==1:
                    return f"juste après {hour2word(hour=hour, language=languague)} heure"
                return f"juste après {hour2word(hour=hour, language=languague)} heures"
            elif minute < 30:
                if hour == 1:
                    return f"juste après {hour2word(hour=hour, language=languague)} heure et quart"
                return f"juste après {hour2word(hour=hour, language=languague)} heures et quart"
            elif minute < 45:
                if hour == 1:
                    return f"juste après {hour2word(hour=hour, language=languague)} heure et demie"
                return f"juste après {hour2word(hour=hour, language=languague)} heures et demie"
            elif minute < 60:
                if hour == 1: 
                    return f"juste après {hour2word(hour=hour+1, language=languague)} heure moins quart"
                return f"juste après {hour2word(hour=hour+1, language=languague)} heures moins quart"
        case _:
            return "unbekannte Sprache"


def shortly_before(minute: int, hour: int, languague: str = "de") -> str:
    match languague:
        case "de":
            if minute < 15:
                return f"kurz vor viertel nach {hour2word(hour=hour, language=languague)}"
            elif minute < 30:
                return f"kurz halb {hour2word(hour=hour+1, language=languague)}"
            elif minute < 45:
                return f"kurz vor viertel vor {hour2word(hour=hour+1, language=languague)}"
            elif minute < 60:
                return f"kurz vor {hour2word(hour=hour+1, language=languague)}"
        case "en":
            if minute < 15:
                return f"shortly before a quarter to {hour2word(hour=hour, language=languague)}"
            elif minute < 30:
                return f"shortly before half past {hour2word(hour=hour, language=languague)}"
            elif minute < 45:
                return f"shortly before a quarter to {hour2word(hour=hour+1, language=languague)}"
            elif minute < 60:
                return f"shortly before {hour2word(hour=hour+1, language=languague)}"
        case "fr":
            if minute < 15:
                if hour == 1:
                    return f"juste avant {hour2word(hour=hour, language=languague)} heure et quart"
                return f"juste avant {hour2word(hour=hour, language=languague)} heures et quart"
            elif minute < 30:
                if hour == 1:
                    return f"juste avant {hour2word(hour=hour, language=languague)} heure et demie"
                return f"juste avant {hour2word(hour=hour, language=languague)} heures et demie"
            elif minute < 45:
                if hour == 1:
                    return f"juste avant {hour2word(hour=hour+1, language=languague)} heure moins quart"
                return f"juste avant {hour2word(hour=hour+1, language=languague)} heures moins quart"
            elif minute < 60:
                if hour == 1: 
                    return f"just avant {hour2word(hour=hour+1, language=languague)} heure"
                return f"just avant {hour2word(hour=hour+1, language=languague)} heures"
        case _:
            return "unbekannte Sprache"


def main():
    pass


if __name__ == "__main__":
    main()
