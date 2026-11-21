# Qivea Skin Class — edit decision list.
# Times in clip segments are SOURCE seconds within that clip.
# Subtitle text: *word* = highlighted keyword.

CHAPTERS = {
    1: ("Kenali Jenis Kulit", "Ujian mudah lepas cuci muka"),
    2: ("3 Cara Pilih Sabun", "Supaya kulit tak kering & makin cerah"),
    3: ("Siapa Sesuai Guna Sabun Scrub?", "Cuci + scrub dalam satu langkah"),
    4: ("Promo Bulan November", "Special untuk penonton Qivea"),
}

def clip(name, a, b, chap, zoom=1.0, subs=(), ov=()):
    return dict(kind="clip", clip=name, a=a, b=b, chap=chap, zoom=zoom, subs=list(subs), ov=list(ov))

def card(kind, dur, **kw):
    return dict(kind="card", type=kind, dur=dur, **kw)

MAIN = [
    card("intro", 3.6),

    # ---------------- BAB 1 : JENIS KULIT ----------------
    card("chapter", 2.2, chap=1),
    clip("C2316", 0.10, 9.95, 1, 1.00,
         subs=[(0.15, 1.80, "Apa jenis kulit muka korang?"),
               (1.90, 5.25, "Jujur je, kulit muka korang dalam kategori yang macam mana?"),
               (5.45, 6.20, "*Kering?*"),
               (6.30, 7.20, "*Berminyak?*"),
               (7.60, 8.55, "*Kombinasi?*"),
               (8.65, 9.95, "Ataupun *sensitif?*")],
         ov=[(5.45, None, "chip", dict(i=0, text="Kering")),
             (6.30, None, "chip", dict(i=1, text="Berminyak")),
             (7.60, None, "chip", dict(i=2, text="Kombinasi")),
             (8.65, None, "chip", dict(i=3, text="Sensitif"))]),
    clip("C2318", 1.60, 5.90, 1, 1.12,
         subs=[(1.65, 5.90, "Cara paling senang nak tahu jenis kulit korang dalam masa *30 saat*.")],
         ov=[(1.80, None, "badge", dict(text="UJIAN JENIS KULIT", sub="Cara paling mudah di rumah"))]),
    clip("C2319", 0.15, 5.55, 1, 1.00,
         subs=[(0.20, 2.60, "Lepas cuci muka, biarkan muka kosong"),
               (2.60, 5.55, "tanpa pakai apa-apa selama *30 minit*.")],
         ov=[(0.30, None, "steps", dict(title="CARA BUAT UJIAN",
                                         items=["Cuci muka", "Biar kosong 30 minit", "Perhati rasa kulit"]))]),
    clip("C2323", 0.15, 16.25, 1, 1.12,
         subs=[(0.20, 4.75, "Kalau kulit rasa *tegang dan kering* satu muka, maknanya *kulit kering*."),
               (4.95, 9.40, "Kalau kulit *berkilat seluruh muka*, itu maknanya *kulit berminyak*."),
               (9.65, 12.95, "Dan kalau dekat *T-zone* sahaja berminyak,"),
               (12.95, 16.25, "pipi biasa ataupun kering, itu *kombinasi*.")],
         ov=[(0.30, None, "result", dict(i=0, cond="Tegang & kering satu muka", res="KERING")),
             (5.00, None, "result", dict(i=1, cond="Berkilat seluruh muka", res="BERMINYAK")),
             (9.70, None, "result", dict(i=2, cond="T-zone berminyak, pipi normal/kering", res="KOMBINASI"))]),

    # ---------------- BAB 2 : PILIH SABUN ----------------
    card("chapter", 2.2, chap=2),
    clip("C2309", 0.15, 9.45, 2, 1.00,
         subs=[(0.20, 4.20, "*3 cara pilih sabun* supaya kulit tak kering dan makin cerah."),
               (4.45, 6.20, "Ramai orang salah pilih sabun,"),
               (6.30, 9.45, "akhirnya kulit jadi *gatal dan bersisik*.")],
         ov=[(4.45, None, "warn", dict(text="Salah pilih sabun = kulit gatal & bersisik"))]),
    clip("C2309", 16.50, 19.10, 2, 1.12,
         subs=[(16.55, 19.10, "Sebelum beli, *semak tiga benda* dulu.")],
         ov=[(16.60, None, "badge", dict(text="SEMAK 3 BENDA", sub="sebelum beli sabun"))]),
    clip("C2310", 0.10, 8.25, 2, 1.00,
         subs=[(0.15, 2.70, "Yang pertama, pilih *bahan utama*,"),
               (2.70, 5.30, "contohnya *ekstrak betik* atau buah-buahan"),
               (5.30, 8.25, "yang boleh bantu mencerahkan *tanpa menghakis*.")],
         ov=[(0.30, None, "info", dict(num="1", title="BAHAN UTAMA",
                                        lines=["Ekstrak betik / buah-buahan", "Cerahkan tanpa menghakis"]))]),
    clip("C2311", 0.05, 4.05, 2, 1.12,
         subs=[(0.10, 4.05, "Yang kedua, cari sabun yang ada fungsi *2 dalam 1*.")],
         ov=[(0.30, None, "info", dict(num="2", title="FUNGSI 2 DALAM 1",
                                        lines=["Cuci + scrub serentak", "Buang sel kulit mati"]))]),
    clip("C2311", 7.45, 14.85, 2, 1.00,
         subs=[(7.50, 11.70, "Kalau nak *jimat masa*, cari sabun yang ada sekali scrub."),
               (11.80, 14.85, "Time cuci, terus boleh *buang sel-sel kulit mati*.")],
         ov=[(7.45, None, "info", dict(num="2", title="FUNGSI 2 DALAM 1", noanim=True,
                                        lines=["Cuci + scrub serentak", "Buang sel kulit mati"]))]),
    clip("C2312", 0.05, 8.15, 2, 1.12,
         subs=[(0.10, 2.00, "Yang ketiga, *kelembapan*."),
               (2.20, 5.60, "Pastikan lepas cuci, kulit rasa *lebih lembut dan segar*,"),
               (5.60, 8.15, "bukan kering ataupun tegang.")],
         ov=[(0.25, None, "info", dict(num="3", title="KELEMBAPAN",
                                        lines=["Lembut & segar lepas cuci", "Bukan kering atau tegang"]))]),
    clip("C2314", 0.05, 4.35, 2, 1.00,
         subs=[(0.10, 4.35, "Sabun pencuci muka korang dah ikut *ketiga-tiga kriteria* ni?")],
         ov=[(0.20, None, "recap", dict(title="SEMAK SABUN ANDA",
                                         items=["Bahan utama yang sesuai", "Fungsi 2 dalam 1", "Kekal lembap"]))]),

    # ---------------- BAB 3 : SIAPA SESUAI ----------------
    card("chapter", 2.2, chap=3),
    clip("C2299", 1.50, 6.40, 3, 1.00,
         subs=[(1.55, 4.70, "Siapa yang sebenarnya sesuai guna *sabun scrub* ni?"),
               (4.70, 6.40, "Semua jenis kulit ke?")],
         ov=[(1.70, None, "badge", dict(text="SESUAI UNTUK SIAPA?", sub="Sabun scrub Qivea"))]),
    clip("C2301", 0.15, 9.65, 3, 1.12,
         subs=[(0.20, 4.20, "Pertama, korang yang ada masalah *daki degil* dekat celah lipatan."),
               (4.35, 9.65, "Yang kedua, kulit badan jenis *kasar, kusam dan berjerawat*.")],
         ov=[(0.30, None, "tick", dict(i=0, text="Daki degil di celah lipatan")),
             (4.40, None, "tick", dict(i=1, text="Kulit kasar, kusam & berjerawat"))]),
    clip("C2302", 0.10, 7.10, 3, 1.00,
         subs=[(0.15, 4.35, "Ketiga, nak cerahkan kulit ataupun *tona tak sekata*,"),
               (4.50, 7.10, "tapi malas nak guna scrub asing.")],
         ov=[(0.00, None, "tick", dict(i=0, text="Daki degil di celah lipatan", noanim=True)),
             (0.00, None, "tick", dict(i=1, text="Kulit kasar, kusam & berjerawat", noanim=True)),
             (0.25, None, "tick", dict(i=2, text="Tona kulit tak sekata"))]),
    clip("C2303", 0.20, 4.60, 3, 1.12,
         subs=[(0.25, 4.60, "Guna ni, *2 dalam 1* — terus cuci dan *buang sel kulit mati*.")],
         ov=[(0.40, None, "big", dict(top="2 DALAM 1", bottom="Cuci + buang sel kulit mati"))]),

    # ---------------- OUTRO ----------------
    clip("C2324", 0.20, 7.35, 3, 1.00,
         subs=[(0.25, 1.60, "*Cuba buat hari ni!*"),
               (1.65, 4.30, "Lepas tu, *subscribe* dan on notification"),
               (4.30, 7.35, "untuk tips penjagaan kulit yang seterusnya.")],
         ov=[(1.70, None, "subscribe", dict())]),
]

PROMO = [
    card("chapter", 2.0, chap=4),
    clip("C2326", 0.10, 12.20, 4, 1.00,
         subs=[(0.15, 2.35, "*Special untuk bulan 11 sahaja!*"),
               (2.55, 7.75, "Syarat nak dapat *iPhone 18 Pro*, hanya bermodalkan *satu sabun Qivea* sahaja."),
               (7.85, 12.20, "Kalau korang nak dapat iPhone 18 Pro, *terus masuk live sekarang!*")],
         ov=[(7.90, None, "live", dict(text="MASUK LIVE SEKARANG"))]),
]

END = [card("end", 3.8)]

VERSIONS = {
    "qivea_skin_class_full": MAIN + PROMO + END,
    "qivea_skin_class_evergreen": MAIN + END,
}
