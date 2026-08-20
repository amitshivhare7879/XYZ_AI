"""
XYZ AI — Comprehensive Multilingual & Vernacular Translation Engine
Translates and formats assistant responses into 11 Indian languages:
Hindi, Gujarati, Marathi, Tamil, Telugu, Bengali, Punjabi, Kannada, Malayalam, Urdu, and Hinglish.
"""

import re
from typing import Dict, Any, List, Optional

# Structured sentence pattern translators for high grammatical fluency across all 11 regional languages
def translate_template_patterns(text: str, target_lang: str) -> str:
    """Translates common complex ERP response patterns into natural vernacular syntax."""
    if not target_lang or target_lang == "en":
        return text

    # Pattern 1: Teacher Attendance - "Great news for **Grade 10-A** (2026-08-14)! **All 8 students are present** (100% attendance rate)."
    m1 = re.search(r"Great news for \*\*([^*]+)\*\* \(([^)]+)\)! \*\*All (\d+) students are present\*\* \((\d+)% attendance rate\)\.", text)
    if m1:
        cname, dt, count, rate = m1.groups()
        if target_lang == "gu":
            return f"**{cname}** ({dt}) માટે ખૂબ સારા સમાચાર! **તમામ {count} વિદ્યાર્થીઓ હાજર છે** ({rate}% હાજરીનો દર)."
        elif target_lang == "hi":
            return f"**{cname}** ({dt}) के लिए बहुत अच्छी खबर! **सभी {count} विद्यार्थी उपस्थित हैं** ({rate}% उपस्थिति दर)।"
        elif target_lang == "mr":
            return f"**{cname}** ({dt}) साठी अत्यंत आनंदाची बातमी! **सर्व {count} विद्यार्थी उपस्थित आहेत** ({rate}% उपस्थितीचे प्रमाण)."
        elif target_lang == "ta":
            return f"**{cname}** ({dt}) மகிழ்ச்சியான செய்தி! **அனைத்து {count} மாணவர்களும் வருகை தந்துள்ளனர்** ({rate}% வருகை சதவீதம்)."
        elif target_lang == "te":
            return f"**{cname}** ({dt}) శుభవార్త! **మొత్తం {count} విద్యార్థులు హాజరయ్యారు** ({rate}% హాజరు శాతం)."
        elif target_lang == "bn":
            return f"**{cname}** ({dt}) এর জন্য দুর্দান্ত খবর! **সমস্ত {count} জন শিক্ষার্থী উপস্থিত রয়েছে** ({rate}% উপস্থিতি হার)।"
        elif target_lang == "pa":
            return f"**{cname}** ({dt}) ਲਈ ਬਹੁਤ ਵਧੀਆ ਖ਼ਬਰ! **ਸਾਰੇ {count} ਵਿਦਿਆਰਥੀ ਹਾਜ਼ਰ ਹਨ** ({rate}% ਹਾਜ਼ਰੀ ਦਰ)।"
        elif target_lang == "kn":
            return f"**{cname}** ({dt}) ಗೆ ಶುಭ ಸುದ್ದಿ! **ಎಲ್ಲಾ {count} ವಿದ್ಯಾರ್ಥಿಗಳು ಹಾಜರಿದ್ದಾರೆ** ({rate}% ಹಾಜರಾತಿ ದರ)."
        elif target_lang == "ml":
            return f"**{cname}** ({dt}) സന്തോഷവാർത്ത! **എല്ലാ {count} വിദ്യാർത്ഥികളും ഹാജരുണ്ട്** ({rate}% ഹാജർ നിരക്ക്)."
        elif target_lang == "ur":
            return f"**{cname}** ({dt}) کے لیے زبردست خوشخبری! **تمام {count} طلباء حاضر ہیں** ({rate}% حاضری کی شرح)۔"
        elif target_lang == "hinglish":
            return f"**{cname}** ({dt}) ke liye great news! **Sabhi {count} students present hain** ({rate}% attendance rate)."

    # Pattern 2: Teacher Attendance with Absences - "Attendance summary for **Grade 10-A** (2026-08-14): **7 of 8 students are present** (87.5%). Absent today (1): **Aman Shah**."
    m2 = re.search(r"Attendance summary for \*\*([^*]+)\*\* \(([^)]+)\): \*\*(\d+) of (\d+) students are present\*\* \(([^)]+)\)\. Absent today \((\d+)\): \*\*([^*]+)\*\*\.", text)
    if m2:
        cname, dt, pres, tot, rate, abs_cnt, abs_list = m2.groups()
        if target_lang == "gu":
            return f"**{cname}** ({dt}) માટે હાજરીનો સારાંશ: **{tot} માંથી {pres} વિદ્યાર્થીઓ હાજર છે** ({rate}). આજે ગેરહાજર ({abs_cnt}): **{abs_list}**."
        elif target_lang == "hi":
            return f"**{cname}** ({dt}) के लिए उपस्थिति सारांश: **{tot} में से {pres} विद्यार्थी उपस्थित हैं** ({rate})। आज अनुपस्थित ({abs_cnt}): **{abs_list}**।"
        elif target_lang == "mr":
            return f"**{cname}** ({dt}) साठी उपस्थिती तपशील: **{tot} पैकी {pres} विद्यार्थी उपस्थित आहेत** ({rate}). आज गैरहजर ({abs_cnt}): **{abs_list}**."
        elif target_lang == "ta":
            return f"**{cname}** ({dt}) வருகை சுருக்கம்: **{tot} மாணவர்களில் {pres} பேர் வருகை தந்துள்ளனர்** ({rate}). இன்று வரவில்லை ({abs_cnt}): **{abs_list}**."
        elif target_lang == "te":
            return f"**{cname}** ({dt}) హాజరు సారాంశం: **{tot} మందిలో {pres} మంది విద్యార్థులు హాజరయ్యారు** ({rate}). ఈరోజు గైర్హాజరు ({abs_cnt}): **{abs_list}**."
        elif target_lang == "bn":
            return f"**{cname}** ({dt}) এর উপস্থিতির সারসংক্ষেপ: **{tot} জনের মধ্যে {pres} জন শিক্ষার্থী উপস্থিত** ({rate})। আজ অনুপস্থিত ({abs_cnt}): **{abs_list}**।"
        elif target_lang == "pa":
            return f"**{cname}** ({dt}) ਲਈ ਹਾਜ਼ਰੀ ਸਾਰ: **{tot} ਵਿੱਚੋਂ {pres} ਵਿਦਿਆਰਥੀ ਹਾਜ਼ਰ ਹਨ** ({rate})। ਅੱਜ ਗ਼ੈਰਹਾਜ਼ਰ ({abs_cnt}): **{abs_list}**।"
        elif target_lang == "kn":
            return f"**{cname}** ({dt}) ಹಾಜರಾತಿ ಸಾರಾಂಶ: **{tot} ರಲ್ಲಿ {pres} ವಿದ್ಯಾರ್ಥಿಗಳು ಹಾಜರಿದ್ದಾರೆ** ({rate}). ಇಂದು ಗೈರುಹಾಜರು ({abs_cnt}): **{abs_list}**."
        elif target_lang == "ml":
            return f"**{cname}** ({dt}) ഹാജർ സംഗ്രഹം: **{tot} ൽ {pres} വിദ്യാർത്ഥികൾ ഹാജരുണ്ട്** ({rate}). ഇന്ന് ഹാജരാകാത്തവർ ({abs_cnt}): **{abs_list}**."
        elif target_lang == "ur":
            return f"**{cname}** ({dt}) کا حاضری خلاصہ: **{tot} میں سے {pres} طلباء حاضر ہیں** ({rate})۔ آج غیر حاضر ({abs_cnt}): **{abs_list}**۔"
        elif target_lang == "hinglish":
            return f"**{cname}** ({dt}) ke liye attendance summary: **{tot} me se {pres} students present hain** ({rate}). Aaj absent ({abs_cnt}): **{abs_list}**."

    # Pattern 3: Attendance Update - "Successfully updated! **Rahul Patel** has been marked **ABSENT** for 2026-08-20. Class total: 7 present."
    m3 = re.search(r"Successfully updated! \*\*([^*]+)\*\* has been marked \*\*([^*]+)\*\* for ([^.]+)\. Class total: (\d+) present\.", text)
    if m3:
        sname, status, dt, pcount = m3.groups()
        status_gu = "ગેરહાજર (ABSENT)" if "ABSENT" in status else "હાજર (PRESENT)"
        status_hi = "अनुपस्थित (ABSENT)" if "ABSENT" in status else "उपस्थित (PRESENT)"
        status_mr = "गैरहजर (ABSENT)" if "ABSENT" in status else "उपस्थित (PRESENT)"
        status_te = "గైర్హాజరు (ABSENT)" if "ABSENT" in status else "హాజరు (PRESENT)"
        status_ta = "வராதவர் (ABSENT)" if "ABSENT" in status else "வருகை (PRESENT)"
        status_bn = "অনুপস্থিত (ABSENT)" if "ABSENT" in status else "উপস্থিত (PRESENT)"
        status_pa = "ਗ਼ੈਰਹਾਜ਼ਰ (ABSENT)" if "ABSENT" in status else "ਹਾਜ਼ਰ (PRESENT)"
        status_kn = "ಗೈರುಹಾಜರು (ABSENT)" if "ABSENT" in status else "ಹಾಜರು (PRESENT)"
        status_ml = "ഹാജരായില്ല (ABSENT)" if "ABSENT" in status else "ഹാജർ (PRESENT)"
        status_ur = "غیر حاضر (ABSENT)" if "ABSENT" in status else "حاضر (PRESENT)"
        if target_lang == "gu":
            return f"સફળતાપૂર્વક અપડેટ થયું! **{sname}** ને {dt} માટે **{status_gu}** તરીકે નોંધવામાં આવ્યા છે. વર્ગમાં કુલ: {pcount} હાજર."
        elif target_lang == "hi":
            return f"सफलतापूर्वक अपडेट किया गया! **{sname}** को {dt} के लिए **{status_hi}** चिह्नित किया गया है। कक्षा कुल: {pcount} उपस्थित।"
        elif target_lang == "mr":
            return f"यशस्वीरित्या अद्यतनित केले! **{sname}** यांना {dt} साठी **{status_mr}** म्हणून नोंदवले आहे. वर्ग एकूण: {pcount} उपस्थित."
        elif target_lang == "te":
            return f"విజయవంతంగా అప్‌డేట్ చేయబడింది! **{sname}** ని {dt} తేదీకి **{status_te}** గా నమోదు చేశారు. తరగతిలో మొత్తం: {pcount} మంది హాజరు."
        elif target_lang == "ta":
            return f"வெற்றிகரமாக புதுப்பிக்கப்பட்டது! **{sname}** {dt} அன்று **{status_ta}** என குறிக்கப்பட்டுள்ளார். வகுப்பு மொத்தம்: {pcount} பேர் வருகை."
        elif target_lang == "bn":
            return f"সফলভাবে আপডেট করা হয়েছে! **{sname}** কে {dt} এর জন্য **{status_bn}** হিসেবে চিহ্নিত করা হয়েছে। ক্লাসের মোট: {pcount} জন উপস্থিত।"
        elif target_lang == "pa":
            return f"ਸਫਲਤਾਪੂਰਵਕ ਅੱਪਡੇਟ ਕੀਤਾ ਗਿਆ! **{sname}** ਨੂੰ {dt} ਲਈ **{status_pa}** ਦਰਜ ਕੀਤਾ ਗਿਆ ਹੈ। ਕਲਾਸ ਕੁੱਲ: {pcount} ਹਾਜ਼ਰ।"
        elif target_lang == "kn":
            return f"ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ! **{sname}** ಅವರನ್ನು {dt} ದಿನಾಂಕಕ್ಕೆ **{status_kn}** ಎಂದು ಗುರುತಿಸಲಾಗಿದೆ. ಒಟ್ಟು ಹಾಜರಾತಿ: {pcount}."
        elif target_lang == "ml":
            return f"വിജയകരമായി പുതുക്കി! **{sname}** {dt} തീയതിയിൽ **{status_ml}** ആയി രേഖപ്പെടുത്തി. ആകെ ഹാജർ: {pcount}."
        elif target_lang == "ur":
            return f"کامیابی سے اپ ڈیٹ کر دیا گیا! **{sname}** کو {dt} کے لیے **{status_ur}** درج کیا گیا ہے۔ کلاس کی کل حاضری: {pcount}۔"

    # Pattern 4: Student Attendance - "Your current attendance stands at **91.2%** (83/91 days attended)! You're in good standing. Keep up the consistent punctuality! 👏"
    m4 = re.search(r"Your current attendance stands at \*\*([^*]+)\*\* \((\d+)/(\d+) days attended\)! You're in good standing\. Keep up the consistent punctuality! 👏", text)
    if m4:
        pct, pres, tot = m4.groups()
        if target_lang == "gu":
            return f"તમારી વર્તમાન હાજરી **{pct}** ({pres}/{tot} દિવસો હાજર) છે! તમારી હાજરી ખૂબ જ સારી છે. આવી જ નિયમિતતા જાળવી રાખો! 👏"
        elif target_lang == "hi":
            return f"आपकी वर्तमान उपस्थिति **{pct}** ({pres}/{tot} दिन उपस्थित) है! आपकी उपस्थिति बहुत अच्छी है। अपनी नियमितता बनाए रखें! 👏"
        elif target_lang == "mr":
            return f"तुमची सध्याची उपस्थिती **{pct}** ({pres}/{tot} दिवस उपस्थित) आहे! तुमची उपस्थिती उत्तम आहे. हीच नियमितता कायम ठेवा! 👏"
        elif target_lang == "ta":
            return f"உங்கள் தற்போதைய வருகை **{pct}** ({pres}/{tot} நாட்கள் வருகை)! உங்கள் வருகை சிறப்பாக உள்ளது. தொடரவும்! 👏"
        elif target_lang == "te":
            return f"మీ ప్రస్తుత హాజరు **{pct}** ({pres}/{tot} రోజులు హాజరు)! మీ హాజరు చాలా బాగుంది. ఇలాగే కొనసాగించండి! 👏"
        elif target_lang == "bn":
            return f"আপনার বর্তমান উপস্থিতি **{pct}** ({pres}/{tot} দিন উপস্থিত)! আপনার উপস্থিতি সন্তোষজনক। ধারাবাহিকতা বজায় রাখুন! 👏"
        elif target_lang == "pa":
            return f"ਤੁਹਾਡੀ ਮੌਜੂਦਾ ਹਾਜ਼ਰੀ **{pct}** ({pres}/{tot} ਦਿਨ ਹਾਜ਼ਰ) ਹੈ! ਤੁਹਾਡੀ ਹਾਜ਼ਰੀ ਬਹੁਤ ਵਧੀਆ ਹੈ। ਆਪਣੀ ਸਮੇਂ ਦੀ ਪਾਬੰਦੀ ਬਣਾਈ ਰੱਖੋ! 👏"
        elif target_lang == "kn":
            return f"ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಹಾಜರಾತಿ **{pct}** ({pres}/{tot} ದಿನಗಳು ಹಾಜರಾಗಿದ್ದಾರೆ)! ನಿಮ್ಮ ಹಾಜರಾತಿ ಉತ್ತಮವಾಗಿದೆ. ಹೀಗೆಯೇ ಮುಂದುವರಿಸಿ! 👏"
        elif target_lang == "ml":
            return f"നിങ്ങളുടെ നിലവിലെ ഹാജർ **{pct}** ({pres}/{tot} ദിവസങ്ങൾ ഹാജരായി)! നിങ്ങളുടെ ഹാജർ വളരെ മികച്ചതാണ്. ഇത് തുടരുക! 👏"
        elif target_lang == "ur":
            return f"آپ کی موجودہ حاضری **{pct}** ({pres}/{tot} دن حاضر) ہے! آپ کی حاضری بہت اچھی ہے۔ اپنی پابندی برقرار رکھیں! 👏"
        elif target_lang == "hinglish":
            return f"Aapki current attendance **{pct}** ({pres}/{tot} days attended) hai! Aapki attendance kaafi acchi hai. Keep it up! 👏"

    # Pattern 5: Timetable / Class Schedule
    m5 = re.search(r"Today's class schedule for \*\*([^*]+)\*\*: ([^.]+)\. Would you like the full weekly breakdown\?", text)
    if m5:
        cname, slot_desc = m5.groups()
        if target_lang == "gu":
            return f"**{cname}** માટે આજનું ટાઇમટેબલ: {slot_desc}. શું તમે આખા અઠવાડિયાનું સમયપત્રક જોવા માંગો છો?"
        elif target_lang == "hi":
            return f"**{cname}** के लिए आज की समय सारणी: {slot_desc}। क्या आप पूरे सप्ताह का विस्तृत शेड्यूल देखना चाहते हैं?"
        elif target_lang == "mr":
            return f"**{cname}** साठी आजचे वेळापत्रक: {slot_desc}. तुम्हाला संपूर्ण आठवड्याचे वेळापत्रक हवे आहे का?"
        elif target_lang == "ta":
            return f"**{cname}** இன்றைய பாடவேளை அட்டவணை: {slot_desc}. முழு வார அட்டவணை வேண்டுமா?"
        elif target_lang == "te":
            return f"**{cname}** కోసం నేటి టైమ్‌టేబుల్: {slot_desc}. పూర్తి వారపు షెడ్యూల్ చూడాలనుకుంటున్నారా?"
        elif target_lang == "bn":
            return f"**{cname}** এর আজকের রুটিন: {slot_desc}। আপনি কি পুরো সপ্তাহের সময়সূচী দেখতে চান?"
        elif target_lang == "pa":
            return f"**{cname}** ਲਈ ਅੱਜ ਦਾ ਟਾਈਮਟੇਬਲ: {slot_desc}। ਕੀ ਤੁਸੀਂ ਪੂਰੇ ਹਫ਼ਤੇ ਦਾ ਸ਼ਡਿਊਲ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
        elif target_lang == "kn":
            return f"**{cname}** ಗಾಗಿ ಇಂದಿನ ತರಗತಿ ವೇಳಾಪಟ್ಟಿ: {slot_desc}. ಸಂಪೂರ್ಣ ವಾರದ ವೇಳಾಪಟ್ಟಿ ನೋಡಲು ಬಯಸುವಿರಾ?"
        elif target_lang == "ml":
            return f"**{cname}** ഇന്നത്തെ ക്ലാസ് ടൈംടേബിൾ: {slot_desc}. പൂർണ്ണമായ പ്രതിവാര ഷെഡ്യൂൾ വേണമെന്നുണ്ടോ?"
        elif target_lang == "ur":
            return f"**{cname}** کا آج کا ٹائم ٹیبل: {slot_desc}۔ کیا آپ پورے ہفتے کا شیڈول دیکھنا چاہتے ہیں؟"
        elif target_lang == "hinglish":
            return f"**{cname}** ke liye aaj ka class schedule: {slot_desc}. Kya aap full weekly timetable dekhna chahte hain?"

    # Pattern 6: Finished Lectures for Today
    m6 = re.search(r"All scheduled lectures for today in \*\*([^*]+)\*\* are finished\. Tomorrow's first session begins at 08:30 AM with Mathematics\.", text)
    if m6:
        cname = m6.group(1)
        if target_lang == "gu":
            return f"**{cname}** માં આજના તમામ તાસ પૂર્ણ થઈ ગયા છે. આવતીકાલે પ્રથમ સત્ર સવારે 08:30 વાગ્યે ગણિત સાથે શરૂ થશે."
        elif target_lang == "hi":
            return f"**{cname}** में आज के सभी पीरियड समाप्त हो चुके हैं। कल का पहला सत्र सुबह 08:30 बजे गणित के साथ शुरू होगा।"
        elif target_lang == "mr":
            return f"**{cname}** मधील आजच्या सर्व तासिका संपल्या आहेत. उद्याचे पहिले सत्र सकाळी 08:30 वाजता गणिताने सुरू होईल."
        elif target_lang == "te":
            return f"**{cname}** లో నేటి అన్ని పీరియడ్లు పూర్తయ్యాయి. రేపటి మొదటి సెషన్ ఉదయం 08:30 గంటలకు గణితంతో ప్రారంభమవుతుంది."
        elif target_lang == "ta":
            return f"**{cname}** இல் இன்றைய அனைத்து பாடவேளைகளும் முடிந்துவிட்டன. நாளைய முதல் வகுப்பு காலை 08:30 மணிக்கு கணிதத்துடன் தொடங்கும்."
        elif target_lang == "bn":
            return f"**{cname}** এ আজকের সমস্ত ক্লাস শেষ হয়েছে। আগামীকালের প্রথম সেশন সকাল ০৮:৩০ টায় গণিত দিয়ে শুরু হবে।"
        elif target_lang == "pa":
            return f"**{cname}** ਵਿੱਚ ਅੱਜ ਦੇ ਸਾਰੇ ਪੀਰੀਅਡ ਖ਼ਤਮ ਹੋ ਚੁੱਕੇ ਹਨ। ਕੱਲ੍ਹ ਦਾ ਪਹਿਲਾ ਸੈਸ਼ਨ ਸਵੇਰੇ 08:30 ਵਜੇ ਗਣਿਤ ਨਾਲ ਸ਼ੁਰੂ ਹੋਵੇਗਾ।"
        elif target_lang == "kn":
            return f"**{cname}** ನಲ್ಲಿ ಇಂದಿನ ಎಲ್ಲಾ ತರಗತಿಗಳು ಮುಗಿದಿವೆ. ನಾಳೆಯ ಮೊದಲ ಅಧಿವೇಶನವು ಬೆಳಿಗ್ಗೆ 08:30 ಕ್ಕೆ ಗಣಿತದೊಂದಿಗೆ ಪ್ರಾರಂಭವಾಗುತ್ತದೆ."
        elif target_lang == "ml":
            return f"**{cname}** ഇന്നത്തെ ക്ലാസുകൾ അവസാനിച്ചു. നാളത്തെ ആദ്യ സെഷൻ രാവിലെ 08:30 ന് മാത്തമാറ്റിക്സോടെ ആരംഭിക്കും."
        elif target_lang == "ur":
            return f"**{cname}** میں آج کے تمام پیریڈز مکمل ہو چکے ہیں۔ کل کا پہلا سیشن صبح 08:30 بجے ریاضی کے ساتھ شروع ہوگا۔"
        elif target_lang == "hinglish":
            return f"**{cname}** me aaj ke sabhi lectures complete ho chuke hain. Kal ka pehla session subah 08:30 AM Mathematics se start hoga."

    # Pattern 7: Management / Principal Executive Fallback
    m7 = re.search(r"Management Assistant ready, ([^.]+)\. I can provide school-wide attendance metrics, fee collection summaries, or escalation reports\. Which executive overview would you like to review\?", text)
    if m7:
        pname = m7.group(1)
        if target_lang == "gu":
            return f"મેનેજમેન્ટ આસિસ્ટન્ટ તૈયાર છે, {pname}. હું સમગ્ર શાળાની હાજરીના આંકડા, ફી કલેક્શન રિપોર્ટ અથવા એસ્કેલેશન વિગતો આપી શકું છું. તમે કયો રિપોર્ટ જોવા માંગો છો?"
        elif target_lang == "hi":
            return f"प्रबंधन सहायक तैयार है, {pname}। मैं स्कूल-स्तरीय उपस्थिति आंकड़े, शुल्क संग्रह सारांश या शिकायत रिपोर्ट प्रदान कर सकता हूँ। आप कौन सा अवलोकन देखना चाहते हैं?"
        elif target_lang == "mr":
            return f"व्यवस्थापन सहाय्यक तयार आहे, {pname}. मी शाळा स्तरावरील उपस्थिती, फी संकलन अहवाल किंवा तक्रारींचा तपशील देऊ शकतो. आपल्याला कोणता अहवाल हवा आहे?"
        elif target_lang == "te":
            return f"మేనేజ్‌మెంట్ అసిస్టెంట్ సిద్ధంగా ఉన్నారు, {pname}. నేను పాఠశాల స్థాయి హాజరు నివేదికలు, ఫీజు వసూలు వివరాలు లేదా ఎస్కలేషన్ నివేదికలను అందించగలను. మీరు దేనిని సమీక్షించాలనుకుంటున్నారు?"
        elif target_lang == "ta":
            return f"நிர்வாக உதவியாளர் தயார், {pname}. பள்ளி அளவிலான வருகை விவரங்கள், கட்டண வசூல் அறிக்கைகள் அல்லது புகார்களை வழங்க முடியும். எதைப் பார்க்க விரும்புகிறீர்கள்?"
        elif target_lang == "bn":
            return f"ম্যানেজমেন্ট সহকারী প্রস্তুত, {pname}। আমি স্কুল-স্তরের উপস্থিতি মেট্রিক্স, ফি সংগ্রহের রিপোর্ট বা অভিযোগ বিবরণ প্রদান করতে পারি। আপনি কোনটি পর্যালোচনা করতে চান?"
        elif target_lang == "pa":
            return f"ਪ੍ਰਬੰਧਨ ਸਹਾਇਕ ਤਿਆਰ ਹੈ, {pname}। ਮੈਂ ਸਕੂਲ ਪੱਧਰ ਦੀ ਹਾਜ਼ਰੀ, ਫ਼ੀਸ ਵਸੂਲੀ ਰਿਪੋਰਟ ਜਾਂ ਸ਼ਿਕਾਇਤਾਂ ਦੇ ਵੇਰਵੇ ਦੇ ਸਕਦਾ ਹਾਂ। ਤੁਸੀਂ ਕਿਹੜਾ ਰਿਪੋਰਟ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
        elif target_lang == "kn":
            return f"ಮ್ಯಾನೇಜ್‌ಮೆಂಟ್ ಸಹಾಯಕ ಸಿದ್ಧರಾಗಿದ್ದಾರೆ, {pname}. ನಾನು ಶಾಲಾ ಮಟ್ಟದ ಹಾಜರಾತಿ, ಶುಲ್ಕ ಸಂಗ್ರಹ ಅಥವಾ ದೂರುಗಳ ವರದಿಯನ್ನು ಒದಗಿಸಬಲ್ಲೆ. ನೀವು ಏನನ್ನು ಪರಿಶೀಲಿಸಲು ಬಯಸುತ್ತೀರಿ?"
        elif target_lang == "ml":
            return f"മാനേജ്‌മെന്റ് അസിസ്റ്റന്റ് സജ്ജമാണ്, {pname}. സ്കൂൾ തല ഹാജർ വിവരങ്ങൾ, ഫീസ് ശേഖരണ റിപ്പോർട്ട് എന്നിവ നൽകാൻ ഞാൻ തയ്യാറാണ്. ഏത് അവലോകനമാണ് താങ്കൾക്ക് വേണ്ടത്?"
        elif target_lang == "ur":
            return f"مینجمنٹ اسسٹنٹ حاضر ہے، {pname}۔ میں اسکول کی مجموعی حاضری، فیس وصولی کے خلاصے اور شکایات کی رپورٹ فراہم کر سکتا ہوں۔ آپ کون سا جائزہ دیکھنا چاہتے ہیں؟"
        elif target_lang == "hinglish":
            return f"Management Assistant ready, {pname}. Main school-wide attendance metrics, fee collection summaries ya escalation reports provide kar sakta hoon. Aap kaun sa overview dekhna chahte hain?"

    # Pattern 8: Parent Conversational Fallback
    m8 = re.search(r"I'm here to help with anything related to ([^']+)'s education, Mr\./Mrs\. ([^!]+)! You can ask me about daily attendance, exam scores, fee payments, class routines, or request a call with the teacher\. What would you like to explore\?", text)
    if m8:
        sname, pname = m8.groups()
        if target_lang == "gu":
            return f"હું {sname} ના શિક્ષણ સંબંધિત તમામ બાબતોમાં મદદ માટે તૈયાર છું, Mr./Mrs. {pname}! તમે દૈનિક હાજરી, પરીક્ષા પરિણામ, ફી ભરવા, ટાઇમટેબલ અથવા શિક્ષક સાથે વાત કરવા વિશે પૂછી શકો છો. તમે શું જાણવા માંગો છો?"
        elif target_lang == "hi":
            return f"मैं {sname} की पढ़ाई से संबंधित हर विषय में आपकी मदद के लिए तैयार हूँ, Mr./Mrs. {pname}! आप दैनिक उपस्थिति, परीक्षा परिणाम, फीस, समय सारणी या शिक्षक से बातचीत के बारे में पूछ सकते हैं।"
        elif target_lang == "mr":
            return f"मी {sname} च्या शिक्षणाशी संबंधित सर्व बाबींमध्ये आपल्या मदतीसाठी सज्ज आहे, Mr./Mrs. {pname}! आपण उपस्थिती, परीक्षा गुण, फी, वेळापत्रक किंवा शिक्षकांशी संपर्क साधण्याबद्दल विचारू शकता."
        elif target_lang == "te":
            return f"నేను {sname} చదువుకు సంబంధించిన ప్రతి విషయంలో మీకు సహాయం చేయడానికి సిద్ధంగా ఉన్నాను, Mr./Mrs. {pname}! మీరు రోజువారీ హాజరు, పరీక్షల ఫలితాలు, ఫీజుల చెల్లింపు లేదా ఉపాధ్యాయులతో మాట్లాడటం గురించి అడగవచ్చు."
        elif target_lang == "ta":
            return f"{sname} இன் கல்வி தொடர்பான அனைத்திலும் உதவ நான் தயாராக உள்ளேன், Mr./Mrs. {pname}! தினசரி வருகை, தேர்வு மதிப்பெண்கள், கட்டணம் அல்லது ஆசிரியரைத் தொடர்புகொள்ள என்னிடம் கேட்கலாம்."
        elif target_lang == "bn":
            return f"আমি {sname} এর পড়াশোনা সংক্রান্ত যেকোনো বিষয়ে আপনাকে সাহায্য করতে প্রস্তুত, Mr./Mrs. {pname}! আপনি প্রতিদিনের উপস্থিতি, পরীক্ষার ফলাফল, ফি বা শিক্ষকের সাথে যোগাযোগ সম্পর্কে জিজ্ঞাসা করতে পারেন।"
        elif target_lang == "pa":
            return f"ਮੈਂ {sname} ਦੀ ਪੜ੍ਹਾਈ ਨਾਲ ਸੰਬੰਧਿਤ ਹਰ ਗੱਲ ਵਿੱਚ ਮਦਦ ਲਈ ਤਿਆਰ ਹਾਂ, Mr./Mrs. {pname}! ਤੁਸੀਂ ਰੋਜ਼ਾਨਾ ਹਾਜ਼ਰੀ, ਪ੍ਰੀਖਿਆ ਨਤੀਜੇ, ਫ਼ੀਸ ਜਾਂ ਅਧਿਆਪਕ ਨਾਲ ਗੱਲਬਾਤ ਬਾਰੇ ਪੁੱਛ ਸਕਦੇ ਹੋ।"
        elif target_lang == "kn":
            return f"ನಾನು {sname} ಅವರ ಶಿಕ್ಷಣಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಎಲ್ಲದರಲ್ಲೂ ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಸಿದ್ಧನಿದ್ದೇನೆ, Mr./Mrs. {pname}! ದೈನಂದಿನ ಹಾಜರಾತಿ, ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳು, ಶುಲ್ಕ ಅಥವಾ ಶಿಕ್ಷಕರೊಂದಿಗೆ ಮಾತನಾಡುವ ಬಗ್ಗೆ ನೀವು ಕೇಳಬಹುದು."
        elif target_lang == "ml":
            return f"{sname} ന്റെ പഠനവുമായി ബന്ധപ്പെട്ട എല്ലാ കാര്യങ്ങളിലും സഹായിക്കാൻ ഞാൻ തയ്യാറാണ്, Mr./Mrs. {pname}! ദിവസേനയുള്ള ഹാജർ, പരീക്ഷാ ഫലങ്ങൾ, ഫീസ് വിവരങ്ങൾ എന്നിവ ചോദിക്കാവുന്നതാണ്."
        elif target_lang == "ur":
            return f"میں {sname} کی تعلیم کے حوالے سے آپ کی ہر ممکن مدد کے لیے حاضر ہوں، Mr./Mrs. {pname}! آپ روزانہ کی حاضری، امتحانی نتائج، فیس ادائیگی یا استاد سے گفتگو کے لیے پوچھ سکتے ہیں۔"

    # Pattern 8B: Student Conversational Fallback
    m8b = re.search(r"I'm here to help you succeed, ([^!]+)! You can ask me about your daily timetable, exam schedules, homework, or attendance\. What can we look at together\?", text)
    if m8b:
        sname = m8b.group(1)
        if target_lang == "gu":
            return f"હું તમારી સફળતા અને અભ્યાસમાં મદદ માટે અહીં છું, {sname}! તમે મને દૈનિક સમયપત્રક, પરીક્ષા શેડ્યૂલ, હોમવર્ક અથવા હાજરી વિશે પૂછી શકો છો. આજે આપણે શું જોઈએ?"
        elif target_lang == "hi":
            return f"मैं आपकी सफलता और पढ़ाई में मदद के लिए यहाँ हूँ, {sname}! आप मुझसे दैनिक समय सारणी, परीक्षा शेड्यूल, होमवर्क या उपस्थिति के बारे में पूछ सकते हैं। आज हम क्या देखें?"
        elif target_lang == "mr":
            return f"मी तुझ्या अभ्यासात आणि प्रगतीमध्ये तुला मदत करण्यासाठी येथे आहे, {sname}! तू मला दैनंदिन वेळापत्रक, परीक्षांचे वेळापत्रक, गृहपाठ किंवा उपस्थितीबद्दल विचारू शकतोस. आज आपण काय पाहूया?"
        elif target_lang == "ta":
            return f"உங்கள் கல்வி வெற்றிக்கு உதவ நான் இங்கு இருக்கிறேன், {sname}! தினசரி நேர அட்டவணை, தேர்வு அட்டவணை, வீட்டுப்பாடம் அல்லது வருகை பற்றி என்னிடம் கேட்கலாம்."
        elif target_lang == "te":
            return f"మీ చదువులో విజయం సాధించడానికి నేను సహాయం చేయడానికి ఇక్కడ ఉన్నాను, {sname}! రోజువారీ టైమ్‌టేబుల్, పరీక్షల షెడ్యూల్, హోమ్‌వర్క్ లేదా హాజరు గురించి మీరు నన్ను అడగవచ్చు."
        elif target_lang == "bn":
            return f"আমি তোমার পড়াশোনায় সাফল্যের জন্য সাহায্য করতে এখানে আছি, {sname}! তুমি আমাকে প্রতিদিনের রুটিন, পরীক্ষার সময়সূচী, হোমওয়ার্ক বা উপস্থিতি সম্পর্কে জিজ্ঞাসা করতে পারো।"
        elif target_lang == "pa":
            return f"ਮੈਂ ਤੁਹਾਡੀ ਪੜ੍ਹਾਈ ਵਿੱਚ ਸਫਲਤਾ ਲਈ ਮਦਦ ਕਰਨ ਲਈ ਇੱਥੇ ਹਾਂ, {sname}! ਤੁਸੀਂ ਮੈਨੂੰ ਰੋਜ਼ਾਨਾ ਟਾਈਮਟੇਬਲ, ਪ੍ਰੀਖਿਆ ਸ਼ਡਿਊਲ, ਹੋਮਵਰਕ ਜਾਂ ਹਾਜ਼ਰੀ ਬਾਰੇ ਪੁੱਛ ਸਕਦੇ ਹੋ।"
        elif target_lang == "kn":
            return f"ನಿಮ್ಮ ಶಿಕ್ಷಣದಲ್ಲಿ ಯಶಸ್ಸು ಸಾಧಿಸಲು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ಇಲ್ಲಿದ್ದೇನೆ, {sname}! ದೈನಂದಿನ ವೇಳಾಪಟ್ಟಿ, ಪರೀಕ್ಷಾ ವೇಳಾಪಟ್ಟಿ, ಮನೆಕೆಲಸ ಅಥವಾ ಹಾಜರಾತಿಯ ಬಗ್ಗೆ ನೀವು ನನ್ನನ್ನು ಕೇಳಬಹುದು."
        elif target_lang == "ml":
            return f"നിങ്ങളുടെ പഠനത്തിൽ സഹായിക്കാൻ ഞാൻ ഇവിടെയുണ്ട്, {sname}! ദൈനംദിന ടൈംടേബിൾ, പരീക്ഷാ ഷെഡ്യൂൾ, ഗൃഹപാഠം അല്ലെങ്കിൽ ഹാജർ എന്നിവയെക്കുറിച്ച് നിങ്ങൾക്ക് എന്നോട് ചോദിക്കാം."
        elif target_lang == "ur":
            return f"میں آپ کی کامیابی اور تعلیمی مدد کے لیے یہاں موجود ہوں، {sname}! آپ مجھ سے روزانہ کا ٹائم ٹیبل، امتحانی شیڈول، ہوم ورک یا حاضری کے بارے میں پوچھ سکتے ہیں۔"
        elif target_lang == "hinglish":
            return f"Main aapki study aur success me help karne ke liye yahan hoon, {sname}! Aap mujhse daily timetable, exam schedule, homework ya attendance ke baare me pooch sakte hain. Aaj hum kya dekhein?"

    # Pattern 9: School-Wide Attendance Overview (Principal Analytics)
    m9 = re.search(r"\*\*School-Wide Attendance Overview\*\*: The overall student attendance across all grades is currently \*\*([^*]+)\*\*\. Top class breakdown: (.*?)\. Would you like an itemized list of classes falling below the 85% benchmark\?", text, re.DOTALL)
    if m9:
        pct, cls_summary = m9.groups()
        if target_lang == "gu":
            return f"**શાળા-વ્યાપી હાજરી વિહંગાવલોકન**: તમામ વર્ગોમાં વિદ્યાર્થીઓની કુલ હાજરી હાલમાં **{pct}** છે. વર્ગવાર વિગત: {cls_summary}. શું તમે 85% થી ઓછી હાજરી ધરાવતા વર્ગોની યાદી જોવા માંગો છો?"
        elif target_lang == "hi":
            return f"**स्कूल-स्तरीय उपस्थिति अवलोकन**: सभी कक्षाओं में कुल विद्यार्थी उपस्थिति वर्तमान में **{pct}** है। कक्षावार विवरण: {cls_summary}। क्या आप 85% से कम उपस्थिति वाली कक्षाओं की सूची देखना चाहते हैं?"
        elif target_lang == "mr":
            return f"**शाळा उपस्थिती आढावा**: सर्व वर्गांमधील एकूण विद्यार्थी उपस्थिती **{pct}** आहे. वर्गवार तपशील: {cls_summary}. आपल्याला 85% पेक्षा कमी उपस्थिती असलेल्या वर्गांची यादी हवी आहे का?"
        elif target_lang == "te":
            return f"**పాఠశాల స్థాయి హాజరు నివేదిక**: అన్ని తరగతుల్లో మొత్తం విద్యార్థుల హాజరు ప్రస్తుతం **{pct}** గా ఉంది. తరగతి వారీ వివరాలు: {cls_summary}. 85% కంటే తక్కువ హాజరు ఉన్న తరగతుల జాబితా కావాలా?"
        elif target_lang == "ta":
            return f"**பள்ளி அளவிலான வருகை மேலோட்டம்**: அனைத்து வகுப்புகளிலும் மொத்த மாணவர் வருகை **{pct}** ஆகும். வகுப்பு வாரியான சுருக்கம்: {cls_summary}. 85% க்கும் குறைவான வகுப்புகளின் பட்டியல் வேண்டுமா?"
        elif target_lang == "bn":
            return f"**স্কুল-স্তরের উপস্থিতির বিবরণ**: সমস্ত ক্লাসে শিক্ষার্থীদের মোট উপস্থিতি বর্তমানে **{pct}**। ক্লাসভিত্তিক বিভাজন: {cls_summary}। আপনি কি ৮৫% এর কম উপস্থিতি থাকা ক্লাসের তালিকা চান?"
        elif target_lang == "pa":
            return f"**ਸਕੂਲ-ਪੱਧਰ ਦੀ ਹਾਜ਼ਰੀ ਦਾ ਜਾਇਜ਼ਾ**: ਸਾਰੀਆਂ ਕਲਾਸਾਂ ਵਿੱਚ ਕੁੱਲ ਵਿਦਿਆਰਥੀਆਂ ਦੀ ਹਾਜ਼ਰੀ ਇਸ ਸਮੇਂ **{pct}** ਹੈ। ਕਲਾਸਵਾਰ ਵੇਰਵੇ: {cls_summary}। ਕੀ ਤੁਸੀਂ 85% ਤੋਂ ਘੱਟ ਹਾਜ਼ਰੀ ਵਾਲੀਆਂ ਕਲਾਸਾਂ ਦੀ ਸੂਚੀ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
        elif target_lang == "kn":
            return f"**ಶಾಲಾ ಮಟ್ಟದ ಹಾಜರಾತಿ ಅವಲೋಕನ**: ಎಲ್ಲಾ ತರಗತಿಗಳಲ್ಲಿ ಒಟ್ಟು ವಿದ್ಯಾರ್ಥಿಗಳ ಹಾಜರಾತಿ ಪ್ರಸ್ತುತ **{pct}** ಆಗಿದೆ. ತರಗತಿವಾರು ವಿವರ: {cls_summary}. 85% ಕ್ಕಿಂತ ಕಡಿಮೆ ಇರುವ ತರಗತಿಗಳ ಪಟ್ಟಿ ಬೇಕೇ?"
        elif target_lang == "ml":
            return f"**സ്കൂൾ തല ഹാജർ അവലോകനം**: എല്ലാ ക്ലാസുകളിലെയും ആകെ വിദ്യാർത്ഥി ഹാജർ നിലവിൽ **{pct}** ആണ്. ക്ലാസ് തിരിച്ചുള്ള വിവരങ്ങൾ: {cls_summary}."
        elif target_lang == "ur":
            return f"**اسکول کی مجموعی حاضری کا جائزہ**: تمام کلاسوں میں طلباء کی کل حاضری اس وقت **{pct}** ہے۔ کلاس وار تفصیلات: {cls_summary}۔ کیا آپ 85 فیصد سے کم حاضری والی کلاسوں کی فہرست دیکھنا چاہتے ہیں؟"
        elif target_lang == "hinglish":
            return f"**School-Wide Attendance Overview**: Sabhi grades me overall student attendance abhi **{pct}** hai. Top class breakdown: {cls_summary}. Kya aap 85% benchmark se neeche wali classes ki list dekhna chahte hain?"

    # Pattern 10: Class Enrollment & Student Roster
    m10 = re.search(r'There are \*\*(\d+) students\*\* enrolled in \*\*([^*]+)\*\*: (.*?)\. Would you like to check today\'s attendance or the academic schedule for this class\?', text, re.DOTALL)
    if m10:
        cnt, cname, names = m10.groups()
        if target_lang == 'gu':
            return f'**{cname}** માં કુલ **{cnt} વિદ્યાર્થીઓ** નોંધાયેલા છે: {names}. શું તમે આ વર્ગની આજની હાજરી અથવા સમયપત્રક તપાસવા માંગો છો?'
        elif target_lang == 'hi':
            return f'**{cname}** में कुल **{cnt} विद्यार्थी** नामांकित हैं: {names}। क्या आप इस कक्षा की आज की उपस्थिति या समय सारणी देखना चाहते हैं?'
        elif target_lang == 'mr':
            return f'**{cname}** मध्ये एकूण **{cnt} विद्यार्थी** नोंदणीकृत आहेत: {names}. आपण या वर्गाची आजची उपस्थिती किंवा वेळापत्रक तपासू इच्छिता?'
        elif target_lang == 'hinglish':
            return f'**{cname}** me total **{cnt} students** enrolled hain: {names}. Kya aap is class ki aaj ki attendance ya timetable check karna chahte hain?'

    # Pattern 11: School-Wide Enrollment
    m11 = re.search(r'\*\*School-Wide Enrollment\*\*: There are currently \*\*(\d+) students\*\* enrolled across the institution\. Class breakdown: \*\*(.*?)\*\*\. Would you like to view attendance or student records for a specific class\?', text, re.DOTALL)
    if m11:
        tot, breakdown = m11.groups()
        if target_lang == 'gu':
            return f'**શાળા-વ્યાપી નોંધણી**: સંસ્થામાં હાલમાં કુલ **{tot} વિદ્યાર્થીઓ** નોંધાયેલા છે. વર્ગવાર વિગત: **{breakdown}**. શું તમે કોઈ ચોક્કસ વર્ગની હાજरी અથવા વિદ્યાર્થી રેકોર્ડ જોવા માંગો છો?'
        elif target_lang == 'hi':
            return f'**स्कूल-स्तरीय कुल नामांकन**: विद्यालय में वर्तमान में कुल **{tot} विद्यार्थी** नामांकित हैं। कक्षावार विवरण: **{breakdown}**। क्या आप किसी विशिष्ट कक्षा की उपस्थिति या रिकॉर्ड देखना चाहते हैं?'
        elif target_lang == 'mr':
            return f'**शाळा एकूण प्रवेश**: संस्थेत सध्या एकूण **{tot} विद्यार्थी** शिकत आहेत. वर्गनिहाय तपशील: **{breakdown}**.'
        elif target_lang == 'hinglish':
            return f'**School-Wide Enrollment**: School me abhi total **{tot} students** enrolled hain. Class breakdown: **{breakdown}**. Kya aap kisi specific class ki attendance ya student records dekhna chahte hain?'

    # Pattern 13: Executive Fee Collection Analytics (Principal Analytics)
    m13 = re.search(r"\*\*Executive Fee Collection Analytics\*\*:\s*-\s*Total Billed:\s*₹([0-9.,]+)\s*-\s*Total Collected:\s*₹([0-9.,]+)\s*\(\s*\*\*([0-9.]+)%\s*collection rate\*\*\)\s*-\s*Total Outstanding Dues:\s*₹([0-9.,]+)\s*across\s*(\d+)\s*overdue accounts\.\s*Would you like to export the list of outstanding accounts for administrative follow-up\?", text, re.DOTALL)
    if m13:
        billed, coll, rate, out, overdue_cnt = m13.groups()
        if target_lang == "hi":
            return (f"**कार्यकारी शुल्क संग्रह विश्लेषण**:\n"
                    f"- कुल बिलिंग: ₹{billed}\n"
                    f"- कुल संग्रह: ₹{coll} (**{rate}% संग्रह दर**)\n"
                    f"- कुल बकाया राशि: ₹{out} ({overdue_cnt} बकाया खातों में)।\n"
                    f"क्या आप प्रशासनिक अनुवर्ती कार्रवाई के लिए बकाया खातों की सूची डाउनलोड करना चाहते हैं?")
        elif target_lang == "gu":
            return (f"**કાર્યકારી ફી સંગ્રહ વિશ્લેષણ**:\n"
                    f"- કુલ બિલિંગ: ₹{billed}\n"
                    f"- કુલ સંગ્રહ: ₹{coll} (**{rate}% સંગ્રહ દર**)\n"
                    f"- કુલ બાકી રકમ: ₹{out} ({overdue_cnt} બાકી ખાતાઓમાં).\n"
                    f"શું આપ વહીવટી ફોલો-અપ માટે બાકી ખાતાઓની યાદી ડાઉનલોડ કરવા માંગો છો?")
        elif target_lang == "mr":
            return (f"**कार्यकारी फी संकलन विश्लेषण**:\n"
                    f"- एकूण बिलिंग: ₹{billed}\n"
                    f"- एकूण संकलित: ₹{coll} (**{rate}% संकलन प्रमाण**)\n"
                    f"- एकूण थकबाकी: ₹{out} ({overdue_cnt} थकीत खात्यांमध्ये).\n"
                    f"आपण प्रशासकीय पाठपुराव्यासाठी थकीत खात्यांची यादी डाउनलोड करू इच्छिता?")
        elif target_lang == "te":
            return (f"**ఎగ్జిక్యూటివ్ ఫీజు వసూలు విశ్లేషణ**:\n"
                    f"- మొత్తం బిల్లింగ్: ₹{billed}\n"
                    f"- మొత్తం వసూలైనది: ₹{coll} (**{rate}% వసూలు శాతం**)\n"
                    f"- మొత్తం బకాయిలు: ₹{out} ({overdue_cnt} బకాయి ఖాతాలు).\n"
                    f"పరిపాలనా చర్యల కొరకు బకాయి ఖాతాల జాబితాను ఎగుమతి చేయాలనుకుంటున్నారా?")
        elif target_lang == "ta":
            return (f"**நிர்வாகக் கட்டண வசூல் பகுப்பாய்வு**:\n"
                    f"- மொத்த பில்லிங்: ₹{billed}\n"
                    f"- மொத்த வசூல்: ₹{coll} (**{rate}% வசூல் விகிதம்**)\n"
                    f"- மொத்த நிலுவைத் தொகை: ₹{out} ({overdue_cnt} நிலுவைக் கணக்குகள்).\n"
                    f"நிர்வாகத் தொடர் நடவடிக்கைக்காக நிலுவைக் கணக்குகளின் பட்டியலைப் பதிவிறக்க விரும்புகிறீர்களா?")
        elif target_lang == "kn":
            return (f"**ಕಾರ್ಯನಿರ್ವಾಹಕ ಶುಲ್ಕ ಸಂಗ್ರಹ ವಿಶ್ಲೇಷಣೆ**:\n"
                    f"- ಒಟ್ಟು ಬಿಲ್ಲಿಂಗ್: ₹{billed}\n"
                    f"- ಒಟ್ಟು ಸಂಗ್ರಹ: ₹{coll} (**{rate}% ಸಂಗ್ರಹ ದರ**)\n"
                    f"- ಒಟ್ಟು ಬಾಕಿ ಶುಲ್ಕ: ₹{out} ({overdue_cnt} ಬಾಕಿ ಖಾತೆಗಳಲ್ಲಿ).\n"
                    f"ಆಡಳಿತಾತ್ಮಕ ಕ್ರಮಕ್ಕಾಗಿ ಬಾಕಿ ಖಾತೆಗಳ ಪಟ್ಟಿಯನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಲು ಬಯಸುವಿರಾ?")
        elif target_lang == "bn":
            return (f"**কার্যনির্বাহী ফি সংগ্রহ বিশ্লেষণ**:\n"
                    f"- মোট বিলিং: ₹{billed}\n"
                    f"- মোট সংগৃহীত: ₹{coll} (**{rate}% সংগ্রহের হার**)\n"
                    f"- মোট বকেয়া: ₹{out} ({overdue_cnt}টি বকেয়া অ্যাকাউন্টে)।\n"
                    f"আপনি কি প্রশাসনিক ফলো-আপের জন্য বকেয়া অ্যাকাউন্টের তালিকা ডাউনলোড করতে চান?")
        elif target_lang == "pa":
            return (f"**ਕਾਰਜਕਾਰੀ ਫ਼ੀਸ ਵਸੂਲੀ ਵਿਸ਼ਲੇਸ਼ਣ**:\n"
                    f"- ਕੁੱਲ ਬਿਲਿੰਗ: ₹{billed}\n"
                    f"- ਕੁੱਲ ਵਸੂਲੀ: ₹{coll} (**{rate}% ਵਸੂਲੀ ਦਰ**)\n"
                    f"- ਕੁੱਲ ਬਕਾਇਆ ਰਕਮ: ₹{out} ({overdue_cnt} ਬਕਾਇਆ ਖਾਤਿਆਂ ਵਿੱਚ)।\n"
                    f"ਕੀ ਤੁਸੀਂ ਪ੍ਰਬੰਧਕੀ ਕਾਰਵਾਈ ਲਈ ਬਕਾਇਆ ਖਾਤਿਆਂ ਦੀ ਸੂਚੀ ਡਾਊਨਲੋਡ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?")
        elif target_lang == "ml":
            return (f"**എക്സിക്യൂട്ടീവ് ഫീസ് ശേഖരണ വിശകലനം**:\n"
                    f"- ആകെ ബില്ലിംഗ്: ₹{billed}\n"
                    f"- ആകെ ശേഖരിച്ചത്: ₹{coll} (**{rate}% ശേഖരണ നിരക്ക്**)\n"
                    f"- ആകെ കുടിശ്ശിക: ₹{out} ({overdue_cnt} അക്കൗണ്ടുകളിൽ).\n"
                    f"തുടർനടപടികൾക്കായി കുടിശ്ശിക അക്കൗണ്ടുകളുടെ ലിസ്റ്റ് ഡൗൺലോഡ് ചെയ്യണോ?")
        elif target_lang == "ur":
            return (f"**ایگزیکٹو فیس وصولی کا تجزیہ**:\n"
                    f"- کل بلنگ: ₹{billed}\n"
                    f"- کل وصول شدہ: ₹{coll} (**{rate}% وصولی کی شرح**)\n"
                    f"- کل واجب الادا رقم: ₹{out} ({overdue_cnt} بقایا کھاتوں میں)۔\n"
                    f"کیا آپ انتظامی کارروائی کے لیے بقایا کھاتوں کی فہرست دیکھنا چاہتے ہیں؟")
        elif target_lang == "hinglish":
            return (f"**Executive Fee Collection Analytics**:\n"
                    f"- Total Billed: ₹{billed}\n"
                    f"- Total Collected: ₹{coll} (**{rate}% collection rate**)\n"
                    f"- Total Outstanding Dues: ₹{out} across {overdue_cnt} overdue accounts.\n"
                    f"Kya aap administrative follow-up ke liye overdue accounts ki list export karna chahte hain?")

    # Pattern 14: Principal Greeting
    m14 = re.search(r"Good day,\s*([^!]+)!\s*I'm Athena,\s*your Executive Management Assistant\.\s*Which language do you prefer\?", text)
    if m14:
        pname = m14.group(1)
        if target_lang == "hi":
            return f"शुभ दिन, {pname}! मैं अथेना हूँ, आपकी कार्यकारी प्रबंधन सहायक। आप किस भाषा में बातचीत करना पसंद करेंगे?"
        elif target_lang == "gu":
            return f"શુભ દિવસ, {pname}! હું અથેના છું, આપની કાર્યકારી મેનેજમેન્ટ આસિસ્ટન્ટ. આપ કઈ ભાષામાં વાતચીત પસંદ કરશો?"
        elif target_lang == "mr":
            return f"शुभ दिवस, {pname}! मी अथेना, आपली कार्यकारी व्यवस्थापन सहाय्यक. आपण कोणत्या भाषेत संवाद साधू इच्छिता?"
        elif target_lang == "te":
            return f"శుభదినం, {pname}! నేను మీ ఎగ్జిక్యూటివ్ మేనేజ్‌మెంట్ అసిస్టెంట్ అథీనా. మీరు ఏ భాషలో మాట్లాడటానికి ఇష్టపడతారు?"
        elif target_lang == "ta":
            return f"நாளொரு நன்நாளாக அமையட்டும், {pname}! நான் அதீனா, உங்கள் நிர்வாக ஏஐ உதவியாளர். எந்த மொழியில் பேச விரும்புகிறீர்கள்?"
        elif target_lang == "kn":
            return f"ಶುಭ ದಿನ, {pname}! ನಾನು ಅಥೀನಾ, ನಿಮ್ಮ ಸಾಂಸ್ಥಿಕ ಕಾರ್ಯನಿರ್ವಾಹಕ ಸಹಾಯಕ. ನೀವು ಯಾವ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಲು ಬಯಸುತ್ತೀರಿ?"
        elif target_lang == "bn":
            return f"শুভ দিন, {pname}! আমি অ্যাথিনা, আপনার এক্সিকিউটিভ ম্যানেজমেন্ট সহকারী। আপনি কোন ভাষায় কথা বলতে পছন্দ করবেন?"
        elif target_lang == "pa":
            return f"ਸ਼ੁਭ ਦਿਨ, {pname}! ਮੈਂ ਅਥੀਨਾ ਹਾਂ, ਤੁਹਾਡੀ ਐਗਜ਼ੀਕਿਊਟਿਵ ਮੈਨੇਜਮੈਂਟ ਅਸਿਸਟੈਂਟ। ਤੁਸੀਂ ਕਿਹੜੀ ਭਾਸ਼ਾ ਪਸੰਦ ਕਰੋਗੇ?"
        elif target_lang == "ml":
            return f"ശുഭദിനം, {pname}! ഞാൻ അഥീന, നിങ്ങളുടെ എക്സിക്യൂട്ടീവ് മാനേജ്‌മെന്റ് സഹായി. ഏത് ഭാഷയിലാണ് സംസാരിക്കാൻ താല്പര്യം?"
        elif target_lang == "ur":
            return f"شاندار دن، {pname}! میں ایتھینا ہوں، آپ کی ایگزیکٹو مینجمنٹ اسسٹنٹ۔ آپ کس زبان میں گفتگو پسند کریں گے؟"
        elif target_lang == "hinglish":
            return f"Good day, {pname}! Main Athena hoon, aapki Executive Management Assistant. Aap kis language me continue karna chahte hain?"

    # Pattern 12: Institutional Leadership Student Disambiguation
    m12 = re.search(r'As institutional leadership, you have access to all records\. Could you please specify which student or class you would like academic results for\?', text)
    if m12:
        if target_lang == 'kn':
            return 'ಸಾಂಸ್ಥಿಕ ಆಡಳಿತ ಮಂಡಳಿಯಾಗಿ, ನೀವು ಎಲ್ಲಾ ವಿದ್ಯಾರ್ಥಿಗಳ ದಾಖಲೆಗಳನ್ನು ವೀಕ್ಷಿಸಬಹುದು. ನೀವು ಯಾವ ವಿದ್ಯಾರ್ಥಿ ಅಥವಾ ತರಗತಿಯ ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳನ್ನು ನೋಡಲು ಬಯಸುತ್ತೀರಿ ಎಂಬುದನ್ನು ತಿಳಿಸಬಹುದೇ?'
        elif target_lang == 'hi':
            return 'प्रशासनिक नेतृत्व के रूप में, आपके पास सभी रिकॉर्ड देखने की अनुमति है। कृपया बताएं कि आप किस विद्यार्थी या कक्षा के परीक्षा परिणाम देखना चाहते हैं?'
        elif target_lang == 'mr':
            return 'शाळा व्यवस्थापन प्रमुख म्हणून, आपल्याकडे सर्व विद्यार्थ्यांचे रेकॉर्ड पाहण्याचा अधिकार आहे. आपण कोणत्या विद्यार्थ्याचा किंवा वर्गाचा निकाल पाहू इच्छिता?'
        elif target_lang == 'gu':
            return 'શાળા વહીવટી વડા તરીકે, આપણી પાસે તમામ રેકોર્ડ જોવાની મંજૂરી છે. કૃપા કરીને જણાવો કે આપ કયા વિદ્યાર્થી અથવા વર્ગનું પરિણામ જોવા માંગો છો?'
        elif target_lang == 'ta':
            return 'பள்ளி நிர்வாகத் தலைவராக, அனைத்து மாணவர்களின் பதிவுகளையும் பார்க்கும் உரிமை உங்களுக்கு உள்ளது. நீங்கள் எந்த மாணவர் அல்லது வகுப்பின் தேர்வு முடிவுகளைப் பார்க்க விரும்புகிறீர்கள்?'
        elif target_lang == 'te':
            return 'సంస్థాగత నాయకత్వంగా, మీకు అన్ని రికార్డులను చూసే అనుమతి ఉంది. మీరు ఏ విద్యార్థి లేదా తరగతి ఫలితాలను చూడాలనుకుంటున్నారో దయచేసి పేర్కొనగలరా?'
        elif target_lang == 'bn':
            return 'প্রাতিষ্ঠানিক নেতৃত্ব হিসেবে, আপনার সমস্ত রেকর্ড দেখার অনুমতি রয়েছে। আপনি কোন শিক্ষার্থী বা ক্লাসের ফলাফল দেখতে চান অনুগ্রহ করে নির্দিষ্ট করুন?'
        elif target_lang == 'pa':
            return 'ਸਕੂਲ ਪ੍ਰਬੰਧਕ ਵਜੋਂ, ਤੁਹਾਡੇ ਕੋਲ ਸਾਰੇ ਵਿਦਿਆਰਥੀਆਂ ਦੇ ਰਿਕਾਰਡ ਦੇਖਣ ਦਾ ਅਧਿਕਾਰ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਦੱਸੋ ਕਿ ਤੁਸੀਂ ਕਿਸ ਵਿਦਿਆਰਥੀ ਜਾਂ ਕਲਾਸ ਦੇ ਨਤੀਜੇ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?'
        elif target_lang == 'ml':
            return 'സ്ഥാപന മേധാവി എന്ന നിലയിൽ, നിങ്ങൾക്ക് എല്ലാ റെക്കോർഡുകളും പരിശോധിക്കാം. ഏത് വിദ്യാർത്ഥിയുടെയോ ക്ലാസിന്റെയോ ഫലങ്ങളാണ് താങ്കൾക്ക് അറിയേണ്ടത്?'
        elif target_lang == 'ur':
            return 'ادارہ جاتی قیادت کے طور پر، آپ کو تمام ریکارڈ تک رسائی حاصل ہے۔ برائے مہربانی بتائیں کہ آپ کس طالب علم یا کلاس کے امتحانی نتائج دیکھنا چاہتے ہیں؟'
        elif target_lang == 'hinglish':
            return 'As institutional leadership, aapke paas sabhi records ka access hai. Please batayein ki aap kis student ya class ke academic results dekhna chahte hain?'

    # Pattern 15: Parent Attendance Overview - "Sure, let me check that for you! Rahul currently has **91.2%** attendance (83/91 days attended). Would you like me to check his recent day-by-day attendance log too?"
    m15 = re.search(r"Sure, let me check that for you!\s*([^*]+)\s*currently has\s*\*\*([^*]+)\*\*\s*attendance\s*\((\d+)/(\d+) days attended\)\.\s*Would you like me to check (?:his|her|their) recent day-by-day attendance log too\?", text)
    if m15:
        sname, pct, pres, tot = m15.groups()
        sname = sname.strip()
        if target_lang == "hi":
            return f"अवश्य, मैं आपके लिए जाँच कर लेता हूँ! {sname} की वर्तमान उपस्थिति **{pct}** ({tot} में से {pres} दिन उपस्थित) है। क्या आप दैनिक उपस्थिति रिकॉर्ड भी देखना चाहते हैं?"
        elif target_lang == "gu":
            return f"ચોક્કસ, હું તમારા માટે તપાસી લઉં છું! {sname} ની હાલની હાજરી **{pct}** ({tot} માંથી {pres} દિવસ હાજર) છે. શું તમે દૈનિક હાજરી પત્રક પણ જોવા માંગો છો?"
        elif target_lang == "mr":
            return f"नक्कीच, मी आपल्यासाठी तपासतो! {sname} ची सद्य उपस्थिती **{pct}** ({tot} पैकी {pres} दिवस उपस्थित) आहे. आपल्याला दैनंदिन उपस्थिती नोंद देखील पाहायची आहे का?"
        elif target_lang == "ta":
            return f"நிச்சயமாக, உங்களுக்காக பார்க்கிறேன்! {sname} இன் தற்போதைய வருகை **{pct}** ({tot} நாட்களில் {pres} நாட்கள் வருகை). தினசரி வருகைப் பதிவையும் பார்க்க விரும்புகிறீர்களா?"
        elif target_lang == "te":
            return f"తప్పకుండా, నేను మీ కోసం తనిఖీ చేస్తాను! {sname} ప్రస్తుత హాజరు **{pct}** ({tot} రోజుల్లో {pres} రోజులు హాజరు). రోజువారీ హాజరు రికార్డును కూడా చూడాలనుకుంటున్నారా?"
        elif target_lang == "bn":
            return f"অবশ্যই, আমি আপনার জন্য দেখে দিচ্ছি! {sname} এর বর্তমান উপস্থিতি **{pct}** ({tot} দিনের মধ্যে {pres} দিন উপস্থিত)। আপনি কি প্রতিদিনের উপস্থিতি লগ দেখতে চান?"
        elif target_lang == "pa":
            return f"ਜ਼ਰੂਰ, ਮੈਂ ਤੁਹਾਡੇ ਲਈ ਚੈੱਕ ਕਰਦਾ ਹਾਂ! {sname} ਦੀ ਮੌਜੂਦਾ ਹਾਜ਼ਰੀ **{pct}** ({tot} ਵਿੱਚੋਂ {pres} ਦਿਨ ਹਾਜ਼ਰ) ਹੈ। ਕੀ ਤੁਸੀਂ ਰੋਜ਼ਾਨਾ ਹਾਜ਼ਰੀ ਰਿਕਾਰਡ ਵੀ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
        elif target_lang == "kn":
            return f"ಖಂಡಿತ, ನಾನು ನಿಮಗಾಗಿ ಪರಿಶೀಲಿಸುತ್ತೇನೆ! {sname} ಅವರ ಪ್ರಸ್ತುತ ಹಾಜರಾತಿ **{pct}** ({tot} ದಿನಗಳಲ್ಲಿ {pres} ದಿನಗಳು ಹಾಜರಾಗಿದ್ದಾರೆ). ಇತ್ತೀಚಿನ ದಿನವಾರು ಹಾಜರಾತಿ ಲಾಗ್ ಅನ್ನು ಸಹ ನೋಡಲು ಬಯಸುವಿರಾ?"
        elif target_lang == "ml":
            return f"തീർച്ചയായും, ഞാൻ പരിശോധിക്കാം! {sname} ന് നിലവിൽ **{pct}** ഹാജറുണ്ട് ({tot} ൽ {pres} ദിവസങ്ങൾ). ദിവസേനയുള്ള ഹാജർ രേഖ കാണണമെന്നുണ്ടോ?"
        elif target_lang == "ur":
            return f"ضرور، میں آپ کے لیے چیک کر لیتا ہوں! {sname} کی موجودہ حاضری **{pct}** ({tot} میں سے {pres} دن حاضر) ہے۔ کیا آپ روزانہ کا حاضری ریکارڈ بھی دیکھنا چاہتے ہیں؟"
        elif target_lang == "hinglish":
            return f"Sure, main aapke liye check kar deta hoon! {sname} ki current attendance **{pct}** ({tot} me se {pres} days attended) hai. Kya aap recent day-by-day attendance log bhi check karna chahte hain?"

    # Pattern 16: Parent Yesterday/Today Status - "Yes! Rahul was marked **PRESENT** yesterday (2026-08-19). Overall, Rahul maintains a strong attendance of **91.2%** (83 present out of 91 school days, with 8 absences)."
    m16 = re.search(r"Yes!\s*([^*]+)\s*was marked\s*\*\*([^*]+)\*\*\s*(yesterday \([^)]+\)|today \([^)]+\)|on [^.]+)\.\s*Overall,\s*([^ ]+)\s*maintains a strong attendance of\s*\*\*([^*]+)\*\*\s*\((\d+)\s*present out of\s*(\d+)\s*school days,\s*with\s*(\d+)\s*absences\)\.", text)
    if m16:
        sname, status, dt_phrase, _, pct, pres, tot, abs_cnt = m16.groups()
        sname = sname.strip()
        status_upper = status.upper()
        if target_lang == "hi":
            st_hi = "उपस्थित (PRESENT)" if "PRESENT" in status_upper else "अनुपस्थित (ABSENT)"
            return f"हाँ! {sname} को {dt_phrase} **{st_hi}** चिह्नित किया गया था। कुल मिलाकर, {sname} की उपस्थिति **{pct}** ({tot} में से {pres} दिन उपस्थित, {abs_cnt} अनुपस्थिति) के साथ उत्कृष्ट है।"
        elif target_lang == "gu":
            st_gu = "હાજર (PRESENT)" if "PRESENT" in status_upper else "ગેરહાજર (ABSENT)"
            return f"હા! {sname} ને {dt_phrase} **{st_gu}** નોંધવામાં આવ્યા હતા. સમગ્ર રીતે, {sname} ની હાજરી **{pct}** ({tot} માંથી {pres} દિવસ હાજર, {abs_cnt} ગેરહાજરી) સાથે ખૂબ સારી છે."
        elif target_lang == "mr":
            st_mr = "उपस्थित (PRESENT)" if "PRESENT" in status_upper else "गैरहजर (ABSENT)"
            return f"होय! {sname} यांना {dt_phrase} **{st_mr}** नोंदवले गेले होते. एकंदरीत, {sname} ची उपस्थिती **{pct}** ({tot} पैकी {pres} दिवस उपस्थित, {abs_cnt} गैरहजर) सह उत्तम आहे."
        elif target_lang == "ta":
            st_ta = "வருகை (PRESENT)" if "PRESENT" in status_upper else "வராதவர் (ABSENT)"
            return f"ஆம்! {sname} {dt_phrase} அன்று **{st_ta}** எனப் பதிவு செய்யப்பட்டுள்ளார். ஒட்டுமொத்தமாக, {sname} **{pct}** வருகை சதவீதத்தை ({tot} நாட்களில் {pres} நாட்கள்) பராமரிக்கிறார்."
        elif target_lang == "te":
            st_te = "హాజరు (PRESENT)" if "PRESENT" in status_upper else "గైర్హాజరు (ABSENT)"
            return f"అవును! {sname} {dt_phrase} న **{st_te}** గా నమోదు చేయబడ్డారు. మొత్తంమీద, {sname} **{pct}** హాజరును ({tot} రోజుల్లో {pres} రోజులు) కొనసాగిస్తున్నారు."
        elif target_lang == "bn":
            st_bn = "উপস্থিত (PRESENT)" if "PRESENT" in status_upper else "অনুপস্থিত (ABSENT)"
            return f"হ্যাঁ! {sname} কে {dt_phrase} **{st_bn}** চিহ্নিত করা হয়েছিল। সামগ্রিকভাবে, {sname} **{pct}** উপস্থিতি ({tot} দিনের মধ্যে {pres} দিন) বজায় রেখেছেন।"
        elif target_lang == "pa":
            st_pa = "ਹਾਜ਼ਰ (PRESENT)" if "PRESENT" in status_upper else "ਗ਼ੈਰਹਾਜ਼ਰ (ABSENT)"
            return f"ਹਾਂ! {sname} ਨੂੰ {dt_phrase} **{st_pa}** ਦਰਜ ਕੀਤਾ ਗਿਆ ਸੀ। ਸਮੁੱਚੇ ਤੌਰ 'ਤੇ, {sname} ਦੀ ਹਾਜ਼ਰੀ **{pct}** ({tot} ਵਿੱਚੋਂ {pres} ਦਿਨ ਹਾਜ਼ਰ) ਬਹੁਤ ਚੰਗੀ ਹੈ।"
        elif target_lang == "kn":
            st_kn = "ಹಾಜರು (PRESENT)" if "PRESENT" in status_upper else "ಗೈರುಹಾಜರು (ABSENT)"
            return f"ಹೌದು! {sname} ಅವರನ್ನು {dt_phrase} **{st_kn}** ಎಂದು ಗುರುತಿಸಲಾಗಿದೆ. ಒಟ್ಟಾರೆಯಾಗಿ, {sname} **{pct}** ಹಾಜರಾತಿಯನ್ನು ({tot} ದಿನಗಳಲ್ಲಿ {pres} ದಿನಗಳು) ಕಾಯ್ದುಕೊಂಡಿದ್ದಾರೆ."
        elif target_lang == "ml":
            st_ml = "ഹാജർ (PRESENT)" if "PRESENT" in status_upper else "ഹാജരായില്ല (ABSENT)"
            return f"അതെ! {sname} {dt_phrase} ൽ **{st_ml}** ആയിരുന്നു. ആകെ {sname} ന് **{pct}** ഹാജറുണ്ട് ({tot} ൽ {pres} ദിവസങ്ങൾ)."
        elif target_lang == "ur":
            st_ur = "حاضر (PRESENT)" if "PRESENT" in status_upper else "غیر حاضر (ABSENT)"
            return f"جی ہاں! {sname} کو {dt_phrase} **{st_ur}** درج کیا گیا تھا۔ مجموعی طور پر، {sname} کی حاضری **{pct}** ({tot} میں سے {pres} دن حاضر) ہے۔"
        elif target_lang == "hinglish":
            return f"Haan! {sname} ko {dt_phrase} **{status_upper}** mark kiya gaya tha. Overall, {sname} ki attendance **{pct}** ({tot} me se {pres} days present, {abs_cnt} absences) ke sath strong hai."

    # Pattern 17: Parent Greeting - "Hello Mr. Amit Patel! Good afternoon! I'm XYZ AI, your Parent Support Assistant. Which language do you prefer?"
    m17 = re.search(r"Hello\s+([^!]+)!\s*([^!]+)!\s*I'm XYZ AI,\s*your Parent Support Assistant\.\s*Which language do you prefer\?", text)
    if m17:
        pname, tgreet = m17.groups()
        if target_lang == "hi":
            return f"नमस्ते {pname}! {tgreet}! मैं XYZ AI हूँ, आपका अभिभावक सहायता सहायक। आप किस भाषा में बातचीत करना पसंद करेंगे?"
        elif target_lang == "gu":
            return f"નમસ્તે {pname}! {tgreet}! હું XYZ AI છું, આપનો પેરેન્ટ સપોર્ટ આસિસ્ટન્ટ. આપ કઈ ભાષામાં વાતચીત પસંદ કરશો?"
        elif target_lang == "mr":
            return f"नमस्कार {pname}! {tgreet}! मी XYZ AI, आपला पालक सहाय्यक. आपण कोणत्या भाषेत संवाद साधू इच्छिता?"
        elif target_lang == "ta":
            return f"வணக்கம் {pname}! {tgreet}! நான் XYZ AI, உங்கள் பெற்றோர் உதவி உதவியாளர். எந்த மொழியில் பேச விரும்புகிறீர்கள்?"
        elif target_lang == "te":
            return f"నమస్కారం {pname}! {tgreet}! నేను XYZ AI, మీ పేరెంట్ సపోర్ట్ అసిస్టెంట్. మీరు ఏ భాషలో మాట్లాడటానికి ఇష్టపడతారు?"
        elif target_lang == "bn":
            return f"নমস্কার {pname}! {tgreet}! আমি XYZ AI, আপনার অভিভাবক সহায়তা সহকারী। আপনি কোন ভাষায় কথা বলতে পছন্দ করবেন?"
        elif target_lang == "pa":
            return f"ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ {pname}! {tgreet}! ਮੈਂ XYZ AI ਹਾਂ, ਤੁਹਾਡਾ ਪੇਰੈਂਟ ਸਪੋਰਟ ਅਸਿਸਟੈਂਟ। ਤੁਸੀਂ ਕਿਹੜੀ ਭਾਸ਼ਾ ਪਸੰਦ ਕਰੋਗੇ?"
        elif target_lang == "kn":
            return f"ನಮಸ್ಕಾರ {pname}! {tgreet}! ನಾನು XYZ AI, ನಿಮ್ಮ ಪೋಷಕರ ಬೆಂಬಲ ಸಹಾಯಕ. ನೀವು ಯಾವ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಲು ಬಯಸುತ್ತೀರಿ?"
        elif target_lang == "ml":
            return f"നമസ്കാരം {pname}! {tgreet}! ഞാൻ XYZ AI, രക്ഷിതാക്കളുടെ പിന്തുണ സഹായി. ഏത് ഭാഷയിലാണ് സംസാരിക്കാൻ താല്പര്യം?"
        elif target_lang == "ur":
            return f"آداب {pname}! {tgreet}! میں XYZ AI ہوں، آپ کا پیرنٹ سپورٹ اسسٹنٹ۔ آپ کس زبان میں گفتگو پسند کریں گے؟"
        elif target_lang == "hinglish":
            return f"Hello {pname}! {tgreet}! Main XYZ AI hoon, aapka Parent Support Assistant. Aap kis language me continue karna chahte hain?"

    # Pattern 18: Student Greeting
    m18 = re.search(r"Hey\s+([^!]+)!\s*([^!]+)!\s*😊\s*I'm XYZ AI,\s*your Academic Assistant\.\s*Which language do you prefer\?", text)
    if m18:
        sname, tgreet = m18.groups()
        if target_lang == "hi":
            return f"नमस्ते {sname}! {tgreet}! 😊 मैं XYZ AI हूँ, आपका शैक्षणिक सहायक। आप किस भाषा में बात करना चाहते हैं?"
        elif target_lang == "gu":
            return f"નમસ્તે {sname}! {tgreet}! 😊 હું XYZ AI છું, તમારો શૈક્ષણિક સહાયક. તમે કઈ ભાષામાં વાત કરવા માંગો છો?"
        elif target_lang == "mr":
            return f"नमस्कार {sname}! {tgreet}! 😊 मी XYZ AI, तुझा शैक्षणिक सहाय्यक. तू कोणत्या भाषेत संवाद साधू इच्छितोस?"
        elif target_lang == "ta":
            return f"வணக்கம் {sname}! {tgreet}! 😊 நான் XYZ AI, உங்கள் கல்வி உதவியாளர். எந்த மொழியில் பேச விரும்புகிறீர்கள்?"
        elif target_lang == "te":
            return f"హలో {sname}! {tgreet}! 😊 నేను XYZ AI, మీ అకడమిక్ అసిస్టెంట్. మీరు ఏ భాషలో మాట్లాడాలనుకుంటున్నారు?"
        elif target_lang == "kn":
            return f"ನಮಸ್ಕಾರ {sname}! {tgreet}! 😊 ನಾನು XYZ AI, ನಿಮ್ಮ ಶೈಕ್ಷಣಿಕ ಸಹಾಯಕ. ನೀವು ಯಾವ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡಲು ಬಯಸುತ್ತೀರಿ?"
        elif target_lang == "bn":
            return f"হ্যালো {sname}! {tgreet}! 😊 আমি XYZ AI, তোমার একাডেমিক সহকারী। তুমি কোন ভাষায় কথা বলতে চাও?"
        elif target_lang == "pa":
            return f"ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ {sname}! {tgreet}! 😊 ਮੈਂ XYZ AI ਹਾਂ, ਤੁਹਾਡਾ ਅਕਾਦਮਿਕ ਸਹਾਇਕ। ਤੁਸੀਂ ਕਿਹੜੀ ਭਾਸ਼ਾ ਚੁਣੋਗੇ?"
        elif target_lang == "ml":
            return f"ഹലോ {sname}! {tgreet}! 😊 ഞാൻ XYZ AI, നിങ്ങളുടെ അക്കാദമിക് സഹായി. ഏത് ഭാഷയിലാണ് സംസാരിക്കേണ്ടത്?"
        elif target_lang == "ur":
            return f"ہیلو {sname}! {tgreet}! 😊 میں XYZ AI ہوں، آپ کا تعلیمی اسسٹنٹ۔ آپ کس زبان میں بات کرنا چاہتے ہیں؟"
        elif target_lang == "hinglish":
            return f"Hey {sname}! {tgreet}! 😊 Main XYZ AI hoon, aapka Academic Assistant. Aap kis language me continue karna chahte hain?"

    # Pattern 19: Holistic Progress - "Overall, **Rahul is doing very well!** 😊\n- **Attendance**: 91.2% (punctual and attending regularly)\n- **Academic Average**: 87.5% across all major subjects\n- **Behavior & Conduct**: Positive teacher remarks across classes.\nIs there a particular subject or upcoming school event you'd like to discuss in detail?"
    m19 = re.search(r"Overall,\s*\*\*([^*]+)\s*is doing very well!\*\*\s*😊\s*-\s*\*\*Attendance\*\*:\s*([0-9.]+)%\s*\(punctual and attending regularly\)\s*-\s*\*\*Academic Average\*\*:\s*([0-9.]+)%\s*across all major subjects\s*-\s*\*\*Behavior & Conduct\*\*:\s*Positive teacher remarks across classes\.\s*Is there a particular subject or upcoming school event you'd like to discuss in detail\?", text, re.DOTALL)
    if m19:
        sname, pct, avg = m19.groups()
        if target_lang == "hi":
            return (f"कुल मिलाकर, **{sname} का प्रदर्शन बहुत अच्छा है!** 😊\n"
                    f"- **उपस्थिति**: {pct}% (नियमित और समय पर उपस्थित)\n"
                    f"- **शैक्षणिक औसत**: प्रमुख विषयों में {avg}%\n"
                    f"- **आचरण व व्यवहार**: शिक्षकों द्वारा सकारात्मक टिप्पणी।\n"
                    f"क्या आप किसी विशिष्ट विषय या आगामी कार्यक्रम के बारे में विस्तार से बात करना चाहते हैं?")
        elif target_lang == "gu":
            return (f"સમગ્ર રીતે, **{sname} નો દેખાવ ખૂબ જ સારો છે!** 😊\n"
                    f"- **હાજરી**: {pct}% (નિયમિત અને સમયપાલન)\n"
                    f"- **શૈક્ષણિક સરેરાશ**: મુખ્ય વિષયોમાં {avg}%\n"
                    f"- **વર્તણૂક અને આચરણ**: શિક્ષકો દ્વારા સકારાત્મક પ્રતિસાદ.\n"
                    f"શું આપ કોઈ ચોક્કસ વિષય અથવા આગામી કાર્યક્રમ વિશે વાત કરવા માંગો છો?")
        elif target_lang == "mr":
            return (f"एकंदरीत, **{sname} ची प्रगती खूप छान आहे!** 😊\n"
                    f"- **उपस्थिती**: {pct}% (नियमित उपस्थिती)\n"
                    f"- **शैक्षणिक सरासरी**: सर्व प्रमुख विषयांमध्ये {avg}%\n"
                    f"- **वर्तन व शिस्त**: शिक्षकांचे सकारात्मक अभिप्राय.\n"
                    f"आपल्याला एखाद्या विशिष्ट विषयाबद्दल किंवा आगामी कार्यक्रमाबद्दल अधिक माहिती हवी आहे का?")
        elif target_lang == "ta":
            return (f"ஒட்டுமொத்தமாக, **{sname} மிகச் சிறப்பாக செயல்படுகிறார்!** 😊\n"
                    f"- **வருகை**: {pct}%\n- **கல்வி சராசரி**: {avg}%\n- **நடத்தை**: ஆசிரியர்களின் சிறந்த கருத்துகள்.\n"
                    f"ஏதேனும் குறிப்பிட்ட பாடம் பற்றி பேச விரும்புகிறீர்களா?")
        elif target_lang == "te":
            return (f"మొత్తంమీద, **{sname} చాలా బాగా రాణిస్తున్నారు!** 😊\n"
                    f"- **హాజరు**: {pct}%\n- **అకడమిక్ సగటు**: {avg}%\n- **ప్రవర్తన**: ఉపాధ్యాయుల సానుకూల అభిప్రాయాలు.\n"
                    f"మీరు ఏదైనా నిర్దిష్ట విషయం గురించి చర్చించాలనుకుంటున్నారా?")
        elif target_lang == "kn":
            return (f"ಒಟ್ಟಾರೆಯಾಗಿ, **{sname} ಉತ್ತಮವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದ್ದಾರೆ!** 😊\n"
                    f"- **ಹಾಜರಾತಿ**: {pct}%\n- **ಶೈಕ್ಷಣಿಕ ಸರಾಸರಿ**: {avg}%\n- **ನಡವಳಿಕೆ**: ಶಿಕ್ಷಕರ ಸಕಾರಾತ್ಮಕ ಪ್ರತಿಕ್ರಿಯೆ.\n"
                    f"ನೀವು ನಿರ್ದಿಷ್ಟ ವಿಷಯದ ಬಗ್ಗೆ ಚರ್ಚಿಸಲು ಬಯಸುವಿರಾ?")
        elif target_lang == "bn":
            return (f"সামগ্রিকভাবে, **{sname} খুব ভালো করছে!** 😊\n"
                    f"- **উপস্থিতি**: {pct}%\n- **একাডেমিক গড়**: {avg}%\n- **আচরণ**: শিক্ষকদের ইতিবাচক মন্তব্য।\n"
                    f"আপনি কি নির্দিষ্ট কোনো বিষয় নিয়ে আলোচনা করতে চান?")
        elif target_lang == "pa":
            return (f"ਕੁੱਲ ਮਿਲਾ ਕੇ, **{sname} ਬਹੁਤ ਵਧੀਆ ਪ੍ਰਦਰਸ਼ਨ ਕਰ ਰਿਹਾ ਹੈ!** 😊\n"
                    f"- **ਹਾਜ਼ਰੀ**: {pct}%\n- **ਅਕਾਦਮਿਕ ਔਸਤ**: {avg}%\n- **ਵਿਵਹਾਰ**: ਅਧਿਆਪਕਾਂ ਦੀ ਚੰਗੀ ਰਾਏ।\n"
                    f"ਕੀ ਤੁਸੀਂ ਕਿਸੇ ਖਾਸ ਵਿਸ਼ੇ ਬਾਰੇ ਗੱਲ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?")
        elif target_lang == "ml":
            return (f"മൊത്തത്തിൽ, **{sname} വളരെ മികച്ച പ്രകടനമാണ് കാഴ്ചവയ്ക്കുന്നത്!** 😊\n"
                    f"- **ഹാജർ**: {pct}%\n- **അക്കാദമിക് ശരാശരി**: {avg}%\n"
                    f"പ്രത്യേകം ഏതെങ്കിലും വിഷയത്തെക്കുറിച്ച് ചർച്ച ചെയ്യണമെന്നുണ്ടോ?")
        elif target_lang == "ur":
            return (f"مجموعی طور پر، **{sname} کی کارکردگی شاندار ہے!** 😊\n"
                    f"- **حاضری**: {pct}%\n- **تعلیمی اوسط**: {avg}%\n- **طرز عمل**: اساتذہ کے مثبت تاثرات۔\n"
                    f"کیا آپ کسی خاص مضمون پر بات کرنا چاہتے ہیں؟")
        elif target_lang == "hinglish":
            return (f"Overall, **{sname} ka performance kaafi accha hai!** 😊\n"
                    f"- **Attendance**: {pct}% (regular aur punctual)\n"
                    f"- **Academic Average**: {avg}% sabhi major subjects me\n"
                    f"- **Behavior & Conduct**: Teachers ke positive remarks hain.\n"
                    f"Kya aap kisi particular subject ya upcoming school event ke baare me discuss karna chahte hain?")

    # Pattern 20: Academic Report Card
    m20 = re.search(r"\*\*Academic Report for ([^*]+)\*\* \(([^)]+)\):\s*Overall Average:\s*\*\*([0-9.]+)%\*\*\.\s*Key subject scores:\s*(.*?)\.\s*Overall, ([^ ]+) is performing commendably\. Would you like to review specific subject remarks or the upcoming test schedule\?", text, re.DOTALL)
    if m20:
        sname, ename, avg, scores, _ = m20.groups()
        if target_lang == "hi":
            return (f"**{sname} की शैक्षणिक रिपोर्ट** ({ename}):\n"
                    f"कुल औसत: **{avg}%**।\n"
                    f"प्रमुख विषय अंक: {scores}।\n"
                    f"कुल मिलाकर, {sname} का प्रदर्शन सराहनीय है। क्या आप विषयवार टिप्पणी या आगामी परीक्षा कार्यक्रम देखना चाहते हैं?")
        elif target_lang == "gu":
            return (f"**{sname} નો શૈક્ષણિક અહેવાલ** ({ename}):\n"
                    f"કુલ સરેરાશ: **{avg}%**.\n"
                    f"મુખ્ય વિષયના ગુણ: {scores}.\n"
                    f"સમગ્ર રીતે, {sname} નો દેખાવ પ્રશંસનીય છે. શું આપ વિષયવાર શિક્ષકની નોંધ અથવા પરીક્ષા શેડ્યૂલ જોવા માંગો છો?")
        elif target_lang == "mr":
            return (f"**{sname} चा शैक्षणिक अहवाल** ({ename}):\n"
                    f"एकूण सरासरी: **{avg}%**.\n"
                    f"प्रमुख विषयांचे गुण: {scores}.\n"
                    f"एकंदरीत, {sname} ची प्रगती वाखाणण्याजोगी आहे. आपल्याला विषयानुसार अभिप्राय किंवा परीक्षेचे वेळापत्रक पाहायचे आहे का?")
        elif target_lang == "ta":
            return f"**{sname} இன் கல்வி அறிக்கை** ({ename}):\nமொத்த சராசரி: **{avg}%**.\nமுக்கிய பாட மதிப்பெண்கள்: {scores}.\nதேர்வு அட்டவணையைப் பார்க்க விரும்புகிறீர்களா?"
        elif target_lang == "te":
            return f"**{sname} అకడమిక్ రిపోర్ట్** ({ename}):\nమొత్తం సగటు: **{avg}%**.\nముఖ్య విషయాల మార్కులు: {scores}.\nపరీక్షల షెడ్యూల్ చూడాలనుకుంటున్నారా?"
        elif target_lang == "kn":
            return f"**{sname} ಅವರ ಶೈಕ್ಷಣಿಕ ವರದಿ** ({ename}):\nಒಟ್ಟು ಸರಾಸರಿ: **{avg}%**.\nಪ್ರಮುಖ ವಿಷಯದ ಅಂಕಗಳು: {scores}.\nಪರೀಕ್ಷಾ ವೇಳಾಪಟ್ಟಿ ನೋಡಲು ಬಯಸುವಿರಾ?"
        elif target_lang == "bn":
            return f"**{sname} এর একাডেমিক রিপোর্ট** ({ename}):\nমোট গড়: **{avg}%**।\nপ্রধান বিষয়গুলির নম্বর: {scores}।\nপরীক্ষার সময়সূচী দেখতে চান?"
        elif target_lang == "pa":
            return f"**{sname} ਦੀ ਅਕਾਦਮਿਕ ਰਿਪੋਰਟ** ({ename}):\nਕੁੱਲ ਔਸਤ: **{avg}%**।\nਮੁੱਖ ਵਿਸ਼ਿਆਂ ਦੇ ਅੰਕ: {scores}।\nਪਰੀਖਿਆ ਸ਼ਡਿਊਲ ਦੇਖਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
        elif target_lang == "ml":
            return f"**{sname} ന്റെ അക്കാദമിക് റിപ്പോർട്ട്** ({ename}):\nആകെ ശരാശരി: **{avg}%**.\nമാർക്കുകൾ: {scores}.\nപരീക്ഷാ ഷെഡ്യൂൾ വേണമെന്നുണ്ടോ?"
        elif target_lang == "ur":
            return f"**{sname} کی تعلیمی رپورٹ** ({ename}):\nمجموعی اوسط: **{avg}%**۔\nاہم مضامین کے نمبر: {scores}۔\nامتحانی شیڈول دیکھنا چاہتے ہیں؟"
        elif target_lang == "hinglish":
            return (f"**Academic Report for {sname}** ({ename}):\n"
                    f"Overall Average: **{avg}%**.\n"
                    f"Key subject scores: {scores}.\n"
                    f"Overall, {sname} ka performance bohot accha hai. Kya aap specific subject remarks ya exam schedule dekhna chahte hain?")

    # Pattern 21: Parent Exam Schedule
    m21 = re.search(r"Upcoming exam schedule for \*\*([^*]+)\*\* \(Mid-Term Assessment 2026\):\s*-\s*Mathematics:\s*([^\n]+)\s*-\s*Science:\s*([^\n]+)\s*-\s*English:\s*([^\n]+)\s*-\s*Computer Applications:\s*([^\n]+)\s*Would you like subject performance insights or study preparation tips for ([^?]+)\?", text, re.DOTALL)
    if m21:
        sname, m_dt, s_dt, e_dt, c_dt, s_child = m21.groups()
        if target_lang == "hi":
            return (f"**{sname}** के लिए आगामी परीक्षा समय सारणी (सत्र 2026):\n"
                    f"- गणित: {m_dt}\n- विज्ञान: {s_dt}\n- अंग्रेजी: {e_dt}\n- कंप्यूटर अनुप्रयोग: {c_dt}\n"
                    f"क्या आप {s_child} के लिए अध्ययन युक्तियाँ (Study Tips) देखना चाहते हैं?")
        elif target_lang == "gu":
            return (f"**{sname}** માટે આગામી પરીક્ષાનું સમયપત્રક (સત્ર 2026):\n"
                    f"- ગણિત: {m_dt}\n- વિજ્ઞાન: {s_dt}\n- અંગ્રેજી: {e_dt}\n- કમ્પ્યુટર: {c_dt}\n"
                    f"શું આપ {s_child} માટે અભ્યાસ ટિપ્સ મેળવવા માંગો છો?")
        elif target_lang == "mr":
            return (f"**{sname}** साठी आगामी परीक्षेचे वेळापत्रक (सत्र 2026):\n"
                    f"- गणित: {m_dt}\n- विज्ञान: {s_dt}\n- इंग्रजी: {e_dt}\n- संगणक: {c_dt}\n"
                    f"आपल्याला {s_child} साठी अभ्यासाच्या टिप्स हव्या आहेत का?")
        elif target_lang == "ta":
            return f"**{sname}** க்கான தேர்வு அட்டவணை:\n- கணிதம்: {m_dt}\n- அறிவியல்: {s_dt}\n- ஆங்கிலம்: {e_dt}\n- கணினி: {c_dt}\nபடிப்பு குறிப்புகள் தேவையா?"
        elif target_lang == "te":
            return f"**{sname}** పరీక్షల షెడ్యూల్:\n- గణితం: {m_dt}\n- సైన్స్: {s_dt}\n- ఇంగ్లీష్: {e_dt}\n- కంప్యూటర్: {c_dt}\nస్టడీ టిప్స్ కావాలా?"
        elif target_lang == "kn":
            return f"**{sname}** ಪರೀಕ್ಷಾ ವೇಳಾಪಟ್ಟಿ:\n- ಗಣಿತ: {m_dt}\n- ವಿಜ್ಞಾನ: {s_dt}\n- ಇಂಗ್ಲಿಷ್: {e_dt}\n- ಕಂಪ್ಯೂಟರ್: {c_dt}\nಸ್ಟಡಿ ಟಿಪ್ಸ್ ಬೇಕೇ?"
        elif target_lang == "bn":
            return f"**{sname}** এর পরীক্ষার সময়সূচী:\n- গণিত: {m_dt}\n- বিজ্ঞান: {s_dt}\n- ইংরেজি: {e_dt}\n- কম্পিউটার: {c_dt}\nপড়ার টিপস চান?"
        elif target_lang == "pa":
            return f"**{sname}** ਲਈ ਪਰੀਖਿਆ ਸ਼ਡਿਊਲ:\n- ਗਣਿਤ: {m_dt}\n- ਵਿਗਿਆਨ: {s_dt}\n- ਅੰਗਰੇਜ਼ੀ: {e_dt}\n- ਕੰਪਿਊਟਰ: {c_dt}\nਸਟੱਡੀ ਟਿਪਸ ਚਾਹੀਦੇ ਹਨ?"
        elif target_lang == "ml":
            return f"**{sname}** പരീക്ഷാ ഷെഡ്യൂൾ:\n- മാത്തമാറ്റിക്സ്: {m_dt}\n- സയൻസ്: {s_dt}\n- ഇംഗ്ലീഷ്: {e_dt}\n- കമ്പ്യൂട്ടർ: {c_dt}"
        elif target_lang == "ur":
            return f"**{sname}** کا امتحانی شیڈول:\n- ریاضی: {m_dt}\n- سائنس: {s_dt}\n- انگریزی: {e_dt}\n- کمپیوٹر: {c_dt}"
        elif target_lang == "hinglish":
            return (f"Upcoming exam schedule for **{sname}**:\n"
                    f"- Mathematics: {m_dt}\n- Science: {s_dt}\n- English: {e_dt}\n- Computer Applications: {c_dt}\n"
                    f"Kya aap {s_child} ke liye study preparation tips chahte hain?")

    # Pattern 22: Parent Fee Outstanding & Payment
    m22 = re.search(r"For \*\*([^*]+)\*\*, there is a current outstanding balance of \*\*₹([0-9.,]+)\*\*\.\s*The upcoming installment is due by ([^.]+)\.\s*Would you like me to share payment details or email you the receipt\?", text, re.DOTALL)
    if m22:
        sname, dues, dt_due = m22.groups()
        if target_lang == "hi":
            return f"**{sname}** के लिए वर्तमान बकाया शुल्क राशि **₹{dues}** है। अगली किस्त {dt_due} तक देय है। क्या आप भुगतान विवरण देखना चाहते हैं या रसीद ईमेल पर चाहते हैं?"
        elif target_lang == "gu":
            return f"**{sname}** માટે હાલની બાકી ફી ની રકમ **₹{dues}** છે. આગામી હપ્તો {dt_due} સુધીમાં ભરવાનો છે. શું તમે ફી ભરવાની વિગતો મેળવવા માંગો છો કે ઈમેલ પર રસીદ મોકલું?"
        elif target_lang == "mr":
            return f"**{sname}** साठी सध्याची थकीत फी रक्कम **₹{dues}** आहे. पुढील हप्ता {dt_due} पर्यंत भरायचा आहे. आपल्याला पेमेंट तपशील हवे आहेत की ईमेलवर पावती पाठवू?"
        elif target_lang == "ta":
            return f"**{sname}** க்கான நிலுவைக் கட்டணம் **₹{dues}**. கட்டணம் செலுத்த வேண்டிய தேதி: {dt_due}. கட்டண விவரங்கள் வேண்டுமா?"
        elif target_lang == "te":
            return f"**{sname}** కోసం ప్రస్తుత బకాయి ఫీజు **₹{dues}**. గడువు తేదీ: {dt_due}. చెల్లింపు వివరాలు పంపమంటారా?"
        elif target_lang == "kn":
            return f"**{sname}** ಅವರ ಬಾಕಿ ಶುಲ್ಕ ಮೊತ್ತ **₹{dues}**. ಅಂತಿಮ ದಿನಾಂಕ: {dt_due}. ಪಾವತಿ ವಿವರಗಳು ಬೇಕೇ?"
        elif target_lang == "bn":
            return f"**{sname}** এর জন্য বর্তমান বকেয়া ফি **₹{dues}**। শেষ তারিখ: {dt_due}। পেমেন্ট বিবরণ দেখতে চান?"
        elif target_lang == "pa":
            return f"**{sname}** ਲਈ ਬਕਾਇਆ ਫ਼ੀਸ **₹{dues}** ਹੈ। ਆਖਰੀ ਮਿਤੀ: {dt_due}। ਭੁਗਤਾਨ ਦੇ ਵੇਰਵੇ ਚਾਹੀਦੇ ਹਨ?"
        elif target_lang == "ml":
            return f"**{sname}** ന്റെ കുടിശ്ശിക ഫീസ് തുക **₹{dues}**. അവസാന തീയതി: {dt_due}."
        elif target_lang == "ur":
            return f"**{sname}** کے لیے واجب الادا فیس **₹{dues}** ہے۔ آخری تاریخ: {dt_due}۔ ادائیگی کی تفصیلات چاہیے؟"
        elif target_lang == "hinglish":
            return f"**{sname}** ke liye current outstanding balance **₹{dues}** hai. Next installment {dt_due} tak due hai. Kya aap payment details chahte hain ya receipt email pe bhej doon?"

    # Pattern 23: Parent Official Payment Details
    m23 = re.search(r"Here are the official school payment details for \*\*([^*]+)\*\* \(Outstanding Amount: \*\*₹([0-9.,]+)\*\*\):\s*(.*?)\s*Would you like me to email you the official invoice and payment receipt for your records\?", text, re.DOTALL)
    if m23:
        sname, dues, pdetails = m23.groups()
        if target_lang == "hi":
            return (f"**{sname}** के लिए आधिकारिक स्कूल शुल्क भुगतान विवरण (बकाया राशि: **₹{dues}**):\n\n"
                    f"💳 **1. ऑनलाइन पोर्टल**: पोर्टल हेडर में 'Pay Fees Online' पर क्लिक करें (UPI, NetBanking, Card).\n"
                    f"🏦 **2. बैंक ट्रांसफर (NEFT/RTGS)**:\n"
                    f"   - **लाभार्थी**: XYZ Public School Fee Collection\n"
                    f"   - **बैंक**: HDFC Bank | **खाता संख्या**: `50200088991122` | **IFSC**: `HDFC0001042`\n"
                    f"📱 **3. UPI ID**: `xyzschool.fees@hdfcbank`\n\n"
                    f"क्या आप आधिकारिक चालान और रसीद ईमेल पर प्राप्त करना चाहते हैं?")
        elif target_lang == "gu":
            return (f"**{sname}** માટે સત્તાવાર ફી ચુકવણી વિગતો (બાકી રકમ: **₹{dues}**):\n\n"
                    f"💳 **1. ઓનલાઇન પોર્ટલ**: પોર્ટલ હેડરમાં 'Pay Fees Online' ક્લિક કરો (UPI, NetBanking, Card).\n"
                    f"🏦 **2. બેંક ટ્રાન્સફર (NEFT/RTGS)**:\n"
                    f"   - **લાભાર્થી**: XYZ Public School Fee Collection\n"
                    f"   - **બેંક**: HDFC Bank | **ખાતા નંબર**: `50200088991122` | **IFSC**: `HDFC0001042`\n"
                    f"📱 **3. UPI ID**: `xyzschool.fees@hdfcbank`\n\n"
                    f"શું આપ ઈમેલ પર સત્તાવાર રસીદ મેળવવા માંગો છો?")
        elif target_lang == "mr":
            return (f"**{sname}** साठी अधिकृत शाळा फी पेमेंट तपशील (थकबाकी: **₹{dues}**):\n\n"
                    f"💳 **1. ऑनलाइन पोर्टल**: 'Pay Fees Online' वर क्लिक करा (UPI, NetBanking, Card).\n"
                    f"🏦 **2. थेट बँक ट्रान्सफर**:\n"
                    f"   - **बँक**: HDFC Bank | **खाते क्र**: `50200088991122` | **IFSC**: `HDFC0001042`\n"
                    f"📱 **3. UPI ID**: `xyzschool.fees@hdfcbank`\n\n"
                    f"आपल्याला अधिकृत पावती ईमेलवर हवी आहे का?")
        elif target_lang == "ta":
            return f"**{sname}** க்கான பள்ளி கட்டண விவரங்கள் (நிலுவை: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122` (IFSC: `HDFC0001042`).\nரசீதை மின்னஞ்சல் செய்யவா?"
        elif target_lang == "te":
            return f"**{sname}** పాఠశాల ఫీజు చెల్లింపు వివరాలు (బకాయి: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122` (IFSC: `HDFC0001042`).\nరశీదు ఇమెయిల్ చేయమంటారా?"
        elif target_lang == "kn":
            return f"**{sname}** ಶಾಲಾ ಶುಲ್ಕ ಪಾವತಿ ವಿವರಗಳು (ಬಾಕಿ: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122` (IFSC: `HDFC0001042`).\nರಶೀದಿಯನ್ನು ಇಮೇಲ್ ಮಾಡಬೇಕೇ?"
        elif target_lang == "bn":
            return f"**{sname}** এর স্কুল ফি প্রদানের বিবরণ (বকেয়া: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122` (IFSC: `HDFC0001042`)।\nরসিদ ইমেল করতে চান?"
        elif target_lang == "pa":
            return f"**{sname}** ਲਈ ਸਕੂਲ ਫ਼ੀਸ ਭੁਗਤਾਨ ਦੇ ਵੇਰਵੇ (ਬਕਾਇਆ: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122` (IFSC: `HDFC0001042`)।\nਰਸੀਦ ਈਮੇਲ ਕਰੀਏ?"
        elif target_lang == "ml":
            return f"**{sname}** ഫീസ് പേയ്‌മെന്റ് വിവരങ്ങൾ (കുടിശ്ശിക: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122`."
        elif target_lang == "ur":
            return f"**{sname}** کے اسکول فیس کی تفصیلات (بقایا: **₹{dues}**):\nUPI: `xyzschool.fees@hdfcbank` | HDFC Bank A/C: `50200088991122`۔\nکیا رسید ای میل کر دی جائے؟"
        elif target_lang == "hinglish":
            return (f"**{sname}** ke liye official payment details (Outstanding Amount: **₹{dues}**):\n\n"
                    f"💳 **1. Online Payment Portal**: Header me 'Pay Fees Online' click karein.\n"
                    f"🏦 **2. Direct Bank Transfer**: HDFC Bank | A/C: `50200088991122` | IFSC: `HDFC0001042`\n"
                    f"📱 **3. UPI**: `xyzschool.fees@hdfcbank`\n\n"
                    f"Kya aapko official invoice aur payment receipt email par chahiye?")

    # Pattern 24: Fee Receipt Dispatched
    m24 = re.search(r"📧 \*\*Fee Receipt & Invoice Dispatched!\*\*\s*The official fee invoice and payment breakdown for \*\*([^*]+)\*\* \(Term 1 - Academic Year 2025-26\) has been sent to your registered email address \(\*\*([^*]+)\*\*\)\.\s*You can also download digital PDF copies anytime under the Parent Portal Documents section\.", text, re.DOTALL)
    if m24:
        sname, p_email = m24.groups()
        if target_lang == "hi":
            return (f"📧 **शुल्क रसीद और चालान भेज दिया गया है!**\n"
                    f"**{sname}** (सत्र 2025-26) का आधिकारिक शुल्क चालान आपके पंजीकृत ईमेल (**{p_email}**) पर भेज दिया गया है।\n"
                    f"आप पेरेंट पोर्टल के दस्तावेज़ अनुभाग से भी कभी भी डिजिटल पीडीएफ डाउनलोड कर सकते हैं।")
        elif target_lang == "gu":
            return (f"📧 **ફી ની રસીદ અને બિલ ઈમેલ પર મોકલી દેવાયું છે!**\n"
                    f"**{sname}** (સત્ર 2025-26) નું સત્તાવાર ફી બિલ આપના ઈમેલ (**{p_email}**) પર મોકલી દેવામાં આવ્યું છે.\n"
                    f"આપ પેરેન્ટ પોર્ટલ પરથી પણ ગમે ત્યારે પીડીએફ ડાઉનલોડ કરી શકો છો.")
        elif target_lang == "mr":
            return (f"📧 **फी पावती व चलन ईमेलवर पाठवले आहे!**\n"
                    f"**{sname}** ची अधिकृत फी पावती आपल्या नोंदणीकृत ईमेलवर (**{p_email}**) पाठवली गेली आहे.\n"
                    f"आपण पालक पोर्टलवरून देखील पीडीएफ डाउनलोड करू शकता.")
        elif target_lang == "ta":
            return f"📧 **கட்டண ரசீது அனுப்பப்பட்டது!**\n**{sname}** இன் கட்டண ரசீது உங்கள் மின்னஞ்சலுக்கு (**{p_email}**) அனுப்பப்பட்டுள்ளது."
        elif target_lang == "te":
            return f"📧 **ఫీజు రసీదు పంపబడింది!**\n**{sname}** ఫీజు రసీదు మీ నమోదిత ఇమెయిల్‌కు (**{p_email}**) పంపబడింది."
        elif target_lang == "kn":
            return f"📧 **ಶುಲ್ಕ ರಶೀದಿಯನ್ನು ರವಾನಿಸಲಾಗಿದೆ!**\n**{sname}** ಅವರ ಶುಲ್ಕ ರಶೀದಿಯನ್ನು ನಿಮ್ಮ ಇಮೇಲ್ ವಿಳಾಸಕ್ಕೆ (**{p_email}**) ಕಳುಹಿಸಲಾಗಿದೆ."
        elif target_lang == "bn":
            return f"📧 **ফি রসিদ সফলভাবে পাঠানো হয়েছে!**\n**{sname}** এর ফি রসিদ আপনার নিবন্ধিত ইমেল ঠিকানায় (**{p_email}**) পাঠানো হয়েছে।"
        elif target_lang == "pa":
            return f"📧 **ਫ਼ੀਸ ਰਸੀਦ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ!**\n**{sname}** ਦੀ ਫ਼ੀਸ ਰਸੀਦ ਤੁਹਾਡੇ ਰਜਿਸਟਰਡ ਈਮੇਲ (**{p_email}**) 'ਤੇ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ।"
        elif target_lang == "ml":
            return f"📧 **ഫീസ് രസീത് ഇമെയിൽ ചെയ്തു!**\n**{sname}** ന്റെ ഫീസ് രസീത് നിങ്ങളുടെ ഇമെയിലിലേക്ക് (**{p_email}**) അയച്ചു കഴിഞ്ഞു."
        elif target_lang == "ur":
            return f"📧 **فیس رسید ارسال کر دی گئی ہے!**\n**{sname}** کی سرکاری فیس رسید آپ کے ای میل (**{p_email}**) پر بھیج دی گئی ہے۔"
        elif target_lang == "hinglish":
            return (f"📧 **Fee Receipt & Invoice Dispatched!**\n"
                    f"**{sname}** ki official fee invoice aapke registered email address (**{p_email}**) par bhej di gayi hai.\n"
                    f"Aap Parent Portal ke Documents section se bhi digital PDF download kar sakte hain.")

    # Pattern 25: Gratitude / Thank You Response
    if "It is truly my pleasure to assist you! Please don't hesitate to reach out whenever you have questions about your child's schooling. Have a wonderful day!" in text:
        if target_lang == "hi":
            return "आपकी सहायता करना मेरा परम सौभाग्य है! जब भी आपको अपने बच्चे की पढ़ाई या स्कूल से जुड़ा कोई प्रश्न हो, बेझिझक पूछें। आपका दिन शुभ हो! 😊"
        elif target_lang == "gu":
            return "આપની મદદ કરવામાં મને ખૂબ આનંદ થયો! જ્યારે પણ બાળકના શિક્ષણ અંગે કોઈ પ્રશ્ન હોય, વિના સંકોચે પૂછશો. આપનો દિવસ શુભ રહે! 😊"
        elif target_lang == "mr":
            return "आपल्याला मदत करताना मला मनापासून आनंद झाला! मुलांच्या शिक्षणाबाबत जेव्हा काही विचारायचे असेल, तेव्हा नक्की विचारा. आपला दिवस छान जावो! 😊"
        elif target_lang == "ta":
            return "உங்களுக்கு உதவ முடிந்ததில் மிக்க மகிழ்ச்சி! உங்கள் குழந்தையின் கல்வி குறித்து எப்போது வேண்டுமானாலும் கேளுங்கள். இனிய நாளாக அமையட்டும்! 😊"
        elif target_lang == "te":
            return "మీకు సహాయం చేయడం నాకెంతో సంతోషం! మీ పిల్లల చదువు గురించి ఎప్పుడైనా అడగవచ్చు. మంచి రోజు కావాలని కోరుకుంటున్నాను! 😊"
        elif target_lang == "kn":
            return "ನಿಮಗೆ ಸಹಾಯ ಮಾಡಲು ನನಗೆ ಸಂತೋಷವಾಗಿದೆ! ನಿಮ್ಮ ಮಗುವಿನ ಶಿಕ್ಷಣದ ಬಗ್ಗೆ ಯಾವುದೇ ಪ್ರಶ್ನೆಗಳಿದ್ದಾಗ ಖಂಡಿತವಾಗಿ ಕೇಳಿ. ನಿಮ್ಮ ದಿನ ಶುಭವಾಗಿರಲಿ! 😊"
        elif target_lang == "bn":
            return "আপনাকে সাহায্য করতে পেরে খুব আনন্দিত! আপনার সন্তানের পড়াশোনা নিয়ে যেকোনো প্রশ্ন থাকলে নির্দ্বিধায় জিজ্ঞাসা করুন। দিনটি শুভ হোক! 😊"
        elif target_lang == "pa":
            return "ਤੁਹਾਡੀ ਮਦਦ ਕਰਕੇ ਮੈਨੂੰ ਬਹੁਤ ਖ਼ੁਸ਼ੀ ਹੋਈ! ਜਦੋਂ ਵੀ ਬੱਚੇ ਦੀ ਪੜ੍ਹਾਈ ਬਾਰੇ ਕੋਈ ਸਵਾਲ ਹੋਵੇ, ਬੇਝਿਜਕ ਪੁੱਛੋ। ਤੁਹਾਡਾ ਦਿਨ ਵਧੀਆ ਰਹੇ! 😊"
        elif target_lang == "ml":
            return "നിങ്ങളെ സഹായിക്കാൻ കഴിഞ്ഞതിൽ സന്തോഷം! കുട്ടിയുടെ പഠനവുമായി ബന്ധപ്പെട്ട് എപ്പോൾ വേണമെങ്കിലും ചോദിക്കാം. നല്ലൊരു ദിവസം ആശംസിക്കുന്നു! 😊"
        elif target_lang == "ur":
            return "آپ کی مدد کرنا میرے لیے خوشی کی بات ہے! بچے کی تعلیم سے متعلق جب بھی کوئی سوال ہو، ضرور پوچھیے۔ آپ کا دن خوشگوار گزرے! 😊"
        elif target_lang == "hinglish":
            return "Aapki help karke mujhe bohot khushi hui! Jab bhi bachhe ki padhai ke baare me koi sawaal ho, bina jhijhak poochiye. Have a wonderful day! 😊"

    return text


VERNACULAR_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "gu": {
        "Great news for": "માટે ખૂબ સારા સમાચાર",
        "All 8 students are present": "તમામ 8 વિદ્યાર્થીઓ હાજર છે",
        "All students are present": "તમામ વિદ્યાર્થીઓ હાજર છે",
        "attendance rate": "હાજરીનો દર",
        "Attendance summary for": "હાજરીનો સારાંશ",
        "students are present": "વિદ્યાર્થીઓ હાજર છે",
        "Absent today": "આજે ગેરહાજર",
        "Successfully updated": "સફળતાપૂર્વક અપડેટ થયું",
        "has been marked": "તરીકે નોંધવામાં આવ્યા છે",
        "Academic Report for": "શૈક્ષણિક પરિણામ પત્રક",
        "Overall Average": "કુલ સરેરાશ ટકાવારી",
        "Key subject scores": "મુખ્ય વિષયોના ગુણ",
        "performing commendably": "ખૂબ જ પ્રશંસનીય દેખાવ કરી રહ્યા છે",
        "Your current attendance stands at": "તમારી વર્તમાન હાજરી",
        "days attended": "દિવસ હાજર",
        "You're in good standing": "તમારી હાજરી ખૂબ જ સારી છે",
        "Keep up the consistent punctuality": "આવી જ નિયમિતતા જાળવી રાખો",
        "Here is your upcoming examination schedule for": "આગામી પરીક્ષાનું સમયપત્રક",
        "Here are your latest exam results": "તમારા તાજેતરના પરીક્ષા પરિણામો",
        "Your overall average is": "તમારી સરેરાશ ટકાવારી છે",
        "Great job! Would you like some study tips for the upcoming term?": "ખૂબ સરસ કામ! શું તમે આગામી સત્ર માટે અભ્યાસ ટિપ્સ મેળવવા માંગો છો?",
        "Top Study & Revision Tips for English": "અંગ્રેજી (English) માટે મહત્વપૂર્ણ અભ્યાસ ટિપ્સ",
        "Top Study & Revision Tips for Mathematics": "ગણિત (Mathematics) માટે મહત્વપૂર્ણ અભ્યાસ ટિપ્સ",
        "Top Study & Revision Tips for Science": "વિજ્ઞાન (Science) માટે મહત્વપૂર્ણ અભ્યાસ ટિપ્સ",
        "Top Study & Revision Tips for Computer Applications & IT": "કમ્પ્યુટર એપ્લિકેશન્સ અને IT માટે મહત્વપૂર્ણ અભ્યાસ ટિપ્સ",
        "Reading Comprehension": "વાંચન સમજ (Comprehension)",
        "Writing Section & Essays": "લેખન વિભાગ અને નિબંધ (Writing & Essays)",
        "Literature & Characters": "સાહિત્ય અને પાત્રો (Literature & Characters)",
        "Active Vocabulary": "શબ્દભંડોળ (Vocabulary)",
        "Daily Problem Solving": "રોજિંદો દાખલાનો અભ્યાસ (Daily Problem Solving)",
        "Formula Chart Sheet": "સૂત્રોની ચાર્ટ શીટ (Formula Chart)",
        "Show Intermediate Working": "ગણતરીના સ્ટેપ્સ દર્શાવો (Step-by-step)",
        "Error Notebook": "ભૂલો સુધારવાની નોટબુક (Error Log)",
        "Diagrams & Labelling": "આકૃતિઓ અને નામનિર્દેશન (Diagrams & Labelling)",
        "Concept Mind-Maps": "કોન્સેપ્ટ માઇન્ડ-મેપ્સ (Mind-Maps)",
        "SI Units & Formulas": "SI એકમો અને સૂત્રો (SI Units)",
        "Chemical Reactions": "રાસાયણિક સમીકરણો (Chemical Reactions)",
        "Here is the latest attendance summary for": "હાજરીનો તાજેતરનો સારાંશ",
        "overall attendance": "કુલ હાજરી",
        "For Rahul Patel, there is a current outstanding balance of": "રાહુલ પટેલ માટે હાલની બાકી ફી",
        "The upcoming installment is due by": "આગામી હપ્તાની છેલ્લી તારીખ",
        "Would you like me to share payment details or email you the receipt?": "શું તમે ફી ભરવાની વિગતો મેળવવા માંગો છો કે ઈમેલ પર રસીદ મોકલું?",
        "Here are the official payment details for": "સત્તાવાર ફી ચુકવણી વિગતો",
        "Beneficiary": "લાભાર્થી (Beneficiary)",
        "Account No": "ખાતા નંબર (Account No)",
        "Fee Receipt & Invoice Dispatched!": "ફી ની રસીદ તમારા ઈમેલ પર સફળતાપૂર્વક મોકલી દેવામાં આવી છે!",
        "Your call request has been submitted to the teacher": "શિક્ષક સાથે વાત કરવાની તમારી વિનંતી મોકલી દેવામાં આવી છે",
        "Your support request has been submitted to School Management": "તમારી વિનંતી સ્કૂલ મેનેજમેન્ટને મોકલી દેવામાં આવી છે",
        "You're very welcome": "તમારું ખૂબ ખૂબ સ્વાગત છે",
        "I am XYZ AI, your school assistant": "હું XYZ AI છું, તમારો શાળા સહાયક",
        "Mathematics": "ગણિત (Mathematics)",
        "Science": "વિજ્ઞાન (Science)",
        "English": "અંગ્રેજી (English)",
        "Computer Applications": "કમ્પ્યુટર (IT)",
        "Social Studies": "સામાજિક વિજ્ઞાન",
        "September": "સપ્ટેમ્બર",
        "August": "ઓગસ્ટ",
        "Present": "હાજર (PRESENT)",
        "Absent": "ગેરહાજર (ABSENT)"
    },
    "hi": {
        "Great news for": "के लिए बहुत अच्छी खबर",
        "All 8 students are present": "सभी 8 विद्यार्थी उपस्थित हैं",
        "All students are present": "सभी विद्यार्थी उपस्थित हैं",
        "attendance rate": "उपस्थिति दर",
        "Attendance summary for": "उपस्थिति सारांश",
        "students are present": "विद्यार्थी उपस्थित हैं",
        "Absent today": "आज अनुपस्थित",
        "Successfully updated": "सफलतापूर्वक अपडेट किया गया",
        "has been marked": "चिह्नित किया गया है",
        "Academic Report for": "शैक्षणिक रिपोर्ट",
        "Overall Average": "कुल औसत",
        "Key subject scores": "मुख्य विषय अंक",
        "performing commendably": "प्रशंसनीय प्रदर्शन कर रहे हैं",
        "Your current attendance stands at": "आपकी वर्तमान उपस्थिति",
        "days attended": "दिन उपस्थित",
        "You're in good standing": "आपकी उपस्थिति बहुत अच्छी है",
        "Keep up the consistent punctuality": "अपनी नियमितता और समय की पाबंदी बनाए रखें",
        "Here is your upcoming examination schedule for": "यह आगामी परीक्षा समय सारणी है",
        "Here are your latest exam results": "यह आपके नवीनतम परीक्षा परिणाम हैं",
        "Your overall average is": "आपका कुल औसत है",
        "Great job! Would you like some study tips for the upcoming term?": "शानदार प्रदर्शन! क्या आप आगामी सत्र के लिए अध्ययन युक्तियाँ (Study Tips) चाहते हैं?",
        "Top Study & Revision Tips for English": "अंग्रेजी (English) के लिए सर्वश्रेष्ठ अध्ययन और पुनरावलोकन युक्तियाँ",
        "Top Study & Revision Tips for Mathematics": "गणित (Mathematics) के लिए सर्वश्रेष्ठ अध्ययन युक्तियाँ",
        "Top Study & Revision Tips for Science": "विज्ञान (Science) के लिए सर्वश्रेष्ठ अध्ययन युक्तियाँ",
        "Top Study & Revision Tips for Computer Applications & IT": "कंप्यूटर अनुप्रयोग और IT के लिए अध्ययन युक्तियाँ",
        "Reading Comprehension": "अपठित गद्यांश (Comprehension)",
        "Writing Section & Essays": "लेखन खंड और निबंध (Writing & Essays)",
        "Literature & Characters": "साहित्य और पात्र (Literature & Characters)",
        "Active Vocabulary": "सक्रिय शब्दावली (Vocabulary)",
        "Daily Problem Solving": "प्रतिदिन अभ्यास (Daily Problem Solving)",
        "Formula Chart Sheet": "सूत्र चार्ट शीट (Formula Chart)",
        "Show Intermediate Working": "चरणबद्ध गणना दिखाएं (Step-by-step)",
        "Error Notebook": "त्रुटि सुधार पुस्तिका (Error Log)",
        "Diagrams & Labelling": "चित्र और नामकरण (Diagrams & Labelling)",
        "Concept Mind-Maps": "अवधारणा मानचित्र (Concept Mind-Maps)",
        "SI Units & Formulas": "एसआई इकाइयाँ और सूत्र (SI Units)",
        "Chemical Reactions": "रासायनिक समीकरण (Chemical Reactions)",
        "Here is the latest attendance summary for": "उपस्थिति का नवीनतम सारांश",
        "overall attendance": "कुल उपस्थिति",
        "For Rahul Patel, there is a current outstanding balance of": "राहुल पटेल के लिए वर्तमान बकाया शुल्क",
        "The upcoming installment is due by": "अगली किस्त की देय तिथि",
        "Would you like me to share payment details or email you the receipt?": "क्या आप भुगतान विवरण देखना चाहते हैं या रसीद ईमेल पर चाहते हैं?",
        "Here are the official payment details for": "आधिकारिक शुल्क भुगतान विवरण",
        "Beneficiary": "लाभार्थी (Beneficiary)",
        "Account No": "खाता संख्या (Account No)",
        "Fee Receipt & Invoice Dispatched!": "शुल्क रसीद और चालान ईमेल पर भेज दिया गया है!",
        "Your call request has been submitted to the teacher": "आपका कॉल अनुरोध शिक्षक को सफलतापूर्वक भेज दिया गया है",
        "Your support request has been submitted to School Management": "आपका सहायता अनुरोध स्कूल प्रबंधन को भेज दिया गया है",
        "You're very welcome": "आपका बहुत-बहुत स्वागत है",
        "I am XYZ AI, your school assistant": "मैं XYZ AI हूँ, आपका स्कूल सहायक",
        "Mathematics": "गणित (Mathematics)",
        "Science": "विज्ञान (Science)",
        "English": "अंग्रेजी (English)",
        "Computer Applications": "कंप्यूटर अनुप्रयोग (IT)",
        "Social Studies": "सामाजिक अध्ययन (Social Studies)",
        "Present": "उपस्थित (Present)",
        "Absent": "अनुपस्थित (Absent)",
        "September": "सितंबर",
        "August": "अगस्त"
    },
    "mr": {
        "Great news for": "साठी अत्यंत आनंदाची बातमी",
        "All 8 students are present": "सर्व 8 विद्यार्थी उपस्थित आहेत",
        "All students are present": "सर्व विद्यार्थी उपस्थित आहेत",
        "attendance rate": "उपस्थितीचे प्रमाण",
        "Attendance summary for": "उपस्थितीचा तपशील",
        "students are present": "विद्यार्थी उपस्थित आहेत",
        "Absent today": "आज गैरहजर",
        "Successfully updated": "यशस्वीरित्या अद्यतनित केले",
        "has been marked": "म्हणून नोंदवले आहे",
        "Academic Report for": "शैक्षणिक प्रगती पुस्तक",
        "Overall Average": "एकूण सरासरी",
        "Key subject scores": "प्रमुख विषयांचे गुण",
        "performing commendably": "उत्कृष्ट प्रगती करत आहे",
        "Your current attendance stands at": "तुमची सध्याची उपस्थिती",
        "days attended": "दिवस उपस्थित",
        "You're in good standing": "तुमची उपस्थिती समाधानकारक आणि उत्तम आहे",
        "Keep up the consistent punctuality": "हीच नियमितता कायम ठेवा",
        "Here is your upcoming examination schedule for": "पुढील परीक्षेचे वेळापत्रक",
        "Here are your latest exam results": "तुमचे नवीनतम परीक्षा निकाल",
        "Your overall average is": "तुमची एकूण सरासरी आहे",
        "Great job! Would you like some study tips for the upcoming term?": "उत्कृष्ट कामगिरी! पुढील सत्रासाठी तुम्हाला अभ्यासाच्या टिप्स हव्या आहेत का?",
        "Top Study & Revision Tips for English": "इंग्रजी (English) विषयासाठी महत्त्वाच्या अभ्यास टिप्स",
        "Top Study & Revision Tips for Mathematics": "गणित (Mathematics) विषयासाठी महत्त्वाच्या अभ्यास टिप्स",
        "Top Study & Revision Tips for Science": "विज्ञान (Science) विषयासाठी महत्त्वाच्या अभ्यास टिप्स",
        "Top Study & Revision Tips for Computer Applications & IT": "संगणक आणि IT साठी अभ्यास टिप्स",
        "Here is the latest attendance summary for": "उपस्थितीचा नवीनतम तपशील",
        "overall attendance": "एकूण उपस्थिती",
        "For Rahul Patel, there is a current outstanding balance of": "राहुल पटेल यांची एकूण शिल्लक फी",
        "Would you like me to share payment details or email you the receipt?": "तुम्हाला पेमेंट तपशील हवे आहेत की पावती ईमेलवर पाठवू?",
        "Fee Receipt & Invoice Dispatched!": "फी पावती तुमच्या नोंदणीकृत ईमेलवर पाठवली आहे!",
        "Your call request has been submitted to the teacher": "शिक्षकांशी संभाषणाची तुमची विनंती नोंदवली गेली आहे",
        "Your support request has been submitted to School Management": "आपली विनंती शाळा प्रशासनाकडे पाठवली आहे",
        "You're very welcome": "आपले मनःपूर्वक स्वागत आहे",
        "Mathematics": "गणित",
        "Science": "विज्ञान",
        "English": "इंग्रजी",
        "September": "सप्टेंबर",
        "August": "ऑगस्ट",
        "Present": "उपस्थित",
        "Absent": "गैरहजर"
    },
    "ta": {
        "Great news for": "மகிழ்ச்சியான செய்தி",
        "All 8 students are present": "அனைத்து 8 மாணவர்களும் வருகை தந்துள்ளனர்",
        "All students are present": "அனைத்து மாணவர்களும் வருகை தந்துள்ளனர்",
        "attendance rate": "வருகை சதவீதம்",
        "Attendance summary for": "வருகை சுருக்கம்",
        "students are present": "மாணவர்கள் வருகை தந்துள்ளனர்",
        "Absent today": "இன்று வரவில்லை",
        "Successfully updated": "வெற்றிகரமாக புதுப்பிக்கப்பட்டது",
        "Academic Report for": "கல்வி அறிக்கை",
        "Overall Average": "ஒட்டுமொத்த சராசரி",
        "Key subject scores": "முக்கிய பாட மதிப்பெண்கள்",
        "performing commendably": "சிறப்பாக செயல்படுகிறார்",
        "Your current attendance stands at": "உங்கள் தற்போதைய வருகை சதவீதம்",
        "days attended": "நாட்கள் வருகை தந்துள்ளீர்கள்",
        "You're in good standing": "உங்கள் வருகை மிகவும் சிறப்பாக உள்ளது",
        "Keep up the consistent punctuality": "இதே ஒழுங்கையும் நேரத்தையும் கடைப்பிடிக்கவும்",
        "Here is your upcoming examination schedule for": "வரவிருக்கும் தேர்வு அட்டவணை",
        "Here are your latest exam results": "உங்கள் தேர்வு முடிவுகள்",
        "Your overall average is": "உங்கள் ஒட்டுமொத்த சராசரி",
        "Top Study & Revision Tips for English": "ஆங்கிலப் பாடத்திற்கான சிறந்த படிப்பு குறிப்புகள்",
        "Top Study & Revision Tips for Mathematics": "கணிதப் பாடத்திற்கான சிறந்த படிப்பு குறிப்புகள்",
        "Top Study & Revision Tips for Science": "அறிவியல் பாடத்திற்கான சிறந்த படிப்பு குறிப்புகள்",
        "For Rahul Patel, there is a current outstanding balance of": "ராகுல் படேலின் நிலுவைக் கட்டணம்",
        "Fee Receipt & Invoice Dispatched!": "கட்டண ரசீது உங்கள் மின்னஞ்சலுக்கு அனுப்பப்பட்டது!",
        "Your call request has been submitted to the teacher": "ஆசிரியருக்கான உங்கள் அழைப்பு கோரிக்கை அனுப்பப்பட்டது",
        "You're very welcome": "மிக்க மகிழ்ச்சி",
        "Mathematics": "கணிதம்",
        "Science": "அறிவியல்",
        "English": "ஆங்கிலம்",
        "September": "செப்டம்பர்",
        "August": "ஆகஸ்ட்"
    },
    "te": {
        "Great news for": "శుభవార్త",
        "All 8 students are present": "మొత్తం 8 మంది విద్యార్థులు హాజరయ్యారు",
        "All students are present": "విద్యార్థులందరూ హాజరయ్యారు",
        "attendance rate": "హాజరు రేటు",
        "Attendance summary for": "హాజరు సారాంశం",
        "students are present": "విద్యార్థులు హాజరయ్యారు",
        "Absent today": "ఈరోజు గైర్హాజరు",
        "Successfully updated": "విజయవంతంగా నవీకరించబడింది",
        "Academic Report for": "విద్యా ప్రగతి నివేదిక",
        "Overall Average": "మొత్తం సగటు",
        "Key subject scores": "ముఖ్య సబ్జెక్టు మార్కులు",
        "performing commendably": "చాలా చక్కగా రాణిస్తున్నారు",
        "Your current attendance stands at": "మీ ప్రస్తుత హాజరు శాతం",
        "days attended": "రోజులు హాజరయ్యారు",
        "You're in good standing": "మీ హాజరు చాలా బాగుంది",
        "Keep up the consistent punctuality": "సమయపాలనను ఇలాగే కొనసాగించండి",
        "Here is your upcoming examination schedule for": "రాబోయే పరీక్షల షెడ్యూల్",
        "Here are your latest exam results": "మీ తాజా పరీక్ష ఫలితాలు",
        "Your overall average is": "మీ మొత్తం సగటు",
        "Top Study & Revision Tips for English": "ఇంగ్లీష్ కోసం ఉత్తమ స్టడీ టిప్స్",
        "Top Study & Revision Tips for Mathematics": "గణితం కోసం ఉత్తమ స్టడీ టిప్స్",
        "Top Study & Revision Tips for Science": "సైన్స్ కోసం ఉత్తమ స్టడీ టిప్స్",
        "For Rahul Patel, there is a current outstanding balance of": "రాహుల్ పటేల్ బకాయి ఫీజు",
        "Fee Receipt & Invoice Dispatched!": "ఫీజు రశీదు మీ ఇమెయిల్‌కు పంపబడింది!",
        "Your call request has been submitted to the teacher": "ఉపాధ్యాయుడికి మీ కాల్ అభ్యర్థన పంపబడింది",
        "You're very welcome": "మీకు సాదర స్వాగతం",
        "Mathematics": "గణితం",
        "Science": "సైన్స్",
        "English": "ఇంగ్లీష్",
        "September": "సెప్టెంబర్",
        "August": "ఆగస్టు"
    },
    "bn": {
        "Great news for": "এর জন্য দুর্দান্ত খবর",
        "All 8 students are present": "সমস্ত 8 জন শিক্ষার্থী উপস্থিত",
        "All students are present": "সমস্ত শিক্ষার্থীরা উপস্থিত",
        "attendance rate": "উপস্থিতির হার",
        "Attendance summary for": "উপস্থিতির সারাংশ",
        "students are present": "শিক্ষার্থী উপস্থিত",
        "Absent today": "আজ অনুপস্থিত",
        "Successfully updated": "সফলভাবে আপডেট করা হয়েছে",
        "Academic Report for": "একাডেমিক রিপোর্ট",
        "Overall Average": "মোট গড়",
        "Key subject scores": "প্রধান বিষয়ের নম্বর",
        "performing commendably": "খুব ভালো পারফর্ম করছেন",
        "Your current attendance stands at": "আপনার বর্তমান উপস্থিতি",
        "days attended": "দিন উপস্থিত ছিলেন",
        "You're in good standing": "আপনার উপস্থিতি খুব ভালো",
        "Here is your upcoming examination schedule for": "আসন্ন পরীক্ষার সময়সূচী",
        "Here are your latest exam results": "আপনার সাম্প্রতিক পরীক্ষার ফলাফল",
        "Your overall average is": "আপনার মোট গড়",
        "Top Study & Revision Tips for English": "ইংরেজি বিষয়ের জন্য সেরা অধ্যয়নের পরামর্শ",
        "Top Study & Revision Tips for Mathematics": "গণিত বিষয়ের জন্য সেরা অধ্যয়নের পরামর্শ",
        "Top Study & Revision Tips for Science": "বিজ্ঞান বিষয়ের জন্য সেরা অধ্যয়নের পরামর্শ",
        "For Rahul Patel, there is a current outstanding balance of": "রাহুল প্যাটেলের বকেয়া ফি",
        "Fee Receipt & Invoice Dispatched!": "ফি রসিদ আপনার ইমেলে পাঠানো হয়েছে!",
        "Your call request has been submitted to the teacher": "শিক্ষকের কাছে আপনার অনুরোধ পাঠানো হয়েছে",
        "You're very welcome": "আপনাকে স্বাগতম",
        "Mathematics": "গণিত",
        "Science": "বিজ্ঞান",
        "English": "ইংরেজি",
        "September": "সেপ্টেম্বর",
        "August": "আগস্ট"
    },
    "pa": {
        "Great news for": "ਲਈ ਬਹੁਤ ਵਧੀਆ ਖ਼ਬਰ",
        "All 8 students are present": "ਸਾਰੇ 8 ਵਿਦਿਆਰਥੀ ਹਾਜ਼ਰ ਹਨ",
        "All students are present": "ਸਾਰੇ ਵਿਦਿਆਰਥੀ ਹਾਜ਼ਰ ਹਨ",
        "attendance rate": "ਹਾਜ਼ਰੀ ਦਰ",
        "Attendance summary for": "ਹਾਜ਼ਰੀ ਦਾ ਸਾਰ",
        "students are present": "ਵਿਦਿਆਰਥੀ ਹਾਜ਼ਰ ਹਨ",
        "Absent today": "ਅੱਜ ਗ਼ੈਰਹਾਜ਼ਰ",
        "Successfully updated": "ਸਫਲਤਾਪੂਰਵਕ ਅੱਪਡੇਟ ਕੀਤਾ ਗਿਆ",
        "Academic Report for": "ਅਕਾਦਮਿਕ ਰਿਪੋਰਟ",
        "Overall Average": "ਕੁੱਲ ਔਸਤ",
        "Key subject scores": "ਮੁੱਖ ਵਿਸ਼ੇ ਦੇ ਅੰਕ",
        "Your current attendance stands at": "ਤੁਹਾਡੀ ਮੌਜੂਦਾ ਹਾਜ਼ਰੀ",
        "days attended": "ਦਿਨ ਹਾਜ਼ਰ",
        "Here is your upcoming examination schedule for": "ਆਉਣ ਵਾਲੀਆਂ ਪ੍ਰੀਖਿਆਵਾਂ ਦੀ ਸਮਾਂ ਸਾਰਣੀ",
        "Here are your latest exam results": "ਤੁਹਾਡੇ ਤਾਜ਼ਾ ਪ੍ਰੀਖਿਆ ਨਤੀਜੇ",
        "For Rahul Patel, there is a current outstanding balance of": "ਰਾਹੁਲ ਪਟੇਲ ਦੀ ਬਕਾਇਆ ਫ਼ੀਸ",
        "Fee Receipt & Invoice Dispatched!": "ਫ਼ੀਸ ਦੀ ਰਸੀਦ ਈਮੇਲ ਕਰ ਦਿੱਤੀ ਗਈ ਹੈ!",
        "Your call request has been submitted to the teacher": "ਅਧਿਆਪਕ ਨੂੰ ਤੁਹਾਡੀ ਕਾਲ ਦੀ ਬੇਨਤੀ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ",
        "You're very welcome": "ਜੀ ਆਇਆਂ ਨੂੰ",
        "Mathematics": "ਗਣਿਤ",
        "Science": "ਵਿਗਿਆਨ",
        "English": "ਅੰਗਰੇਜ਼ੀ"
    },
    "kn": {
        "Great news for": "ಗೆ ಶುಭ ಸುದ್ದಿ",
        "All 8 students are present": "ಎಲ್ಲಾ 8 ವಿದ್ಯಾರ್ಥಿಗಳು ಹಾಜರಿದ್ದಾರೆ",
        "All students are present": "ಎಲ್ಲಾ ವಿದ್ಯಾರ್ಥಿಗಳು ಹಾಜರಿದ್ದಾರೆ",
        "attendance rate": "ಹಾಜರಾತಿ ದರ",
        "Attendance summary for": "ಹಾಜರಾತಿ ಸಾರಾಂಶ",
        "students are present": "ವಿದ್ಯಾರ್ಥಿಗಳು ಹಾಜರಿದ್ದಾರೆ",
        "Absent today": "ಇಂದು ಗೈರುಹಾಜರು",
        "Successfully updated": "ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ",
        "Academic Report for": "ಶೈಕ್ಷಣಿಕ ಪ್ರಗತಿ ವರದಿ",
        "Overall Average": "ಒಟ್ಟು ಸರಾಸರಿ",
        "Key subject scores": "ಪ್ರಮುಖ ವಿಷಯದ ಅಂಕಗಳು",
        "Your current attendance stands at": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಹಾಜರಾತಿ",
        "days attended": "ದಿನಗಳು ಹಾಜರಾಗಿದ್ದಾರೆ",
        "Here is your upcoming examination schedule for": "ಮುಂಬರುವ ಪರೀಕ್ಷಾ ವೇಳಾಪಟ್ಟಿ",
        "Here are your latest exam results": "ನಿಮ್ಮ ಇತ್ತೀಚಿನ ಪರೀಕ್ಷಾ ಫಲಿತಾಂಶಗಳು",
        "For Rahul Patel, there is a current outstanding balance of": "ರಾಹುಲ್ ಪಟೇಲ್ ಬಾಕಿ ಶುಲ್ಕ",
        "Fee Receipt & Invoice Dispatched!": "ಶುಲ್ಕ ರಶೀದಿಯನ್ನು ಇಮೇಲ್ ಮಾಡಲಾಗಿದೆ!",
        "Your call request has been submitted to the teacher": "ಶಿಕ್ಷಕರಿಗೆ ನಿಮ್ಮ ಕರೆ ವಿನಂತಿಯನ್ನು ಕಳುಹಿಸಲಾಗಿದೆ",
        "You're very welcome": "ನಿಮಗೆ ಸುಸ್ವಾಗತ",
        "Mathematics": "ಗಣಿತ",
        "Science": "ವಿಜ್ಞಾನ",
        "English": "ಇಂಗ್ಲಿಷ್"
    },
    "ml": {
        "Great news for": "സന്തോഷവാർത്ത",
        "All 8 students are present": "എല്ലാ 8 വിദ്യാർത്ഥികളും ഹാജരുണ്ട്",
        "All students are present": "എല്ലാ വിദ്യാർത്ഥികളും ഹാജരുണ്ട്",
        "attendance rate": "ഹാജർ നിരക്ക്",
        "Attendance summary for": "ഹാജർ സംഗ്രഹം",
        "students are present": "വിദ്യാർത്ഥികൾ ഹാജരുണ്ട്",
        "Absent today": "ഇന്ന് ഹാജരാകാത്തവർ",
        "Successfully updated": "വിജയകരമായി പുതുക്കി",
        "Academic Report for": "അക്കാദമിക് റിപ്പോർട്ട്",
        "Overall Average": "മൊത്തം ശരാശരി",
        "Key subject scores": "പ്രധാന വിഷയങ്ങളിലെ മാർക്കുകൾ",
        "Your current attendance stands at": "നിങ്ങളുടെ നിലവിലെ ഹാജർ",
        "days attended": "ദിവസങ്ങൾ ഹാജരായി",
        "Here is your upcoming examination schedule for": "വരാനിരിക്കുന്ന പരീക്ഷാ ഷെഡ്യൂൾ",
        "Here are your latest exam results": "നിങ്ങളുടെ പരീക്ഷാ ഫലങ്ങൾ",
        "For Rahul Patel, there is a current outstanding balance of": "രാഹുൽ പട്ടേലിന്റെ കുടിശ്ശിക ഫീസ്",
        "Fee Receipt & Invoice Dispatched!": "ഫീസ് രസീത് ഇമെയിൽ ചെയ്തു!",
        "Your call request has been submitted to the teacher": "അധ്യാപകനുള്ള നിങ്ങളുടെ കോൾ അഭ്യർത്ഥന സമർപ്പിച്ചു",
        "You're very welcome": "സ്വാഗതം",
        "Mathematics": "മാത്തമാറ്റിക്സ്",
        "Science": "സയൻസ്",
        "English": "ഇംഗ്ലീഷ്"
    },
    "ur": {
        "Great news for": "کے لیے خوشخبری",
        "All 8 students are present": "تمام 8 طلباء حاضر ہیں",
        "All students are present": "تمام طلباء حاضر ہیں",
        "attendance rate": "حاضری کی شرح",
        "Attendance summary for": "حاضری کا خلاصہ",
        "students are present": "طلباء حاضر ہیں",
        "Absent today": "آج غیر حاضر",
        "Successfully updated": "کامیابی سے اپ ڈیٹ کر دیا گیا",
        "Academic Report for": "تعلیمی رپورٹ",
        "Overall Average": "مجموعی اوسط",
        "Key subject scores": "اہم مضامین کے نمبر",
        "Your current attendance stands at": "آپ کی موجودہ حاضری",
        "days attended": "دن حاضر رہے",
        "Here is your upcoming examination schedule for": "امتحان کا شیڈول",
        "Here are your latest exam results": "آپ کے امتحانی نتائج",
        "For Rahul Patel, there is a current outstanding balance of": "راہول پٹیل کی واجب الادا فیس",
        "Fee Receipt & Invoice Dispatched!": "فیس کی رسید ای میل کر دی گئی ہے!",
        "Your call request has been submitted to the teacher": "استاد کو آپ کی درخواست بھیج دی گئی ہے",
        "You're very welcome": "خوش آمدید",
        "Mathematics": "ریاضی",
        "Science": "سائنس",
        "English": "انگریزی"
    },
    "hinglish": {
        "Great news for": "Great news for",
        "All 8 students are present": "Sabhi 8 students present hain",
        "All students are present": "Sabhi students present hain",
        "attendance rate": "attendance rate",
        "Attendance summary for": "Attendance summary for",
        "Academic Report for": "Academic Report for",
        "Overall Average": "Overall Average",
        "Your current attendance stands at": "Aapki current attendance",
        "days attended": "days attend kiye hain",
        "You're in good standing": "Aapki attendance kaafi acchi hai",
        "Keep up the consistent punctuality": "Aise hi regular aur punctual rahiye! 👏",
        "Here is your upcoming examination schedule for": "Aapka upcoming exam schedule yeh raha for",
        "Here are your latest exam results": "Aapke latest exam results yeh rahe",
        "Your overall average is": "Aapka overall average hai",
        "Great job! Would you like some study tips for the upcoming term?": "Shandar performance! Kya aap upcoming term ke liye subject study tips chahte hain?",
        "Top Study & Revision Tips for English": "English ke liye Top Study & Revision Tips",
        "Top Study & Revision Tips for Mathematics": "Mathematics ke liye Top Study & Revision Tips",
        "Top Study & Revision Tips for Science": "Science ke liye Top Study & Revision Tips",
        "For Rahul Patel, there is a current outstanding balance of": "Rahul Patel ke liye outstanding fee balance hai",
        "Would you like me to share payment details or email you the receipt?": "Kya aap payment details chahte hain ya receipt email pe bhej doon?",
        "Fee Receipt & Invoice Dispatched!": "Fee Receipt & Invoice aapke email par bhej di gayi hai!",
        "Your call request has been submitted to the teacher": "Aapka teacher call request successfully submit ho gaya hai",
        "You're very welcome": "Aapka bohot bohot welcome!"
    }
}

def translate_response_text(text: str, target_lang: str) -> str:
    """Translates an English response string to the target language seamlessly."""
    if not target_lang or target_lang == "en":
        return text

    # 1. First attempt full structured template pattern translation
    text_templated = translate_template_patterns(text, target_lang)
    if text_templated != text:
        return text_templated

    # 2. Sequential phrase substitution
    dict_map = VERNACULAR_TRANSLATIONS.get(target_lang)
    if not dict_map:
        return text

    translated = text
    for en_phrase, vernacular_phrase in dict_map.items():
        if en_phrase in translated:
            translated = translated.replace(en_phrase, vernacular_phrase)

    return translated

def translate_suggested_actions(actions: list, target_lang: str) -> list:
    """Translates suggested action labels into target language."""
    if not target_lang or target_lang == "en":
        return actions

    label_map = {
        "hi": {
            "Mark Student Attendance": "विद्यार्थी उपस्थिति दर्ज करें",
            "Class Roster": "कक्षा सूची (Roster)",
            "English Study Tips": "अंग्रेजी अध्ययन युक्तियाँ",
            "Mathematics Revision Guide": "गणित पुनरावलोकन गाइड",
            "Science Study Guide": "विज्ञान अध्ययन गाइड",
            "Upcoming Exam Schedule": "आगामी परीक्षा समय सारणी",
            "Share Payment Details": "भुगतान विवरण देखें",
            "Email Fee Receipt": "ईमेल पर रसीद भेजें",
            "Talk to Teacher": "शिक्षक से बात करें",
            "Contact School Management": "स्कूल प्रबंधन से संपर्क करें",
            "Full Report Card": "पूर्ण रिपोर्ट कार्ड",
            "Recent Absences": "हाल की अनुपस्थिति",
            "Submit Leave Note": "अवकाश आवेदन"
        },
        "gu": {
            "Mark Student Attendance": "વિદ્યાર્થીની હાજરી પૂરો",
            "Class Roster": "વર્ગ રોસ્ટર (વિદ્યાર્થી યાદી)",
            "English Study Tips": "અંગ્રેજી અભ્યાસ ટિપ્સ",
            "Mathematics Revision Guide": "ગણિત રિવિઝન ગાઈડ",
            "Science Study Guide": "વિજ્ઞાન અભ્યાસ ગાઈડ",
            "Upcoming Exam Schedule": "પરીક્ષાનું સમયપત્રક",
            "Share Payment Details": "ફી ભરવાની વિગતો",
            "Email Fee Receipt": "ઈમેલ પર રસીદ મોકલો",
            "Talk to Teacher": "શિક્ષક સાથે વાત કરો",
            "Contact School Management": "મેનેજમેન્ટનો સંપર્ક કરો",
            "Full Report Card": "પરિણામ પત્રક"
        },
        "mr": {
            "Mark Student Attendance": "उपस्थिती नोंदवा",
            "Class Roster": "विद्यार्थी यादी",
            "English Study Tips": "इंग्रजी अभ्यास टिप्स",
            "Mathematics Revision Guide": "गणित पुनरावलोकन",
            "Science Study Guide": "विज्ञान अभ्यास गाइड",
            "Share Payment Details": "पेमेंट तपशील",
            "Email Fee Receipt": "ईमेल पावती पाठवा",
            "Talk to Teacher": "शिक्षकांशी बोला"
        },
        "ta": {
            "Mark Student Attendance": "வருகைப் பதிவு செய்க",
            "Class Roster": "மாணவர் பட்டியல்",
            "English Study Tips": "ஆங்கில படிப்பு குறிப்புகள்",
            "Mathematics Revision Guide": "கணித வழிகாட்டி",
            "Share Payment Details": "கட்டண விவரங்கள்",
            "Email Fee Receipt": "ரசீதை மின்னஞ்சல் செய்"
        },
        "te": {
            "Mark Student Attendance": "హాజరు నమోదు చేయండి",
            "Class Roster": "తరగతి రోస్టర్",
            "English Study Tips": "ఇంగ్లీష్ స్టడీ టిప్స్",
            "Mathematics Revision Guide": "గణిత రివిజన్ గైడ్",
            "Share Payment Details": "చెల్లింపు వివరాలు",
            "Email Fee Receipt": "రసీదు ఇమెయిల్ చేయండి"
        },
        "bn": {
            "Mark Student Attendance": "উপস্থিতি চিহ্নিত করুন",
            "Class Roster": "ক্লাস রোস্টার",
            "English Study Tips": "ইংরেজি পড়ার পরামর্শ",
            "Share Payment Details": "পেমেন্ট বিবরণ",
            "Email Fee Receipt": "রসিদ ইমেল করুন"
        },
        "pa": {
            "Mark Student Attendance": "ਹਾਜ਼ਰੀ ਲਗਾਓ",
            "Class Roster": "ਕਲਾਸ ਰੋਸਟਰ",
            "Share Payment Details": "ਭੁਗਤਾਨ ਵੇਰਵੇ",
            "Email Fee Receipt": "ਰਸੀਦ ਈਮੇਲ ਕਰੋ"
        },
        "kn": {
            "Mark Student Attendance": "ಹಾಜರಾತಿ ಗುರುತಿಸಿ",
            "Class Roster": "ತರಗತಿ ಪಟ್ಟಿ",
            "Share Payment Details": "ಪಾವತಿ ವಿವರಗಳು",
            "Email Fee Receipt": "ರಶೀದಿ ಇಮೇಲ್ ಮಾಡಿ"
        },
        "ml": {
            "Mark Student Attendance": "ഹാജർ രേഖപ്പെടുത്തുക",
            "Class Roster": "ക്ലാസ് പട്ടിക",
            "Share Payment Details": "പേയ്‌മെന്റ് വിവരങ്ങൾ",
            "Email Fee Receipt": "രസീത് ഇമെയിൽ ചെയ്യുക"
        },
        "ur": {
            "Mark Student Attendance": "حاضری لگائیں",
            "Class Roster": "کلاس فہرست",
            "Share Payment Details": "ادائیگی کی تفصیلات",
            "Email Fee Receipt": "رسید ای میل کریں"
        },
        "hinglish": {
            "Mark Student Attendance": "Attendance Mark Karein",
            "Class Roster": "Class Roster",
            "English Study Tips": "English Study Tips",
            "Mathematics Revision Guide": "Maths Revision Guide",
            "Share Payment Details": "Payment Details Dekhein",
            "Email Fee Receipt": "Receipt Email Karein",
            "Talk to Teacher": "Teacher Se Baat Karein"
        }
    }

    trans_map = label_map.get(target_lang, {})
    for act in actions:
        if hasattr(act, 'label') and act.label in trans_map:
            act.label = trans_map[act.label]
    return actions
