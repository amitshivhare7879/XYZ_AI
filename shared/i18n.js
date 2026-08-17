/**
 * XYZ AI — Ultra-Reliable Bi-Directional Multi-Language System (shared/i18n.js)
 * Supports continuous, unlimited switching across 12 languages with full DOM & chat translation.
 */

(function(global) {
  const UI_DICTIONARIES = {
    en: {
      "Attendance Rate": "Attendance Rate",
      "Academic Grade": "Academic Grade",
      "Upcoming Tasks": "Upcoming Tasks",
      "Academic Standing": "Academic Standing",
      "83 Present / 91 Total Days": "83 Present / 91 Total Days",
      "Annual Rank: Top 5%": "Annual Rank: Top 5%",
      "Math & Science due Friday": "Math & Science due Friday",
      "Go Live Voice": "Go Live Voice",
      "Switch": "Switch",
      "Student Academic Assistant": "Student Academic Assistant",
      "Parent Support Assistant": "Parent Support Assistant",
      "Teacher Assistant": "Teacher Assistant",
      "Management Assistant": "Management Assistant",
      "AI Academic Assistant": "AI Academic Assistant",
      "Today's Schedule": "Today's Schedule",
      "Homework & Assignments": "Homework & Assignments",
      "Attendance Record": "Attendance Record",
      "Academic Report Card": "Academic Report Card",
      "Fee Invoices & Receipts": "Fee Invoices & Receipts",
      "School Notices": "School Notices",
      "Class Attendance": "Class Attendance",
      "Grade Entry": "Grade Entry",
      "Curriculum Planning": "Curriculum Planning",
      "Executive Analytics": "Executive Analytics",
      "Fee Reconciliation": "Fee Reconciliation",
      "Staff Roster": "Staff Roster",
      "Campus Safety": "Campus Safety",
      "Ask XYZ AI anything...": "Ask XYZ AI anything...",
      "Send": "Send",
      "Pay Fees Online": "Pay Fees Online",
      "Submit Leave Note": "Submit Leave Note",
      "Talk to Teacher": "Talk to Teacher",
      "Contact School Management": "Contact School Management",
      "Total Outstanding Dues": "Total Outstanding Dues",
      "Upcoming Exam Dates": "Upcoming Exam Dates",
      "Recent Absences": "Recent Absences",
      "Active Students": "Active Students",
      "Faculty on Duty": "Faculty on Duty",
      "Monthly Fee Collection": "Monthly Fee Collection",
      "Pending Escalations": "Pending Escalations",
      "View Schedule": "View Schedule",
      "Check Absences": "Check Absences",
      "Download Report": "Download Report",
      "Pay Now": "Pay Now"
    },
    hi: {
      "Attendance Rate": "उपस्थिति दर",
      "Academic Grade": "शैक्षणिक ग्रेड",
      "Upcoming Tasks": "आगामी कार्य",
      "Academic Standing": "शैक्षणिक स्थिति",
      "83 Present / 91 Total Days": "83 उपस्थित / 91 कुल दिन",
      "Annual Rank: Top 5%": "वार्षिक रैंक: शीर्ष 5%",
      "Math & Science due Friday": "गणित और विज्ञान शुक्रवार तक देय",
      "Go Live Voice": "लाइव वॉयस शुरू करें",
      "Switch": "बदलें",
      "Student Academic Assistant": "विद्यार्थी शैक्षणिक सहायक",
      "Parent Support Assistant": "अभिभावक सहायता सहायक",
      "Teacher Assistant": "शिक्षक सहायक",
      "Management Assistant": "प्रबंधन सहायक",
      "AI Academic Assistant": "एआई शैक्षणिक सहायक",
      "Today's Schedule": "आज की समय सारणी",
      "Homework & Assignments": "गृहकार्य और असाइनमेंट",
      "Attendance Record": "उपस्थिति रिकॉर्ड",
      "Academic Report Card": "शैक्षणिक रिपोर्ट कार्ड",
      "Fee Invoices & Receipts": "शुल्क चालान और रसीदें",
      "School Notices": "स्कूल सूचनाएं",
      "Class Attendance": "कक्षा उपस्थिति",
      "Grade Entry": "अंक प्रविष्टि",
      "Curriculum Planning": "पाठ्यक्रम योजना",
      "Executive Analytics": "कार्यकारी विश्लेषिकी",
      "Fee Reconciliation": "शुल्क समाधान",
      "Staff Roster": "स्टाफ सूची",
      "Campus Safety": "परिसर सुरक्षा",
      "Ask XYZ AI anything...": "XYZ AI से कुछ भी पूछें...",
      "Send": "भेजें",
      "Pay Fees Online": "ऑनलाइन शुल्क भरें",
      "Submit Leave Note": "अवकाश आवेदन जमा करें",
      "Talk to Teacher": "शिक्षक से बात करें",
      "Contact School Management": "स्कूल प्रबंधन से संपर्क करें",
      "Total Outstanding Dues": "कुल बकाया शुल्क",
      "Upcoming Exam Dates": "आगामी परीक्षा तिथियां",
      "Recent Absences": "हाल की अनुपस्थिति",
      "Active Students": "सक्रिय विद्यार्थी",
      "Faculty on Duty": "ड्यूटी पर शिक्षक",
      "Monthly Fee Collection": "मासिक शुल्क संग्रह",
      "Pending Escalations": "लंबित शिकायतें",
      "View Schedule": "समय सारणी देखें",
      "Check Absences": "अनुपस्थिति देखें",
      "Download Report": "रिपोर्ट डाउनलोड करें",
      "Pay Now": "अभी भुगतान करें"
    },
    gu: {
      "Attendance Rate": "હાજરીનો દર",
      "Academic Grade": "શૈક્ષણિક ગ્રેડ",
      "Upcoming Tasks": "આગામી કાર્યો",
      "Academic Standing": "શૈક્ષણિક સ્થિતિ",
      "83 Present / 91 Total Days": "83 હાજર / 91 કુલ દિવસો",
      "Annual Rank: Top 5%": "વાર્ષિક રેન્ક: ટોચના 5%",
      "Math & Science due Friday": "ગણિત અને વિજ્ઞાન શુક્રવાર સુધી",
      "Go Live Voice": "લાઈવ વોઈસ શરૂ કરો",
      "Switch": "યુઝર બદલો",
      "Student Academic Assistant": "વિદ્યાર્થી શૈક્ષણિક સહાયક",
      "Parent Support Assistant": "વાલી સહાયક સહાયક",
      "Teacher Assistant": "શિક્ષક સહાયક",
      "Management Assistant": "મેનેજમેન્ટ સહાયક",
      "AI Academic Assistant": "એઆઈ શૈક્ષણિક સહાયક",
      "Today's Schedule": "આજનું ટાઈમટેબલ",
      "Homework & Assignments": "ગૃહકાર્ય અને અસાઇનમેન્ટ્સ",
      "Attendance Record": "હાજરી પત્રક",
      "Academic Report Card": "પરિણામ પત્રક (Report Card)",
      "Fee Invoices & Receipts": "ફી ઇન્વૉઇસ અને રસીદો",
      "School Notices": "શાળાની નોટિસ",
      "Class Attendance": "વર્ગ હાજરી",
      "Grade Entry": "માર્ક્સ એન્ટ્રી",
      "Executive Analytics": "એક્ઝિક્યુટિવ એનાલિટિક્સ",
      "Fee Reconciliation": "ફી કલેક્શન વિગત",
      "Staff Roster": "સ્ટાફ રોસ્ટર",
      "Campus Safety": "કેમ્પસ સુરક્ષા",
      "Ask XYZ AI anything...": "XYZ AI ને કંઈ પણ પૂછો...",
      "Send": "મોકલો",
      "Pay Fees Online": "ઓનલાઇન ફી ભરો",
      "Submit Leave Note": "રજા માટે અરજી કરો",
      "Talk to Teacher": "શિક્ષક સાથે વાત કરો",
      "Contact School Management": "સ્કૂલ મેનેજમેન્ટનો સંપર્ક કરો",
      "Total Outstanding Dues": "કુલ બાકી ફી",
      "Upcoming Exam Dates": "પરીક્ષાની તારીખો",
      "Recent Absences": "તાજેતરની ગેરહાજરી",
      "Active Students": "કુલ વિદ્યાર્થીઓ",
      "Faculty on Duty": "હાજર શિક્ષકો",
      "Monthly Fee Collection": "માસિક ફી કલેક્શન",
      "Pending Escalations": "બાકી ફરિયાદો",
      "View Schedule": "ટાઈમટેબલ જુઓ",
      "Check Absences": "ગેરહાજરી જુઓ",
      "Download Report": "પરિણામ ડાઉનલોડ કરો",
      "Pay Now": "હમણાં ફી ભરો"
    },
    mr: {
      "Attendance Rate": "उपस्थितीचे प्रमाण",
      "Academic Grade": "शैक्षणिक श्रेणी",
      "Upcoming Tasks": "पुढील कामे",
      "Academic Standing": "शैक्षणिक प्रगती",
      "83 Present / 91 Total Days": "83 उपस्थित / 91 एकूण दिवस",
      "Go Live Voice": "थेट आवाज सुरू करा",
      "Switch": "बदला",
      "Student Academic Assistant": "विद्यार्थी शैक्षणिक सहाय्यक",
      "Parent Support Assistant": "पालक सहाय्यता",
      "Teacher Assistant": "शिक्षक सहाय्यक",
      "Management Assistant": "व्यवस्थापन सहाय्यक",
      "Today's Schedule": "आजचे वेळापत्रक",
      "Homework & Assignments": "गृहपाठ आणि स्वाध्याय",
      "Attendance Record": "उपस्थिती नोंद",
      "Academic Report Card": "प्रगती पुस्तक (Report Card)",
      "Fee Invoices & Receipts": "शुल्क पावती",
      "School Notices": "शालेय सूचना",
      "Class Attendance": "वर्ग उपस्थिती",
      "Ask XYZ AI anything...": "XYZ AI ला काहीही विचारा...",
      "Send": "पाठवा",
      "Pay Fees Online": "ऑनलाइन फी भरा",
      "Submit Leave Note": "रजेचा अर्ज सादर करा",
      "Talk to Teacher": "शिक्षकांशी बोला",
      "Contact School Management": "शाळा व्यवस्थापनाशी संपर्क साधा",
      "Total Outstanding Dues": "एकूण थकबाकी",
      "Upcoming Exam Dates": "परीक्षेच्या तारखा",
      "View Schedule": "वेळापत्रक पहा",
      "Pay Now": "आत्ताच भरा"
    },
    ta: {
      "Attendance Rate": "வருகை சதவீதம்",
      "Academic Grade": "கல்வி தரம்",
      "Upcoming Tasks": "வரவிருக்கும் பணிகள்",
      "Go Live Voice": "நேரலை குரல்",
      "Switch": "மாற்று",
      "Student Academic Assistant": "மாணவர் கல்வி உதவியாளர்",
      "Parent Support Assistant": "பெற்றோர் ஆதரவு உதவியாளர்",
      "Today's Schedule": "இன்றைய அட்டவணை",
      "Homework & Assignments": "வீட்டுப்பாடம்",
      "Attendance Record": "வருகைப் பதிவு",
      "Academic Report Card": "மதிப்பெண் பட்டியல்",
      "Fee Invoices & Receipts": "கட்டண ரசீதுகள்",
      "School Notices": "பள்ளி அறிவிப்புகள்",
      "Ask XYZ AI anything...": "XYZ AI-யிடம் கேளுங்கள்...",
      "Send": "அனுப்பு",
      "Pay Fees Online": "ஆன்லைனில் கட்டணம் செலுத்துக",
      "Submit Leave Note": "விடுப்பு விண்ணப்பம்",
      "Talk to Teacher": "ஆசிரியரிடம் பேசுங்கள்",
      "Contact School Management": "நிர்வாகத்தைத் தொடர்பு கொள்க",
      "Total Outstanding Dues": "மொத்த நிலுவைத் தொகை",
      "Pay Now": "இப்போது செலுத்துக"
    },
    hinglish: {
      "Attendance Rate": "Attendance Rate",
      "Academic Grade": "Academic Grade",
      "Upcoming Tasks": "Upcoming Tasks",
      "83 Present / 91 Total Days": "83 Present / 91 Total Days",
      "Go Live Voice": "Go Live Voice",
      "Switch": "Switch User",
      "Student Academic Assistant": "Student Academic Assistant",
      "Parent Support Assistant": "Parent Support Assistant",
      "Teacher Assistant": "Faculty Assistant",
      "Management Assistant": "Management Assistant",
      "Today's Schedule": "Aaj Ka Schedule",
      "Homework & Assignments": "Homework & Assignments",
      "Attendance Record": "Attendance Record",
      "Academic Report Card": "Report Card",
      "Fee Invoices & Receipts": "Fee Invoices & Receipts",
      "School Notices": "School Notices & Circulars",
      "Ask XYZ AI anything...": "XYZ AI se kuch bhi poochein...",
      "Send": "Send",
      "Pay Fees Online": "Pay Fees Online",
      "Submit Leave Note": "Submit Leave Note",
      "Talk to Teacher": "Teacher Se Baat Karein",
      "Contact School Management": "School Management Se Contact Karein",
      "Total Outstanding Dues": "Total Outstanding Dues",
      "Pay Now": "Pay Now"
    }
  };

  // Build bi-directional lookup map: any translated string -> canonical English key
  const CANONICAL_MAP = {};
  for (const [lang, dict] of Object.entries(UI_DICTIONARIES)) {
    for (const [canonicalKey, translatedText] of Object.entries(dict)) {
      CANONICAL_MAP[translatedText.trim().toLowerCase()] = canonicalKey;
      CANONICAL_MAP[canonicalKey.trim().toLowerCase()] = canonicalKey;
    }
  }

  function applyTranslations(lang) {
    const targetDict = UI_DICTIONARIES[lang] || UI_DICTIONARIES.en;

    // 1. Walk through all text nodes in the document body
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    const textReplacements = [];

    while (node = walker.nextNode()) {
      const parent = node.parentElement;
      if (!parent || parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE' || parent.tagName === 'CODE') {
        continue;
      }

      const trimmed = node.nodeValue.trim();
      if (!trimmed) continue;

      // Check if this parent or text node has an original key or matches in canonical map
      const lookupKey = (parent.dataset && parent.dataset.i18nKey) ? parent.dataset.i18nKey : CANONICAL_MAP[trimmed.toLowerCase()];
      if (lookupKey && targetDict[lookupKey]) {
        if (parent.dataset && !parent.dataset.i18nKey) {
          parent.dataset.i18nKey = lookupKey;
        }
        textReplacements.push({ node, newText: targetDict[lookupKey] });
      }
    }

    textReplacements.forEach(({ node, newText }) => {
      node.nodeValue = newText;
    });

    // 2. Update input / textarea placeholders
    document.querySelectorAll('input, textarea').forEach(el => {
      const p = el.placeholder ? el.placeholder.trim() : '';
      if (p) {
        const lookupKey = (el.dataset && el.dataset.i18nPlaceholder) ? el.dataset.i18nPlaceholder : CANONICAL_MAP[p.toLowerCase()];
        if (lookupKey && targetDict[lookupKey]) {
          if (!el.dataset.i18nPlaceholder) el.dataset.i18nPlaceholder = lookupKey;
          el.placeholder = targetDict[lookupKey];
        }
      }
    });

    // 3. Update global states and localStorage
    global.selectedLanguage = lang;
    localStorage.setItem('preferred_lang', lang);
    localStorage.setItem('xyz_language', lang);

    // 4. Update dropdown element value if needed
    const sel = document.getElementById('languageSelect');
    if (sel && sel.value !== lang) {
      sel.value = lang;
    }
  }

  function initI18n(defaultLang = 'en') {
    const saved = localStorage.getItem('preferred_lang') || localStorage.getItem('xyz_language') || defaultLang;
    global.selectedLanguage = saved;
    const sel = document.getElementById('languageSelect');
    if (sel) {
      sel.value = saved;
    }
    if (saved !== 'en') {
      setTimeout(() => applyTranslations(saved), 30);
    }
  }

  // Global exports
  global.SchoolI18n = {
    applyTranslations,
    initI18n,
    dictionaries: UI_DICTIONARIES
  };

  global.onLanguageChange = function(lang) {
    applyTranslations(lang);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => initI18n());
  } else {
    initI18n();
  }

})(typeof window !== 'undefined' ? window : this);
