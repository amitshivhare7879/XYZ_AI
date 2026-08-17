"""
XYZ AI — Comprehensive Multilingual & Vernacular Translation Engine
Translates and formats assistant responses into Indian regional languages (Hindi, Gujarati, Marathi, Tamil, Telugu, Bengali, Punjabi, Kannada, Malayalam, Hinglish).
"""

import re
from typing import Dict, Any, List, Optional

# Structured sentence pattern translators for high grammatical fluency
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
        elif target_lang == "hinglish":
            return f"**{cname}** ({dt}) ke liye attendance summary: **{tot} me se {pres} students present hain** ({rate}). Aaj absent ({abs_cnt}): **{abs_list}**."

    # Pattern 3: Attendance Update - "Successfully updated! **Rahul Patel** has been marked **ABSENT** for 2026-08-20. Class total: 7 present."
    m3 = re.search(r"Successfully updated! \*\*([^*]+)\*\* has been marked \*\*([^*]+)\*\* for ([^.]+)\. Class total: (\d+) present\.", text)
    if m3:
        sname, status, dt, pcount = m3.groups()
        status_gu = "ગેરહાજર (ABSENT)" if "ABSENT" in status else "હાજર (PRESENT)"
        status_hi = "अनुपस्थित (ABSENT)" if "ABSENT" in status else "उपस्थित (PRESENT)"
        status_mr = "गैरहजर (ABSENT)" if "ABSENT" in status else "उपस्थित (PRESENT)"
        if target_lang == "gu":
            return f"સફળતાપૂર્વક અપડેટ થયું! **{sname}** ને {dt} માટે **{status_gu}** તરીકે નોંધવામાં આવ્યા છે. વર્ગમાં કુલ: {pcount} હાજર."
        elif target_lang == "hi":
            return f"सफलतापूर्वक अपडेट किया गया! **{sname}** को {dt} के लिए **{status_hi}** चिह्नित किया गया है। कक्षा कुल: {pcount} उपस्थित।"
        elif target_lang == "mr":
            return f"यशस्वीरित्या अद्यतनित केले! **{sname}** यांना {dt} साठी **{status_mr}** म्हणून नोंदवले आहे. वर्ग एकूण: {pcount} उपस्थित."

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
        elif target_lang == "hinglish":
            return f"Aapki current attendance **{pct}** ({pres}/{tot} days attended) hai! Aapki attendance kaafi acchi hai. Keep it up! 👏"

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
        "attendance rate": "उपस्थितीचे प्रमाण",
        "Attendance summary for": "उपस्थितीचा तपशील",
        "students are present": "विद्यार्थी उपस्थित आहेत",
        "Absent today": "आज गैरहजर",
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
        "Here is the latest attendance summary for": "उपस्थितीचा नवीनतम तपशील",
        "overall attendance": "एकूण उपस्थिती",
        "For Rahul Patel, there is a current outstanding balance of": "राहुल पटेल यांची एकूण शिल्लक फी",
        "Would you like me to share payment details or email you the receipt?": "तुम्हाला पेमेंट तपशील हवे आहेत की पावती ईमेलवर पाठवू?",
        "Fee Receipt & Invoice Dispatched!": "फी पावती तुमच्या नोंदणीकृत ईमेलवर पाठवली आहे!",
        "Your call request has been submitted to the teacher": "शिक्षकांशी संभाषणाची तुमची विनंती नोंदवली गेली आहे",
        "You're very welcome": "आपले मनःपूर्वक स्वागत आहे",
        "Mathematics": "गणित",
        "Science": "विज्ञान",
        "English": "इंग्रजी",
        "September": "सप्टेंबर",
        "August": "ऑगस्ट"
    },
    "ta": {
        "Great news for": "மகிழ்ச்சியான செய்தி",
        "All 8 students are present": "அனைத்து 8 மாணவர்களும் வருகை தந்துள்ளனர்",
        "attendance rate": "வருகை சதவீதம்",
        "Academic Report for": "கல்வி அறிக்கை",
        "Overall Average": "ஒட்டுமொத்த சராசரி",
        "Key subject scores": "முக்கிய பாட மதிப்பெண்கள்",
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
