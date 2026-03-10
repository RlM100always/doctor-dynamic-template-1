from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    SiteSettings, TickerMessage, TrustChip, HeroDegree, AboutHighlight,
    Qualification, Certificate, Chamber, Service, FeeItem, FeeInfo,
    AppointmentSlot, Review, RatingBar, Video, BlogPost, MediaCoverage,
    TeamMember, FAQ
)


class Command(BaseCommand):
    help = 'Seed the database with initial data from the original static website'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        # ── SITE SETTINGS ──────────────────────────────────────────────────────
        site, _ = SiteSettings.objects.get_or_create(pk=1)
        site.doctor_name = 'ডাঃ সানজিদা ইসলাম চৌধুরী'
        site.doctor_name_en = 'Dr. Sanjida Islam Chowdhury'
        site.specialty = 'গাইনী ও প্রসূতি বিশেষজ্ঞ'
        site.degrees = 'MBBS · FCPS · MRCOG (UK)'
        site.bio = 'ঢাকা মেডিকেল কলেজ হাসপাতালের সিনিয়র কনসালটেন্ট। মা ও শিশুর স্বাস্থ্য সেবায় ২২ বছরের নিবেদিত অভিজ্ঞতা। রয়্যাল কলেজ অব অবস্টেট্রিশিয়ানস, লন্ডন থেকে MRCOG ডিগ্রিধারী। ডাঃ সানজিদা ইসলাম চৌধুরী বাংলাদেশের একজন শীর্ষস্থানীয় গাইনোকোলজিস্ট ও প্রসূতি বিশেষজ্ঞ। গত ২২ বছরে তিনি ৮,০০০-এরও বেশি সফল প্রসব পরিচালনা করেছেন।'
        site.phone = '০১৮১১-২২৩৩৪৪'
        site.phone_raw = '+8801811223344'
        site.whatsapp = '8801811223344'
        site.email = 'dr.sanjida@example.com'
        site.facebook_url = 'https://facebook.com/dr.sanjida.bd'
        site.profile_photo_url = 'https://cdn.sasthyaseba.com/doctors/7410/xoWEh5iyzT9wpngIPNnKbQQiN5AnbUCE8y2hJYpv/dr-sanjida-hossain.jpg'
        site.years_experience = 22
        site.successful_deliveries = 8000
        site.google_rating = 4.8
        site.google_review_count = 650
        site.research_papers = 18
        site.booking_fee = 300
        site.bkash_number = '০১৮১১-২২৩৩৪৪'
        site.nagad_number = '০১৮১১-২২৩৩৪৪'
        site.rocket_number = '০১৮১১২২৩৩৪৪৭'
        site.maps_link = 'https://maps.google.com/?q=মিরপুর+ঢাকা'
        site.meta_title = 'ডাঃ সানজিদা ইসলাম চৌধুরী | গাইনী ও প্রসূতি বিশেষজ্ঞ'
        site.save()
        self.stdout.write('  ✅ Site settings')

        # ── TICKERS ────────────────────────────────────────────────────────────
        TickerMessage.objects.all().delete()
        tickers = [
            'শুক্রবার চেম্বার বন্ধ থাকবে',
            'অ্যাপয়েন্টমেন্ট: ০১৮১১-২২৩৩৪৪',
            'অনলাইন কনসালটেশন এখন উপলব্ধ',
            'নতুন মাতৃত্ব প্যাকেজ চালু',
        ]
        for i, msg in enumerate(tickers):
            TickerMessage.objects.create(message=msg, order=i)
        self.stdout.write('  ✅ Tickers')

        # ── TRUST CHIPS ────────────────────────────────────────────────────────
        TrustChip.objects.all().delete()
        chips = [
            ('fas fa-award', 'BMA Award 2024'),
            ('fas fa-globe', 'RCOG Fellow, London'),
            ('fas fa-hospital', 'DMCH Senior Consultant'),
        ]
        for i, (icon, text) in enumerate(chips):
            TrustChip.objects.create(icon_class=icon, text=text, order=i)
        self.stdout.write('  ✅ Trust chips')

        # ── HERO DEGREES ───────────────────────────────────────────────────────
        HeroDegree.objects.all().delete()
        for i, label in enumerate(['MBBS', 'FCPS (গাইনী)', 'MRCOG (UK)']):
            HeroDegree.objects.create(label=label, order=i)
        self.stdout.write('  ✅ Hero degrees')

        # ── ABOUT HIGHLIGHTS ───────────────────────────────────────────────────
        AboutHighlight.objects.all().delete()
        highlights = [
            ('fas fa-graduation-cap', 'MRCOG ডিগ্রি', 'রয়্যাল কলেজ অব অবস্টেট্রিশিয়ানস, লন্ডন'),
            ('fas fa-microscope', 'গবেষণাপত্র', '১৮টি আন্তর্জাতিক জার্নালে প্রকাশিত'),
            ('fas fa-award', 'বিএমএ অ্যাওয়ার্ড ২০২৪', 'শ্রেষ্ঠ গাইনী বিশেষজ্ঞ পুরস্কার'),
        ]
        for i, (icon, title, desc) in enumerate(highlights):
            AboutHighlight.objects.create(icon_class=icon, title=title, description=desc, order=i)
        self.stdout.write('  ✅ About highlights')

        # ── QUALIFICATIONS ─────────────────────────────────────────────────────
        Qualification.objects.all().delete()
        quals = [
            ('১৯৯৯', 'MBBS', 'ঢাকা মেডিকেল কলেজ, ঢাকা বিশ্ববিদ্যালয়', 'fas fa-graduation-cap', 'degree'),
            ('২০০৭', 'FCPS (গাইনী ও প্রসূতি)', 'বাংলাদেশ কলেজ অব ফিজিশিয়ানস অ্যান্ড সার্জনস', 'fas fa-stethoscope', 'postgrad'),
            ('২০১০', 'MRCOG (UK)', 'রয়্যাল কলেজ অব অবস্টেট্রিশিয়ানস অ্যান্ড গাইনোকোলজিস্টস, লন্ডন', 'fas fa-globe-europe', 'international'),
            ('২০১২–১৩', 'ফেলোশিপ প্রশিক্ষণ', 'কিং এডওয়ার্ড মেমোরিয়াল হাসপাতাল, পার্থ, অস্ট্রেলিয়া', 'fas fa-hospital-alt', 'training'),
            ('২০১৫–বর্তমান', 'সিনিয়র কনসালটেন্ট', 'ঢাকা মেডিকেল কলেজ হাসপাতাল, গাইনী ও প্রসূতি বিভাগ', 'fas fa-chalkboard-teacher', 'current'),
        ]
        for i, (year, degree, inst, icon, etype) in enumerate(quals):
            Qualification.objects.create(year=year, degree=degree, institution=inst, icon_class=icon, entry_type=etype, order=i)
        self.stdout.write('  ✅ Qualifications')

        # ── CERTIFICATES ───────────────────────────────────────────────────────
        Certificate.objects.all().delete()
        certs = [
            ('01', 'fas fa-scroll', 'এফসিপিএস সনদ', 'বাংলাদেশ কলেজ অব ফিজিশিয়ানস অ্যান্ড সার্জনস — গাইনোকোলজি ও অবস্টেট্রিক্স', 'সনদ যাচাই করুন', 'https://www.bcps.edu.bd/', False),
            ('02', 'fas fa-crown', 'MRCOG (UK)', 'রয়্যাল কলেজ অব অবস্টেট্রিশিয়ানস অ্যান্ড গাইনোকোলজিস্টস, লন্ডন, যুক্তরাজ্য', 'RCOG যাচাই করুন', 'https://www.rcog.org.uk/', True),
            ('03', 'fas fa-university', 'MBBS সনদ', 'ঢাকা মেডিকেল কলেজ, ঢাকা বিশ্ববিদ্যালয় — ১৯৯৯ সালে প্রথম শ্রেণিতে উত্তীর্ণ', 'প্রতিষ্ঠান দেখুন', 'https://www.dmch.gov.bd/', False),
            ('04', 'fas fa-baby', 'MFM ফেলোশিপ', 'ম্যাটারনাল-ফেটাল মেডিসিনে বিশেষ ফেলোশিপ প্রশিক্ষণ, অস্ট্রেলিয়া', 'বিস্তারিত দেখুন', 'https://www.rcog.org.uk/', False),
            ('05', 'fas fa-award', 'FACOG (সম্মানসূচক)', 'আমেরিকান কলেজ অব অবস্টেট্রিশিয়ানস অ্যান্ড গাইনোকোলজিস্টস ফেলোশিপ', 'ACOG যাচাই করুন', 'https://www.acog.org/', True),
            ('06', 'fas fa-id-card-alt', 'বিএমডিসি নিবন্ধন', 'বাংলাদেশ মেডিকেল অ্যান্ড ডেন্টাল কাউন্সিল — নিবন্ধন নং: A-৪৮৭২১', 'নিবন্ধন যাচাই করুন', 'http://bmdc.org.bd/', False),
        ]
        for i, (num, icon, title, desc, link_text, link_url, is_amber) in enumerate(certs):
            Certificate.objects.create(number=num, icon_class=icon, title=title, description=desc, link_text=link_text, link_url=link_url, is_amber=is_amber, order=i)
        self.stdout.write('  ✅ Certificates')

        # ── CHAMBERS ───────────────────────────────────────────────────────────
        Chamber.objects.all().delete()
        Chamber.objects.create(badge='প্রধান চেম্বার', name='মিরপুর চেম্বার', area='ঢাকা – মিরপুর',
            address='বাড়ি ১২, রোড ৪, সেকশন ১০, মিরপুর, ঢাকা ১২১৬',
            schedule='বিকাল ৫ টা – রাত ৯ টা (শনি–বৃহঃ)', closed_days='শুক্রবার: বন্ধ',
            phone='০১৮১১-২২৩৩৪৪', phone_raw='+8801811223344', icon_class='fas fa-hospital-alt', order=0)
        Chamber.objects.create(badge='সকালের চেম্বার', name='মগবাজার চেম্বার', area='ঢাকা – মগবাজার',
            address='বাড়ি ৩৫, ওয়্যারলেস রোড, মগবাজার, ঢাকা ১২১৭',
            schedule='সকাল ৯ টা – দুপুর ১ টা (শনি, সোম, বুধ)', closed_days='মঙ্গল, বৃহঃ, শুক্র: বন্ধ',
            phone='০১৯২২-৩৩৪৪৫৫', phone_raw='+8801922334455', icon_class='fas fa-clinic-medical', is_amber=True, order=1)
        self.stdout.write('  ✅ Chambers')

        # ── SERVICES ───────────────────────────────────────────────────────────
        Service.objects.all().delete()
        services = [
            ('fas fa-baby-carriage', 'স্বাভাবিক প্রসব', 'জটিলতামুক্ত প্রাকৃতিক প্রসব পরিচালনায় বিশেষজ্ঞ।', False),
            ('fas fa-cut', 'সিজারিয়ান বিভাগ', 'উচ্চঝুঁকিপূর্ণ প্রসবে সিজারিয়ান ও ল্যাপারোস্কোপিক সার্জারি।', False),
            ('fas fa-heartbeat', 'উচ্চঝুঁকি গর্ভাবস্থা', 'ডায়াবেটিস, উচ্চ রক্তচাপ ও একাধিক গর্ভধারণে বিশেষজ্ঞ পরিচর্যা।', True),
            ('fas fa-baby', 'গর্ভকালীন সেবা', 'সম্পূর্ণ প্রসবপূর্ব পরিচর্যা, আলট্রাসনোগ্রাফি ও ভ্রূণ পর্যবেক্ষণ।', False),
            ('fas fa-female', 'গাইনোকোলজিক্যাল সমস্যা', 'মাসিকের সমস্যা, এন্ডোমেট্রিওসিস, ফাইব্রয়েড ও পিসিওএস চিকিৎসা।', False),
            ('fas fa-dna', 'বন্ধ্যাত্ব চিকিৎসা', 'দম্পতির প্রজনন স্বাস্থ্য মূল্যায়ন, হরমোন থেরাপি ও আইভিএফ পরামর্শ।', False),
            ('fas fa-microscope', 'ক্যান্সার স্ক্রিনিং', 'জরায়ু মুখের ক্যান্সার স্ক্রিনিং, কলপোস্কোপি ও প্যাপ স্মিয়ার।', False),
            ('fas fa-laptop-medical', 'অনলাইন কনসাল্ট', 'ঘরে বসেই ভিডিও কলে গাইনী পরামর্শ। প্রেসক্রিপশন ইমেইলে পাঠানো হবে।', False),
        ]
        for i, (icon, title, desc, featured) in enumerate(services):
            Service.objects.create(icon_class=icon, title=title, description=desc, is_featured=featured, order=i)
        self.stdout.write('  ✅ Services')

        # ── FEES ───────────────────────────────────────────────────────────────
        FeeItem.objects.all().delete()
        fees = [
            ('প্রথম দর্শন ফি', 1200, 'সম্পূর্ণ পরীক্ষা ও ব্যবস্থাপত্র', False),
            ('ফলোআপ ফি', 600, 'পূর্ববর্তী রোগীদের পরবর্তী ভিজিট', False),
            ('অনলাইন কনসাল্ট', 800, 'ভিডিও কল + ডিজিটাল প্রেসক্রিপশন', False),
            ('প্রসূতি প্যাকেজ', 5000, '৯ মাসব্যাপী সম্পূর্ণ গর্ভকালীন সেবা', True),
            ('রিপোর্ট রিভিউ', 400, 'টেস্ট রিপোর্ট দেখা ও পরামর্শ', False),
            ('আলট্রাসনোগ্রাফি পরামর্শ', 300, 'আলট্রাসনোগ্রাফি রিপোর্ট ব্যাখ্যা', False),
        ]
        for i, (name, fee, inc, featured) in enumerate(fees):
            FeeItem.objects.create(service_name=name, fee=fee, includes=inc, is_featured=featured, order=i)
        self.stdout.write('  ✅ Fee items')

        # ── APPOINTMENT SLOTS ──────────────────────────────────────────────────
        AppointmentSlot.objects.all().delete()
        slots = [
            ('সকাল ৯:০০ টা', 'সকাল ৯:০০ টা'),
            ('সকাল ১০:০০ টা', 'সকাল ১০:০০ টা'),
            ('সকাল ১১:০০ টা', 'সকাল ১১:০০ টা'),
            ('বিকাল ৫:০০ টা', 'বিকাল ৫:০০ টা'),
            ('বিকাল ৬:০০ টা', 'বিকাল ৬:০০ টা'),
            ('সন্ধ্যা ৭:০০ টা', 'সন্ধ্যা ৭:০০ টা'),
        ]
        for i, (label, value) in enumerate(slots):
            AppointmentSlot.objects.create(label=label, value=value, order=i)
        self.stdout.write('  ✅ Appointment slots')

        # ── REVIEWS ────────────────────────────────────────────────────────────
        Review.objects.all().delete()
        reviews = [
            ('ফারজানা আক্তার', 5, 'ডাঃ সানজিদা ম্যাডাম আমার প্রথম গর্ভধারণে অসাধারণ সহায়তা করেছেন। তাঁর যত্ন ও পেশাদারিত্ব অতুলনীয়।', True, False),
            ('মনিরা বেগম', 5, 'উচ্চঝুঁকিপূর্ণ গর্ভাবস্থায় তাঁর দক্ষতা ও মনোযোগের কারণেই আজ আমার সুস্থ সন্তান আছে। কৃতজ্ঞতার ভাষা নেই।', True, True),
            ('রিনা সুলতানা', 5, 'পিসিওএস সমস্যায় ডাঃ সানজিদার চিকিৎসায় ৬ মাসে অনেক উন্নতি হয়েছে। অনলাইন ফলোআপও দারুণ কাজ করে।', True, False),
            ('সালমা খানম', 5, 'তৃতীয় সন্তানের সময় অনেক জটিলতা ছিল। ডাক্তার সানজিদার কারণেই মা ও শিশু দুজনেই সুস্থ আছি।', True, False),
        ]
        for i, (name, rating, text, verified, accent) in enumerate(reviews):
            Review.objects.create(reviewer_name=name, rating=rating, review_text=text, is_verified=verified, is_accent=accent, order=i)
        self.stdout.write('  ✅ Reviews')

        # ── RATING BARS ────────────────────────────────────────────────────────
        RatingBar.objects.all().delete()
        for stars, pct in [(5, 82), (4, 12), (3, 4), (2, 2)]:
            RatingBar.objects.create(stars=stars, percentage=pct)
        self.stdout.write('  ✅ Rating bars')

        # ── VIDEOS ─────────────────────────────────────────────────────────────
        Video.objects.all().delete()
        videos = [
            ('https://www.youtube.com/embed/nICE29D_27A', 'প্রথম ত্রৈমাসিকে সঠিক যত্ন কীভাবে নেবেন', 'গর্ভাবস্থা'),
            ('https://www.youtube.com/embed/JF6Vfl6qz8o', 'পিসিওএস থেকে স্বাভাবিক গর্ভধারণ — সম্ভব?', 'পিসিওএস'),
            ('https://www.youtube.com/embed/m5U37nJ3V0k', 'সিজার নাকি স্বাভাবিক প্রসব — সঠিক সিদ্ধান্ত কীভাবে নেবেন', 'প্রসব'),
        ]
        for i, (url, title, tag) in enumerate(videos):
            Video.objects.create(youtube_url=url, title=title, tag=tag, order=i)
        self.stdout.write('  ✅ Videos')

        # ── BLOG POSTS ─────────────────────────────────────────────────────────
        BlogPost.objects.all().delete()
        posts = [
            ('fas fa-baby', 'গর্ভাবস্থা', 'গর্ভাবস্থায় কী খাবেন, কী এড়িয়ে চলবেন?',
             'সুষম পুষ্টি, নিরাপদ ব্যায়াম এবং মানসিক স্বাস্থ্য — গর্ভকালীন সময়ে এই তিনটি বিষয়ে সঠিক জ্ঞান থাকা অত্যন্ত জরুরি।',
             '<p>গর্ভাবস্থায় সঠিক পুষ্টি মায়ের ও শিশুর সুস্বাস্থ্যের জন্য অপরিহার্য।</p><h3>কী খাবেন?</h3><ul><li>প্রচুর শাকসবজি ও ফলমূল</li><li>আয়রনসমৃদ্ধ খাবার</li><li>ক্যালসিয়ামসমৃদ্ধ দুগ্ধজাত পণ্য</li><li>পর্যাপ্ত পানি</li></ul><h3>কী এড়িয়ে চলবেন?</h3><ul><li>কাঁচা মাছ বা মাংস</li><li>অতিরিক্ত ক্যাফেইন</li><li>মদ্যপান ও ধূমপান</li></ul>', True),
            ('fas fa-female', 'মহিলা স্বাস্থ্য', 'পিসিওএস কী এবং কীভাবে নিয়ন্ত্রণ করবেন?',
             'পলিসিস্টিক ওভারি সিনড্রোমের লক্ষণ, কারণ ও আধুনিক চিকিৎসা পদ্ধতি।',
             '<p>পিসিওএস (Polycystic Ovary Syndrome) বাংলাদেশে নারীদের মধ্যে একটি সাধারণ হরমোনজনিত সমস্যা।</p><h3>লক্ষণসমূহ</h3><ul><li>অনিয়মিত মাসিক</li><li>ওজন বৃদ্ধি</li><li>মুখে অতিরিক্ত লোম</li></ul><h3>চিকিৎসা</h3><p>সঠিক খাদ্যাভ্যাস, ব্যায়াম ও প্রয়োজনে ওষুধের মাধ্যমে পিসিওএস নিয়ন্ত্রণ করা সম্ভব।</p>', False),
            ('fas fa-heartbeat', 'জরুরি তথ্য', 'প্রিক্ল্যাম্পসিয়া: নীরব বিপদ চেনার উপায়',
             'উচ্চ রক্তচাপজনিত গর্ভাবস্থার জটিলতা সময়মতো চিহ্নিত করুন।',
             '<p>প্রিক্ল্যাম্পসিয়া গর্ভাবস্থার একটি গুরুতর জটিলতা যা সময়মতো চিহ্নিত না হলে মারাত্মক হতে পারে।</p><h3>সতর্কতার লক্ষণ</h3><ul><li>হঠাৎ রক্তচাপ বৃদ্ধি</li><li>প্রস্রাবে প্রোটিন</li><li>হাত-পায়ে অতিরিক্ত ফোলা</li><li>মাথাব্যথা ও চোখে ঝাপসা দেখা</li></ul>', False),
        ]
        for i, (icon, cat, title, excerpt, content, is_large) in enumerate(posts):
            BlogPost.objects.create(icon_class=icon, category=cat, title=title, excerpt=excerpt, full_content=content, is_large=is_large, order=i)
        self.stdout.write('  ✅ Blog posts')

        # ── MEDIA COVERAGE ─────────────────────────────────────────────────────
        MediaCoverage.objects.all().delete()
        media = [
            ('fas fa-newspaper', 'প্রথম আলো', 'গাইনী বিশেষজ্ঞ হিসেবে সাক্ষাৎকার — "মায়েদের স্বাস্থ্য সচেতনতা জরুরি"', False),
            ('fas fa-tv', 'সময় টিভি', 'লাইভ টকশো: "গর্ভকালীন ডায়াবেটিস ও করণীয়"', False),
            ('fas fa-trophy', 'বিএমএ অ্যাওয়ার্ড ২০২৪', 'শ্রেষ্ঠ গাইনী ও প্রসূতি বিশেষজ্ঞ পুরস্কার', True),
            ('fas fa-globe', 'RCOG কনফারেন্স', 'লন্ডনে আন্তর্জাতিক সম্মেলনে মূল বক্তা', False),
        ]
        for i, (icon, name, desc, is_amber) in enumerate(media):
            MediaCoverage.objects.create(icon_class=icon, outlet_name=name, description=desc, is_amber=is_amber, order=i)
        self.stdout.write('  ✅ Media coverage')

        # ── TEAM ───────────────────────────────────────────────────────────────
        TeamMember.objects.all().delete()
        team = [
            ('প্রধান বিশেষজ্ঞ', 'ডাঃ সানজিদা ইসলাম চৌধুরী', 'MBBS, FCPS (গাইনী), MRCOG (UK)',
             'https://img.freepik.com/premium-photo/portrait-female-doctor-white-coat-stethoscope_73944-4.jpg?w=400',
             'fas fa-user-md', True),
            ('সহকারী বিশেষজ্ঞ', 'ডাঃ রোখসানা পারভীন', 'MBBS, DGO (গাইনী বিশেষজ্ঞ)', '', 'fas fa-user-md', False),
            ('সিনিয়র মিডওয়াইফ', 'হোসনে আরা বেগম', 'বিএসসি মিডওয়াইফারি (প্রসব সহকারী)', '', 'fas fa-user-nurse', False),
            ('চেম্বার পরিচালক', 'মাসুদ রানা', 'বিবিএ (হাসপাতাল ম্যানেজমেন্ট)', '', 'fas fa-user-tie', False),
        ]
        for i, (role, name, qual, photo_url, icon, is_lead) in enumerate(team):
            TeamMember.objects.create(role=role, name=name, qualifications=qual, photo_url=photo_url, icon_class=icon, is_lead=is_lead, order=i)
        self.stdout.write('  ✅ Team members')

        # ── FAQs ───────────────────────────────────────────────────────────────
        FAQ.objects.all().delete()
        faqs = [
            ('প্রথমবার গর্ভধারণে কখন ডাক্তার দেখাতে হবে?',
             'গর্ভধারণ নিশ্চিত হওয়ার সঙ্গে সঙ্গে, সাধারণত ৬–৮ সপ্তাহের মধ্যে প্রথম দর্শন সারতে হবে। রক্তপরীক্ষা ও আলট্রাসনোগ্রাফি করানো হবে।'),
            ('অনলাইনে কনসাল্টেশন কীভাবে করব?',
             'হোয়াটসঅ্যাপে ০১৮১১-২২৩৩৪৪ নম্বরে যোগাযোগ করুন। পেমেন্ট করার পর নির্ধারিত সময়ে ভিডিও কল করুন। প্রেসক্রিপশন ইমেইলে পাঠানো হবে।'),
            ('সিজার করালে পরবর্তী গর্ভধারণে স্বাভাবিক প্রসব সম্ভব?',
             'হ্যাঁ, অনেক ক্ষেত্রেই সম্ভব। একে VBAC (Vaginal Birth After Caesarean) বলে। তবে এটি বিভিন্ন শর্তের উপর নির্ভর করে। বিস্তারিত পরামর্শের জন্য আসুন।'),
            ('বন্ধ্যাত্বের চিকিৎসায় কত সময় লাগে?',
             'প্রথমে সম্পূর্ণ মূল্যায়ন করা হয়। কারণ ও চিকিৎসা পদ্ধতির উপর নির্ভর করে সময় কয়েক মাস থেকে বছরখানেক হতে পারে। ধৈর্য ও নিয়মিত ফলোআপ জরুরি।'),
            ('গর্ভকালীন ডায়াবেটিস কি বিপজ্জনক?',
             'সময়মতো নির্ণয় ও সঠিক ব্যবস্থাপনায় গর্ভকালীন ডায়াবেটিস নিরাপদে নিয়ন্ত্রণ করা যায়। নিয়মিত চেকআপ এবং খাদ্যাভ্যাস নিয়ন্ত্রণ অত্যন্ত জরুরি।'),
            ('অ্যাপয়েন্টমেন্ট ছাড়া আসা যাবে কি?',
             'জরুরি অবস্থায় অবশ্যই আসতে পারবেন। তবে অ্যাপয়েন্টমেন্ট থাকলে সময়মতো সেবা পাবেন এবং অপেক্ষা কম করতে হবে। আগে থেকে বুক করার অনুরোধ।'),
        ]
        for i, (q, a) in enumerate(faqs):
            FAQ.objects.create(question=q, answer=a, order=i)
        self.stdout.write('  ✅ FAQs')

        # ── SUPERUSER ──────────────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('  ✅ Superuser created → username: admin | password: admin123')
        else:
            self.stdout.write('  ⚠️  Superuser "admin" already exists')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!\n'))
        self.stdout.write('🚀 Run: python manage.py runserver')
        self.stdout.write('🌐 Site: http://127.0.0.1:8000/')
        self.stdout.write('🔐 Admin: http://127.0.0.1:8000/admin-panel/ (admin / admin123)')
