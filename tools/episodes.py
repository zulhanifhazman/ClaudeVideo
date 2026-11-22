# Edit decision lists for the Qivea "Kelas Kulit" education series.
# Times are in SOURCE-clip seconds. Subtitle chunks: (text, start, end); *word* = highlighted keyword.

EPISODES = {
 "EP01_3_Cara_Pilih_Sabun": {
  "label": "KELAS KULIT · EP 01",
  "title": ["3 Cara Pilih Sabun", "Kulit Tak Kering & Makin Cerah"],
  "panel_title": "SEMAK 3 PERKARA SEBELUM BELI",
  "rows": ["Bahan utama: ekstrak betik / buah-buahan",
           "Fungsi 2-dalam-1: cuci + scrub",
           "Kelembapan: lembut, tak tegang"],
  "segments": [
   {"src": "C2309", "in": 0.00, "out": 4.25, "zoom": 1.00, "subs": [
      ("*3 cara* pilih sabun", 0.00, 1.76), ("supaya kulit *tak kering*", 1.76, 2.88), ("dan makin *cerah*", 2.88, 4.25)]},
   {"src": "C2309", "in": 4.45, "out": 9.30, "zoom": 1.10, "subs": [
      ("Ramai orang *salah pilih* sabun,", 4.50, 6.20), ("akhirnya kulit jadi", 6.35, 7.48), ("*kasar* & *bersisik*", 7.48, 9.30)],
    "events": [("warn", 6.35, 9.30, "Salah pilih sabun = kulit kasar & bersisik")]},
   {"src": "C2309", "in": 16.10, "out": 18.95, "zoom": 1.00, "subs": [
      ("Sebelum beli,", 16.10, 17.50), ("*semak 3 perkara* dulu!", 17.60, 18.95)],
    "events": [("panel", 16.10)]},
   {"src": "C2310", "in": 0.00, "out": 8.35, "zoom": 1.06, "subs": [
      ("Yang *pertama*,", 0.00, 1.20), ("pilih *bahan utama*", 1.30, 2.60), ("contohnya *ekstrak betik*", 2.70, 4.70),
      ("atau *buah-buahan*", 4.70, 5.60), ("yang bantu *cerahkan*", 5.60, 7.10), ("*tanpa menghakis*", 7.10, 8.35)],
    "events": [("row", 0.00, 0)]},
   {"src": "C2311", "in": 0.00, "out": 3.85, "zoom": 1.00, "subs": [
      ("Yang *kedua*,", 0.00, 1.00), ("cari sabun *2 dalam 1*", 1.05, 3.85)],
    "events": [("row", 0.00, 1)]},
   {"src": "C2311", "in": 7.35, "out": 14.75, "zoom": 1.10, "subs": [
      ("Kalau nak *jimat masa*,", 7.40, 9.20), ("cari sabun yang ada", 9.30, 10.38), ("*sekali gus scrub*", 10.38, 11.70),
      ("Time cuci, terus boleh", 11.85, 13.58), ("buang *sel kulit mati*", 13.58, 14.75)],
    "events": [("badge", 10.38, 14.75, "2-IN-1", "Cuci + buang sel kulit mati")]},
   {"src": "C2312", "in": 0.00, "out": 8.05, "zoom": 1.00, "subs": [
      ("Yang *ketiga*:", 0.00, 0.95), ("*kelembapan*", 0.95, 2.10), ("Pastikan lepas cuci,", 2.20, 4.04),
      ("kulit rasa *lembut* & *segar*", 4.04, 6.35), ("*bukan kering* atau *tegang*", 6.40, 8.05)],
    "events": [("row", 0.00, 2)]},
   {"src": "C2314", "in": 0.00, "out": 5.30, "zoom": 1.08, "subs": [
      ("Sabun korang dah ikut", 0.00, 1.86), ("*ketiga-tiga kriteria* ni?", 1.86, 3.70), ("*Komen* kat bawah!", 4.20, 5.30)],
    "events": [("done", 0.00), ("cta", 3.9, "Komen sabun pilihan korang!")]},
  ],
  "recap_title": "RINGKASAN: PILIH SABUN",
 },

 "EP02_Siapa_Sesuai_Soap_Scrub": {
  "label": "KELAS KULIT · EP 02",
  "title": ["Siapa Sesuai Guna", "Soap Scrub Qivea?"],
  "panel_title": "SESUAI UNTUK KORANG YANG ADA:",
  "rows": ["Daki di celah lipatan",
           "Kulit badan kasar, kusam & berjerawat",
           "Tona tak sekata, malas scrub berasingan"],
  "segments": [
   {"src": "C2299", "in": 1.20, "out": 5.30, "zoom": 1.00, "subs": [
      ("Siapa yang *sebenarnya* sesuai", 1.30, 2.96), ("guna *Soap Scrub* ni?", 2.96, 4.15), ("Semua jenis kulit ke?", 4.20, 5.30)]},
   {"src": "C2301", "in": 0.00, "out": 5.10, "zoom": 1.08, "subs": [
      ("*Pertama*,", 0.00, 1.00), ("korang yang ada masalah", 1.04, 1.88), ("*daki* dekat *celah lipatan*", 1.88, 4.20),
      ("Yang *kedua*,", 4.30, 5.10)],
    "events": [("panel", 0.00), ("row", 0.00, 0), ("row", 4.30, 1)]},
   {"src": "C2301", "in": 6.30, "out": 9.55, "zoom": 1.00, "subs": [
      ("kulit badan *kasar*,", 6.35, 7.95), ("*kusam* & *berjerawat*", 8.05, 9.55)]},
   {"src": "C2302", "in": 0.00, "out": 6.95, "zoom": 1.08, "subs": [
      ("*Ketiga*,", 0.00, 0.72), ("nak *cerahkan* kulit", 0.72, 1.90), ("ataupun *tona tak sekata*", 1.90, 4.15),
      ("tapi malas nak guna", 4.25, 5.92), ("*scrub* asing", 5.92, 6.95)],
    "events": [("row", 0.00, 2)]},
   {"src": "C2303", "in": 0.00, "out": 4.40, "zoom": 1.00, "subs": [
      ("Guna yang ni —", 0.00, 1.06), ("*2 dalam 1*", 1.06, 2.15), ("terus *cuci* & *buang*", 2.30, 3.54), ("*sel kulit mati*", 3.54, 4.40)],
    "events": [("done", 0.00), ("badge", 1.06, 4.40, "2-IN-1", "Cuci + scrub sekali mandi")]},
   {"src": "C2305", "in": 0.00, "out": 2.65, "zoom": 1.08, "subs": [
      ("Korang ada masalah yang macam mana?", 0.00, 1.45), ("*Komen* kat bawah!", 1.50, 2.65)],
    "events": [("cta", 0.0, "Komen masalah kulit korang!")]},
  ],
  "recap_title": "RINGKASAN: SIAPA SESUAI?",
 },

 "EP03_Kenal_Jenis_Kulit": {
  "label": "KELAS KULIT · EP 03",
  "title": ["Kenal Jenis Kulit Muka", "dalam 30 Saat"],
  "panel_title": "UJIAN MUKA KOSONG 30 MINIT",
  "rows": ["Tegang & kering satu muka → KERING",
           "Berkilat seluruh muka → BERMINYAK",
           "T-zone berminyak, pipi biasa → KOMBINASI"],
  "segments": [
   {"src": "C2318", "in": 1.15, "out": 5.75, "zoom": 1.00, "subs": [
      ("Cara *paling senang*", 1.20, 2.74), ("nak tahu *jenis kulit* korang", 2.74, 4.34), ("dalam masa *30 saat*!", 4.34, 5.75)]},
   {"src": "C2319", "in": 0.00, "out": 5.55, "zoom": 1.08, "subs": [
      ("Lepas *cuci muka*,", 0.00, 1.45), ("biarkan muka *kosong*", 1.50, 2.64), ("tanpa pakai apa-apa", 2.64, 3.74), ("selama *30 minit*", 3.74, 5.55)],
    "events": [("panel", 0.00), ("timer", 0.00, 5.55)]},
   {"src": "C2323", "in": 0.00, "out": 4.62, "zoom": 1.00, "subs": [
      ("Kalau kulit muka rasa", 0.00, 1.26), ("*tegang* & *kering* satu muka,", 1.26, 3.26), ("itu maknanya *kulit kering*", 3.26, 4.62)],
    "events": [("row", 0.00, 0)]},
   {"src": "C2323", "in": 4.70, "out": 9.45, "zoom": 1.08, "subs": [
      ("Kalau kulit muka *berkilat*", 4.75, 6.60), ("*seluruh muka*,", 6.60, 7.35), ("itu maknanya *kulit berminyak*", 7.40, 9.45)],
    "events": [("row", 4.75, 1)]},
   {"src": "C2323", "in": 9.60, "out": 16.00, "zoom": 1.00, "subs": [
      ("Dan kalau kulit korang,", 9.65, 11.25), ("dekat *T-zone* sahaja berminyak,", 11.35, 13.04), ("dan pipi *biasa* atau *kering*,", 13.04, 14.88),
      ("itu *kombinasi*!", 14.90, 16.00)],
    "events": [("row", 9.65, 2), ("tzone", 11.35, 14.88)]},
   {"src": "C2316", "in": 0.00, "out": 11.50, "zoom": 1.06, "subs": [
      ("Apa *jenis kulit* muka korang?", 0.00, 1.60), ("Jujur je —", 1.70, 2.70), ("dalam kategori yang macam mana?", 2.75, 5.25),
      ("*Kering*,", 5.40, 6.40), ("*berminyak*,", 6.45, 7.50), ("*kombinasi*,", 7.55, 8.65), ("ataupun *sensitif*?", 8.70, 10.10),
      ("*Drop komen* kat bawah!", 10.15, 11.50)],
    "events": [("done", 0.00), ("poll", 5.40, 11.50, [5.40, 6.45, 7.55, 8.70])]},
   {"src": "C2324", "in": 0.00, "out": 7.15, "zoom": 1.00, "subs": [
      ("*Save* video ni.", 0.00, 1.45), ("Lepas tu, *subscribe*", 1.55, 2.90), ("& on *notification*", 3.00, 4.20),
      ("untuk tips penjagaan kulit", 4.20, 6.15), ("yang seterusnya!", 6.15, 7.15)],
    "events": [("cta", 0.0, "Save + Subscribe untuk tips seterusnya")]},
  ],
  "recap_title": "RINGKASAN: JENIS KULIT",
 },
}
