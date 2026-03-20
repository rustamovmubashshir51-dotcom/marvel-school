import json
import io
import re
from bs4 import BeautifulSoup

replacements = {
    # Nav Links
    'Bosh Sahifa': 'Home',
    'Kurslar': 'Courses',
    'Afzalliklar': 'Features',
    'Jadval': 'Schedule',
    "O'qituvchilar": 'Teachers',
    "Ro'yxat": 'Register',
    
    # Hero Section
    "Professional <span>O'qituvchilar</span> bilan Zamonaviy Ta'lim": "Modern Education with <span>Professional Teachers</span>",
    "Marvel School - O'zbekistondagi eng ilg'or ta'lim markazi. Ingliz tili, Matematika va Rus tilini professional o'qituvchilardan o'rganing.": "Marvel School - The most advanced education center in Uzbekistan. Learn English, Mathematics, and Russian from professional teachers.",
    "<i class=\"fas fa-user-plus\"></i> Kursga Yozilish": "<i class=\"fas fa-user-plus\"></i> Enroll in Course",
    "<i class=\"fas fa-info-circle\"></i> Batafsil": "<i class=\"fas fa-info-circle\"></i> Learn More",
    
    # Courses Section
    "1-AB <span>YUQORI BOLGAN</span> YO'NALISHLAR": "TOP <span>TRENDING</span> COURSES",
    "Eng ko'p talab qilinadigan kurslar va ularning narxlari": "The most demanded courses and their prices",
    "IELTS va General English bosqichlari. Speaking va Grammar chuqurlashtirilgan holda. Native speaker bilan amaliyot.": "IELTS and General English levels. In-depth Speaking and Grammar. Practice with a Native speaker.",
    "<i class=\"fas fa-check-circle\"></i> Haftasiga 3 marta": "<i class=\"fas fa-check-circle\"></i> 3 times a week",
    "<i class=\"fas fa-check-circle\"></i> 1.5 soat / dars": "<i class=\"fas fa-check-circle\"></i> 1.5 hours / lesson",
    "<i class=\"fas fa-check-circle\"></i> Native speaker bilan": "<i class=\"fas fa-check-circle\"></i> With a Native speaker",
    "<i class=\"fas fa-check-circle\"></i> IELTS 7.5+ garant": "<i class=\"fas fa-check-circle\"></i> IELTS 7.5+ guaranteed",
    "Oylik to'lov": "Monthly fee",
    "500 000 <small>so'm</small>": "500 000 <small>UZS</small>",
    "Kursga yozilish <i class=\"fas fa-arrow-right\"></i>": "Enroll in Course <i class=\"fas fa-arrow-right\"></i>",
    
    "DTM va Xalqaro universitetlarga tayyorgarlik. Mantiqiy fikrlashni rivojlantirish. Masalalar yechish amaliyoti.": "Preparation for DTM and International universities. Development of logical thinking. Problem-solving practice.",
    "<i class=\"fas fa-check-circle\"></i> Testlar tahlili": "<i class=\"fas fa-check-circle\"></i> Test analysis",
    "<i class=\"fas fa-check-circle\"></i> Individual yondashuv": "<i class=\"fas fa-check-circle\"></i> Individual approach",
    
    "Rus Tili": "Russian Language",
    "So'zlashuv": "Conversational",
    "So'zlashuv va Grammatika. Qisqa muddatda erkin muloqot qilishni o'rganing. Amaliy mashg'ulotlar.": "Conversational and Grammar. Learn to communicate fluently in a short time. Practical lessons.",
    "<i class=\"fas fa-check-circle\"></i> Suhbat amaliyoti": "<i class=\"fas fa-check-circle\"></i> Conversation practice",
    "<i class=\"fas fa-check-circle\"></i> Kino va audio darslar": "<i class=\"fas fa-check-circle\"></i> Movie and audio lessons",
    
    # Features Section
    "Nega <span>Bizni Tanlashadi?</span>": "Why <span>Choose Us?</span>",
    "Marvel School afzalliklari va siz uchun yaratilgan imkoniyatlar": "Marvel School advantages and opportunities created for you",
    "Professional O'qituvchilar": "Professional Teachers",
    "5+ yillik tajribaga ega sertifikatlangan o'qituvchilar. Har bir o'qituvchi o'z sohasining mutaxassisi.": "Certified teachers with 5+ years of experience. Every teacher is an expert in their field.",
    "Zamonaviy Darsxonalar": "Modern Classrooms",
    "Smart doskalar, kompyuterlar va zamonaviy uskunalar bilan jihozlangan darsxonalar.": "Classrooms equipped with smart boards, computers, and modern equipment.",
    "Xalqaro Sertifikat": "International Certificate",
    "Kursni muvaffaqiyatli tamomlagan talabalar xalqaro darajadagi sertifikat oladilar.": "Students who successfully complete the course will receive an internationally recognized certificate.",
    
    # Schedule Section
    "Dars <span>Jadvali</span>": "Class <span>Schedule</span>",
    "Haftalik dars jadvali va o'qituvchilar taqsimoti": "Weekly class schedule and teacher allocation",
    "Kurs": "Course",
    "Dushanba": "Monday",
    "Chorshanba": "Wednesday",
    "Juma": "Friday",
    "O'qituvchi": "Teacher",
    "Ingliz Tili": "English Language",
    "Matematika": "Mathematics",
    "Kirill Alifbosi": "Cyrillic Alphabet",
    "Grammatika": "Grammar",
    "Nutq": "Speech",
    "<i class=\"fas fa-info-circle\"></i> Barcha kurslar haftasiga 3 marta, har bir dars 1.5 soat davom etadi": "<i class=\"fas fa-info-circle\"></i> All courses are 3 times a week, each lesson lasts 1.5 hours",
    
    # Teachers Section
    "Bizning <span>O'qituvchilar</span>": "Our <span>Teachers</span>",
    "Professional va tajribali o'qituvchilar jamoasi": "A team of professional and experienced teachers",
    "Ingliz Tili O'qituvchisi": "English Language Teacher",
    "<i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i> <span>5.0 (5 yillik tajriba)</span>": "<i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i> <span>5.0 (5 years experience)</span>",
    "IELTS 8.5 sohibi. 5 yildan ortiq tajriba. 200+ talaba imtihonlarni muvaffaqiyatli topshirgan.": "IELTS 8.5 holder. Over 5 years of experience. 200+ students successfully passed exams.",
    "Matematika O'qituvchisi": "Mathematics Teacher",
    "4.5 (4 yillik tajriba)": "4.5 (4 years experience)",
    "Toshkent Davlat Universiteti bitiruvchisi. Matematikadan oliy toifali o'qituvchi.": "Tashkent State University graduate. Top category mathematics teacher.",
    "Rus Tili O'qituvchisi": "Russian Language Teacher",
    "4.0 (3 yillik tajriba)": "4.0 (3 years experience)",
    "Rus tili - ona tili. O'zbekiston Respublikasida 3 yildan beri rus tili o'qitadi.": "Russian is his native language. Has been teaching Russian in the Republic of Uzbekistan for 3 years.",
    
    # Registration Section
    "Kursga <span style=\"color: var(--accent);\">Ro'yxatdan O'tish</span>": "Course <span style=\"color: var(--accent);\">Registration</span>",
    "Hoziroq ro'yxatdan o'ting va 20% chegirmaga ega bo'ling": "Register now and get a 20% discount",
    "Ismingiz *": "Your Name *",
    "Ism familiyangizni kiriting": "Enter your full name",
    "Telefon Raqamingiz *": "Phone Number *",
    "Email Manzilingiz": "Email Address",
    "Tanlagan Kursingiz *": "Selected Course *",
    "Kursni tanlang": "Select a course",
    "Ingliz Tili - 500 000 so'm/oy": "English Language - 500 000 UZS/month",
    "Matematika - 500 000 so'm/oy": "Mathematics - 500 000 UZS/month",
    "Rus Tili - 500 000 so'm/oy": "Russian Language - 500 000 UZS/month",
    "Qo'shimcha Izoh": "Additional Comments",
    "Savollaringiz yoki talablaringiz...": "Your questions or requirements...",
    "Men <a href=\"#\" style=\"color: var(--accent);\">shartlar va qoidalar</a> bilan tanishdim va roziman": "I have read and agree to the <a href=\"#\" style=\"color: var(--accent);\">terms and conditions</a>",
    "<i class=\"fas fa-paper-plane\"></i> Ro'yxatdan O'tish": "<i class=\"fas fa-paper-plane\"></i> Register",
    
    # Footer Section
    "O'zbekistondagi eng yaxshi professional ta'lim markazi. 5 yildan ortiq tajriba, 1000+ bitiruvchi, 20+ professional o'qituvchi.": "The best professional education center in Uzbekistan. Over 5 years of experience, 1000+ graduates, 20+ professional teachers.",
    "Aloqa": "Contact",
    "<i class=\"fas fa-map-marker-alt\" style=\"margin-right: 8px;\"></i> Toshkent, Yunusobod": "<i class=\"fas fa-map-marker-alt\" style=\"margin-right: 8px;\"></i> Tashkent, Yunusabad",
    "<i class=\"fas fa-clock\" style=\"margin-right: 8px;\"></i> Dush-Jum: 9:00 - 21:00": "<i class=\"fas fa-clock\" style=\"margin-right: 8px;\"></i> Mon-Fri: 9:00 - 21:00",
    "Barcha huquqlar himoyalangan.": "All rights reserved.",
    "DTM tayyorgarlik": "DTM Preparation",
}

with io.open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

def normalize(s):
    return re.sub(r'\\s+', ' ', str(s)).strip()

# Add i18n to exact tags
for tags in soup.find_all(True):
    # Only process tags that don't have block children to target leaves or small wrappers
    if tags.name not in ['script', 'style', 'html', 'head', 'body', 'ul', 'div', 'section', 'nav', 'table', 'tbody', 'thead', 'tr']:
        content_norm = normalize(tags.decode_contents())
        for uz, en in replacements.items():
            en_norm = normalize(en)
            if content_norm == en_norm:
                tags['data-i18n-en'] = en
                tags['data-i18n-uz'] = uz
                
                # Replace children to revert to UZ
                new_tag = BeautifulSoup(uz, 'html.parser')
                tags.clear()
                for c in new_tag.contents:
                    tags.append(c)
                break

# Special handling for title
title_tag = soup.find('title')
if title_tag and 'Professional Education Center' in title_tag.string:
    title_tag['data-i18n-en'] = "Marvel School - Professional Education Center"
    title_tag['data-i18n-uz'] = "Marvel School - Professional Ta'lim Markazi"
    title_tag.string = "Marvel School - Professional Ta'lim Markazi"

# Special handling for inputs placeholders
for inp in soup.find_all('input', placeholder=True):
    ph = inp['placeholder']
    for uz, en in replacements.items():
        if ph == en:
            inp['data-i18n-ph-en'] = en
            inp['data-i18n-ph-uz'] = uz
            inp['placeholder'] = uz
            break

for ta in soup.find_all('textarea', placeholder=True):
    ph = ta['placeholder']
    for uz, en in replacements.items():
        if ph == en:
            ta['data-i18n-ph-en'] = en
            ta['data-i18n-ph-uz'] = uz
            ta['placeholder'] = uz
            break

# Change HTML lang back to uz
html_tag = soup.find('html')
if html_tag:
    html_tag['lang'] = 'uz'

# Insert the Language Switcher UI into header-container
header_container = soup.find('div', class_='header-container')
if header_container:
    # Build Lang switcher HTML
    lang_switcher_html = """
    <div class="lang-switcher" id="langSwitcher" style="position: relative; margin-left: 15px; display: flex; align-items: center; cursor: pointer; color: white; font-weight: 500; font-size: 0.95rem;">
        <span class="active-lang" style="display: flex; align-items: center; gap: 5px;">
            <img id="activeLangImg" src="https://flagcdn.com/w20/uz.png" alt="UZ" style="width: 20px; border-radius: 2px;">
            <span id="activeLangText">UZ</span>
            <i class="fas fa-chevron-down" style="font-size: 0.7rem;"></i>
        </span>
        <div class="lang-dropdown" style="display: none; position: absolute; top: 100%; right: 0; background: var(--card); color: var(--text); border-radius: 8px; box-shadow: 0 4px 15px var(--shadow); overflow: hidden; margin-top: 10px; min-width: 100px; z-index: 1000;">
            <div class="lang-option" data-lang="uz" style="padding: 10px 15px; display: flex; align-items: center; gap: 8px; transition: background 0.2s;">
                <img src="https://flagcdn.com/w20/uz.png" alt="UZ" style="width: 20px; border-radius: 2px;"> UZ
            </div>
            <div class="lang-option" data-lang="en" style="padding: 10px 15px; display: flex; align-items: center; gap: 8px; transition: background 0.2s;">
                <img src="https://flagcdn.com/w20/gb.png" alt="EN" style="width: 20px; border-radius: 2px;"> EN
            </div>
        </div>
    </div>
    """
    lang_soup = BeautifulSoup(lang_switcher_html, 'html.parser')
    
    # Insert switcher right before the theme toggle
    theme_toggle = header_container.find('button', id='themeToggle')
    if theme_toggle:
        theme_toggle.insert_before(lang_soup)
    else:
        header_container.append(lang_soup)

# Add custom styling for the dropdown
style_tag = soup.find('style')
if style_tag:
    style_content = style_tag.string
    if ".lang-option:hover" not in style_content:
        style_content += "\\n.lang-option:hover { background: rgba(26, 35, 126, 0.05); }\\n"
        style_tag.string = style_content

# Append the JavaScript logic to the bottom of body
body_tag = soup.find('body')
if body_tag:
    script_html = """
    <script>
        // LANGUAGE SWITCHER
        const langSwitcher = document.getElementById('langSwitcher');
        const langDropdown = langSwitcher.querySelector('.lang-dropdown');
        const langOptions = langSwitcher.querySelectorAll('.lang-option');
        const activeLangImg = document.getElementById('activeLangImg');
        const activeLangText = document.getElementById('activeLangText');
        
        let currentLang = localStorage.getItem('language') || 'uz';
        
        function applyLanguage(lang) {
            currentLang = lang;
            document.documentElement.setAttribute('lang', lang);
            localStorage.setItem('language', lang);
            
            // Update UI
            if(lang === 'uz') {
                activeLangImg.src = 'https://flagcdn.com/w20/uz.png';
                activeLangText.innerText = 'UZ';
            } else {
                activeLangImg.src = 'https://flagcdn.com/w20/gb.png';
                activeLangText.innerText = 'EN';
            }
            
            // Translate tags
            document.querySelectorAll('[data-i18n-en]').forEach(el => {
                const enStr = el.getAttribute('data-i18n-en');
                const uzStr = el.getAttribute('data-i18n-uz');
                el.innerHTML = lang === 'en' ? enStr : uzStr;
            });
            
            // Translate placeholders
            document.querySelectorAll('[data-i18n-ph-en]').forEach(el => {
                const enStr = el.getAttribute('data-i18n-ph-en');
                const uzStr = el.getAttribute('data-i18n-ph-uz');
                el.placeholder = lang === 'en' ? enStr : uzStr;
            });
            
            // Form success JS message fix (dirty patch)
            if (window.submitBtnOriginalText) {
                // If the language changes, we reset the translation keys in js if needed
            }
        }
        
        // Initial apply
        applyLanguage(currentLang);
        
        langSwitcher.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = langDropdown.style.display === 'block';
            langDropdown.style.display = isVisible ? 'none' : 'block';
        });
        
        document.addEventListener('click', () => {
            langDropdown.style.display = 'none';
        });
        
        langOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                const selectedLang = option.getAttribute('data-lang');
                applyLanguage(selectedLang);
            });
        });
    </script>
    """
    script_soup = BeautifulSoup(script_html, 'html.parser')
    body_tag.append(script_soup)

# Save the updated file safely
with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
