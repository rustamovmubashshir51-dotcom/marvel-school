import json
import io

replacements = {
    # Head
    '<html lang="uz" data-theme="light">': '<html lang="en" data-theme="light">',
    "Professional Ta'lim Markazi": "Professional Education Center",
    
    # Nav Links
    'Bosh Sahifa': 'Home',
    'Kurslar': 'Courses',
    'Afzalliklar': 'Features',
    'Jadval': 'Schedule',
    "O'qituvchilar": 'Teachers',
    "Ro'yxat": 'Register',
    
    # Hero Section
    "<h1>Professional <span>O'qituvchilar</span> bilan Zamonaviy Ta'lim</h1>": "<h1>Modern Education with <span>Professional Teachers</span></h1>",
    "Marvel School - O'zbekistondagi eng ilg'or ta'lim markazi. Ingliz tili, Matematika va Rus tilini professional o'qituvchilardan o'rganing.": "Marvel School - The most advanced education center in Uzbekistan. Learn English, Mathematics, and Russian from professional teachers.",
    "Kursga Yozilish": "Enroll in Course",
    "Batafsil": "Learn More",
    
    # Courses Section
    "1-AB <span>YUQORI BOLGAN</span> YO'NALISHLAR": "TOP <span>TRENDING</span> COURSES",
    "Eng ko'p talab qilinadigan kurslar va ularning narxlari": "The most demanded courses and their prices",
    "IELTS va General English bosqichlari. Speaking va Grammar chuqurlashtirilgan holda. Native speaker bilan amaliyot.": "IELTS and General English levels. In-depth Speaking and Grammar. Practice with a Native speaker.",
    "Haftasiga 3 marta": "3 times a week",
    "1.5 soat / dars": "1.5 hours / lesson",
    "Native speaker bilan": "With a Native speaker",
    "IELTS 7.5+ garant": "IELTS 7.5+ guaranteed",
    "Oylik to'lov": "Monthly fee",
    "500 000 <small>so'm</small>": "500 000 <small>UZS</small>",
    "Kursga yozilish": "Enroll in Course",
    
    "DTM va Xalqaro universitetlarga tayyorgarlik. Mantiqiy fikrlashni rivojlantirish. Masalalar yechish amaliyoti.": "Preparation for DTM and International universities. Development of logical thinking. Problem-solving practice.",
    "Testlar tahlili": "Test analysis",
    "Individual yondashuv": "Individual approach",
    
    "Rus Tili": "Russian Language",
    "So'zlashuv": "Conversational",
    "So'zlashuv va Grammatika. Qisqa muddatda erkin muloqot qilishni o'rganing. Amaliy mashg'ulotlar.": "Conversational and Grammar. Learn to communicate fluently in a short time. Practical lessons.",
    "Suhbat amaliyoti": "Conversation practice",
    "Kino va audio darslar": "Movie and audio lessons",
    
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
    "Barcha kurslar haftasiga 3 marta, har bir dars 1.5 soat davom etadi": "All courses are 3 times a week, each lesson lasts 1.5 hours",
    
    # Teachers Section
    "Bizning <span>O'qituvchilar</span>": "Our <span>Teachers</span>",
    "Professional va tajribali o'qituvchilar jamoasi": "A team of professional and experienced teachers",
    "Ingliz Tili O'qituvchisi": "English Language Teacher",
    "5.0 (5 yillik tajriba)": "5.0 (5 years experience)",
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
    "Ro'yxatdan O'tish": "Register",
    
    # Footer Section
    "O'zbekistondagi eng yaxshi professional ta'lim markazi. 5 yildan ortiq tajriba, 1000+ bitiruvchi, 20+ professional o'qituvchi.": "The best professional education center in Uzbekistan. Over 5 years of experience, 1000+ graduates, 20+ professional teachers.",
    "Aloqa": "Contact",
    "Toshkent, Yunusobod": "Tashkent, Yunusabad",
    "Dush-Jum: 9:00 - 21:00": "Mon-Fri: 9:00 - 21:00",
    "Barcha huquqlar himoyalangan.": "All rights reserved.",
    "DTM tayyorgarlik": "DTM Preparation",
    
    # Scripts
    "Muvaffaqiyatli!": "Successful!",
    "tanlangan": "selected",
    "Rahmat, ${name}! Siz ${courseNames[course] || 'tanlangan'} kursiga ro'yxatdan o'tdingiz.\\nTez orada siz bilan bog'lanamiz.": "Thank you, ${name}! You have registered for the ${courseNames[course] || 'selected'} course.\\nWe will contact you shortly."
}

with io.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for uz, en in replacements.items():
    html = html.replace(uz, en)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
