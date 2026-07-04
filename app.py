import random
import json

import streamlit as st
import streamlit.components.v1 as components


APP_TITLE = "Sports Jersey Prompt Generator"
APP_SUBTITLE = "Prompt photoshoot jersey olahraga yang realistis, natural, dan profesional."

JERSEY_REFERENCE_TEXT = (
    "Use the uploaded jersey design as the main reference. "
    "Apply the jersey design exactly the same as the provided design reference, "
    "without changing any detail."
)

JERSEY_LOCK_TEXT = (
    "Keep every jersey detail unchanged: colors, pattern, motif, logo placement, "
    "sponsor placement, collar shape, sleeve details, side panels, stitching details, "
    "front design, back design, names, numbers, and all graphic elements."
)

NEGATIVE_PROMPT = (
    "Negative prompt: cartoon, anime, illustration, CGI, 3D render, plastic skin, "
    "overly glossy jersey, unrealistic fabric, distorted body, extra fingers, missing fingers, "
    "deformed hands, bad anatomy, duplicated person, blurry face, low resolution, pixelated, "
    "warped logo, changed jersey design, wrong colors, wrong pattern, moved sponsor logo, "
    "incorrect number, incorrect name, unreadable text, fake badge, altered collar, altered sleeves, "
    "messy composition, harsh overexposure, underexposure, watermark, signature, frame, text overlay."
)


def p(label, prompt):
    return {"label": label, "prompt": prompt}


PRESETS = {
    "tampilan_foto": [
        p("Jersey dipakai atlet/model", "jersey worn naturally by a real athlete or sportswear model"),
        p("Detail produk jersey saja", "jersey product detail photo without a full human model"),
        p("Jersey digantung", "jersey hanging naturally as a product mockup"),
        p("Jersey di kursi stadion", "jersey placed on a stadium seat as a realistic product display"),
        p("Jersey di ruang ganti", "jersey displayed in a locker room product scene"),
        p("Jersey dipegang tangan", "jersey held by hands for a realistic reveal photo"),
        p("Close-up bahan dan logo", "close-up product detail focusing on fabric texture, logo, collar, and stitching"),
        p("Tampak belakang nama dan nomor", "back view product photo focusing on player name and number"),
        p("Flat lay / jersey dibentangkan", "flat lay jersey product photo neatly arranged"),
        p("Katalog produk studio", "clean studio catalog product photo of the jersey"),
    ],
    "tema_produk": [
        p("Jersey di kursi pemain", "jersey placed on a player bench seat"),
        p("Jersey di kursi stadion kosong", "jersey placed on empty stadium seats"),
        p("Jersey digantung di locker", "jersey hanging inside a locker"),
        p("Jersey digantung di hanger", "jersey hanging on a simple hanger"),
        p("Jersey dibentangkan di meja", "jersey laid flat neatly on a table"),
        p("Jersey di atas rumput", "jersey laid on clean grass pitch"),
        p("Jersey dipegang dua tangan", "jersey held open by two hands"),
        p("Jersey tampak depan penuh", "full front view of the jersey as the main product"),
        p("Jersey tampak belakang penuh", "full back view of the jersey as the main product"),
        p("Close-up logo dada", "close-up of chest logo and sponsor area"),
        p("Close-up kerah", "close-up of collar shape and neckline"),
        p("Close-up lengan", "close-up of sleeve detail and sleeve trim"),
        p("Close-up motif kain", "close-up of fabric pattern and texture"),
        p("Detail jahitan samping", "close-up of side panels and stitching"),
        p("Detail nama dan nomor", "close-up of back name and number"),
        p("Jersey di lantai locker room", "jersey laid naturally on locker room floor"),
        p("Jersey di bangku gym", "jersey placed on a gym bench"),
        p("Jersey di rak apparel", "jersey displayed on a sportswear rack"),
        p("Jersey dengan sepatu olahraga", "jersey product photo with sport shoes nearby"),
        p("Jersey dengan bola/raket", "jersey product photo with relevant sport equipment nearby"),
        p("Mockup campaign premium", "premium campaign-style jersey product mockup"),
        p("Mockup presentasi klien", "clean client presentation jersey mockup"),
        p("Foto detail untuk katalog", "catalog detail product photo"),
        p("Konten promosi brand", "promotional brand content product photo"),
    ],
    "olahraga": [
        p("Sepak bola", "football / soccer"),
        p("Futsal", "futsal"),
        p("Lari / running", "running"),
        p("Badminton", "badminton"),
        p("Padel", "padel tennis"),
        p("Basket", "basketball"),
        p("Voli", "volleyball"),
        p("Tenis", "tennis"),
        p("Sepeda", "cycling"),
        p("Gym / fitness", "gym fitness training"),
        p("Rugby", "rugby"),
        p("Baseball", "baseball"),
        p("Hoki", "field hockey"),
        p("Esports jersey", "esports team jersey"),
        p("Training olahraga umum", "general sports training"),
    ],
    "jenis_model": [
        p("Tanpa model, fokus produk", "no human model, jersey product only"),
        p("Tangan memegang jersey saja", "hands holding the jersey, no full face visible"),
        p("Atlet pria profesional", "male professional athlete"),
        p("Atlet wanita profesional", "female professional athlete"),
        p("Model pria sporty", "male athletic sportswear model"),
        p("Model wanita sporty", "female athletic sportswear model"),
        p("Kapten tim pria", "male team captain"),
        p("Kapten tim wanita", "female team captain"),
        p("Atlet muda akademi", "youth academy athlete"),
        p("Atlet senior berpengalaman", "experienced senior athlete"),
        p("Runner pria", "male runner"),
        p("Runner wanita", "female runner"),
        p("Pemain badminton pria", "male badminton player"),
        p("Pemain badminton wanita", "female badminton player"),
        p("Pemain padel pria", "male padel player"),
        p("Pemain padel wanita", "female padel player"),
        p("Pemain basket pria", "male basketball player"),
        p("Pemain basket wanita", "female basketball player"),
        p("Pemain voli pria", "male volleyball player"),
        p("Pemain voli wanita", "female volleyball player"),
        p("Pemain tenis pria", "male tennis player"),
        p("Pemain tenis wanita", "female tennis player"),
        p("Atlet gym / fitness", "fitness athlete"),
        p("Pemain futsal pria", "male futsal player"),
        p("Pemain futsal wanita", "female futsal player"),
        p("Kiper", "goalkeeper"),
        p("Defender / pemain bertahan", "defensive athlete"),
        p("Pemain sayap cepat", "fast winger athlete"),
        p("Midfielder / pengatur permainan", "midfielder playmaker"),
        p("Tim campuran pria dan wanita", "mixed male and female sports team"),
        p("Duo atlet untuk campaign", "two-athlete sportswear campaign models"),
        p("Grup atlet profesional", "group of professional athletes"),
        p("Model brand ambassador", "sportswear brand ambassador model"),
        p("Atlet urban street sport", "urban street sport athlete"),
    ],
    "jumlah_model": [
        p("Tanpa model", "no human model"),
        p("1 orang", "1 model"),
        p("2 orang", "2 models"),
        p("3 orang", "3 models"),
        p("5 orang lineup tim", "5 models team lineup"),
        p("Tim besar / full squad", "full team group"),
    ],
    "pose": [
        p("Jersey dibentangkan rapi", "jersey neatly spread out as the main product"),
        p("Jersey digantung natural", "jersey hanging naturally as a product display"),
        p("Jersey diletakkan di kursi", "jersey placed naturally on a seat"),
        p("Jersey dipegang menghadap kamera", "jersey held open facing the camera"),
        p("Close-up logo dan sponsor", "close-up of logo and sponsor area"),
        p("Close-up kerah dan jahitan", "close-up of collar and stitching details"),
        p("Close-up lengan jersey", "close-up of sleeve detail"),
        p("Bagian belakang nama nomor", "back view focusing on name and number"),
        p("Jersey dilipat sebagian", "jersey partially folded in a natural product photo"),
        p("Detail kain dan motif", "fabric texture and motif detail shot"),
        p("Berdiri santai percaya diri", "standing confidently with relaxed arms"),
        p("Tangan menyilang", "crossed arms hero pose"),
        p("Berjalan ke arah kamera", "walking naturally toward camera"),
        p("Memegang ujung kerah jersey", "adjusting the jersey collar"),
        p("Menarik bagian depan jersey", "lightly pulling the front of the jersey to show fabric detail"),
        p("Menunjuk logo di dada", "pointing to the chest logo area naturally"),
        p("Memegang bola di samping badan", "holding a ball under one arm"),
        p("Mengikat sepatu olahraga", "tying sport shoes before training"),
        p("Pemanasan sebelum latihan", "warming up before training"),
        p("Stretching ringan", "doing a light athletic stretch"),
        p("Jogging pelan", "light jogging motion"),
        p("Sprint cepat", "fast sprint action pose"),
        p("Lari di tikungan track", "running around a track curve"),
        p("Start lari dari garis start", "starting run from the start line"),
        p("Selebrasi kemenangan", "natural celebration after winning"),
        p("Selebrasi setelah mencetak poin", "celebration pose after scoring"),
        p("Fokus sebelum pertandingan", "pre-match focused pose"),
        p("Duduk di ruang ganti", "seated locker room portrait"),
        p("Berdiri di lorong stadion", "standing in a stadium tunnel"),
        p("Team huddle / kumpul tim", "team huddle pose"),
        p("Lineup tim menghadap kamera", "team lineup facing camera"),
        p("Melompat untuk smash", "jumping for a smash action"),
        p("Ayunan raket badminton", "badminton racket swing action"),
        p("Servis badminton", "badminton serve pose"),
        p("Ayunan raket padel", "padel racket swing action"),
        p("Ready position padel", "padel ready position"),
        p("Dribble bola basket", "basketball dribble action"),
        p("Shooting basket", "basketball shooting pose"),
        p("Passing bola", "passing the ball in motion"),
        p("Menendang bola", "kicking a ball naturally"),
        p("Kontrol bola dekat kaki", "close ball control near the feet"),
        p("Menerima umpan", "receiving a pass"),
        p("Block voli", "volleyball blocking action"),
        p("Smash voli", "volleyball spike action"),
        p("Pose after workout", "post-workout confident pose"),
        p("Mengangkat dumbbell ringan", "holding a light dumbbell naturally"),
        p("Berjalan di studio campaign", "walking in a sportswear studio campaign"),
        p("Menoleh ke samping", "looking slightly to the side"),
        p("Menatap kamera dengan tenang", "looking calmly into the camera"),
        p("Tertawa natural bersama tim", "natural team laugh"),
        p("Berbicara dengan rekan tim", "talking naturally with a teammate"),
        p("Mengikat rambut sebelum latihan", "tying hair before training"),
        p("Memakai wristband", "adjusting a wristband"),
        p("Membawa tas olahraga", "carrying a sports bag"),
        p("Minum dari botol olahraga", "drinking from a sport bottle naturally"),
        p("Duduk di bench pemain", "sitting on the player bench"),
        p("Bersandar di dinding urban court", "leaning against an urban court wall"),
        p("Foto close-up bagian jersey", "close-up pose emphasizing jersey texture"),
        p("Full body pose untuk katalog", "full-body catalog pose"),
        p("Pose campaign premium", "premium sportswear campaign pose"),
        p("Pose candid natural", "natural candid athletic pose"),
        p("Berjalan bersama tim", "walking together with teammates"),
        p("Berdoa / fokus sebelum game", "quiet focused pre-game moment"),
    ],
    "ekspresi": [
        p("Tenang dan percaya diri", "calm and confident expression"),
        p("Fokus serius", "serious focused expression"),
        p("Senyum natural", "natural relaxed smile"),
        p("Intens kompetitif", "intense competitive look"),
        p("Bangga seperti kapten", "proud captain expression"),
        p("Enerjik setelah menang", "energetic victory expression"),
        p("Semangat latihan", "determined training expression"),
        p("Ramah untuk campaign", "friendly sports campaign expression"),
    ],
    "komposisi": [
        p("Portrait profesional bersih", "clean professional sports portrait composition"),
        p("Full body seluruh badan", "full-body sportswear campaign composition"),
        p("Half body pinggang ke atas", "half-body editorial sports composition"),
        p("Action shot dinamis", "dynamic action composition with realistic motion"),
        p("Poster tim", "team poster composition"),
        p("Jersey jadi fokus utama", "centered product-focused jersey composition"),
        p("Cinematic match day", "cinematic match day composition"),
        p("Minimal modern campaign", "minimal modern sportswear campaign layout"),
        p("Close-up detail bahan", "close-up jersey fabric detail composition"),
        p("Wide shot lokasi terlihat", "wide environmental sports composition"),
        p("Candid natural", "natural candid sports photography composition"),
        p("Editorial majalah olahraga", "sports magazine editorial composition"),
        p("Lookbook sportswear", "sportswear lookbook composition"),
        p("Hero shot brand campaign", "hero shot brand campaign composition"),
        p("Before match story", "pre-match storytelling composition"),
        p("After training story", "post-training storytelling composition"),
    ],
    "background": [
        p("Kursi pemain / bench", "player bench seat product scene"),
        p("Kursi stadion kosong", "empty stadium seat product scene"),
        p("Locker room product setup", "locker room product setup"),
        p("Hanger studio bersih", "clean studio hanger setup"),
        p("Meja katalog produk", "clean product catalog table"),
        p("Rak apparel olahraga", "sportswear apparel rack"),
        p("Lantai kayu indoor court", "indoor court wooden floor product scene"),
        p("Rumput lapangan untuk detail jersey", "grass pitch product detail setup"),
        p("Backdrop studio minimal", "minimal studio backdrop product scene"),
        p("Bench gym modern", "modern gym bench product scene"),
        p("Stadion sepak bola", "football stadium"),
        p("Lapangan futsal indoor", "indoor futsal court"),
        p("Lorong stadion", "stadium tunnel"),
        p("Ruang ganti pemain", "locker room"),
        p("Lapangan latihan rumput", "grass training ground"),
        p("Lintasan lari", "running track"),
        p("Gym sport campaign", "gym sport campaign environment"),
        p("Stadion malam floodlight", "night stadium floodlight"),
        p("Lapangan bola urban", "urban football court"),
        p("Studio campaign profesional", "professional studio sportswear campaign"),
        p("Lapangan rumput golden hour", "grass pitch during golden hour"),
        p("Arena indoor bersih", "clean indoor sports arena"),
        p("Tribun stadion", "stadium seats background"),
        p("Street court beton", "concrete street sport court"),
        p("Stadion hujan ringan", "rainy match day stadium"),
        p("Lapangan badminton indoor", "indoor badminton court"),
        p("Lapangan padel modern", "modern padel court"),
        p("Lapangan basket indoor", "indoor basketball court"),
        p("Lapangan basket outdoor", "outdoor basketball court"),
        p("Lapangan voli indoor", "indoor volleyball court"),
        p("Lapangan tenis outdoor", "outdoor tennis court"),
        p("Tepi track dengan tribun", "trackside stadium environment"),
        p("Area start race", "race starting line area"),
        p("Jalan kota untuk running", "urban running street"),
        p("Taman kota sporty", "city park sport environment"),
        p("Rooftop sport court", "rooftop sport court"),
        p("Training camp outdoor", "outdoor training camp"),
        p("Area bench pemain", "player bench area"),
        p("Backdrop press conference", "sports press conference backdrop"),
        p("Studio hitam premium", "premium black studio sportswear set"),
        p("Studio putih bersih", "clean white studio sportswear set"),
        p("Gudang industrial sporty", "industrial warehouse sport campaign set"),
        p("Arena esports team room", "esports team room"),
        p("Velodrome / arena sepeda", "cycling velodrome"),
        p("Jalur sepeda outdoor", "outdoor cycling route"),
        p("Trek trail ringan", "light trail running route"),
        p("Lapangan rugby", "rugby field"),
        p("Lapangan baseball", "baseball field"),
        p("Lapangan hoki", "field hockey pitch"),
        p("Indoor performance lab", "indoor athletic performance lab"),
    ],
    "lighting": [
        p("Cahaya siang natural", "natural daylight"),
        p("Soft studio light", "soft studio lighting"),
        p("Cinematic stadium light", "cinematic stadium lighting"),
        p("Golden hour sore", "golden hour sunlight"),
        p("Lampu stadion malam", "night floodlight lighting"),
        p("Side light dramatis", "dramatic side lighting"),
        p("Commercial clean light", "clean commercial sportswear lighting"),
        p("Cahaya ruang ganti lembut", "soft locker room practical lighting"),
        p("Lampu futsal terang", "bright indoor court lighting"),
        p("Backlight tipis", "subtle backlight rim lighting"),
        p("Overcast natural", "soft overcast natural light"),
        p("Pagi cerah", "fresh morning light"),
        p("Cahaya sunset hangat", "warm sunset sports lighting"),
        p("High contrast editorial", "high contrast editorial lighting"),
        p("Low-key premium", "premium low-key studio lighting"),
        p("White studio even light", "even white studio lighting"),
        p("Action freeze lighting", "sharp action-freeze sports lighting"),
        p("Indoor arena light", "professional indoor arena lighting"),
        p("Rainy night reflection", "rainy night reflective stadium lighting"),
        p("Natural window light", "natural window light"),
        p("Softbox campaign", "large softbox campaign lighting"),
    ],
    "camera_angle": [
        p("Sejajar mata", "eye-level camera angle"),
        p("Sedikit dari bawah", "slightly low angle"),
        p("Hero shot dari bawah", "low angle hero shot"),
        p("Sedikit dari atas", "slightly high angle"),
        p("Dari samping", "side angle"),
        p("Tiga perempat", "three-quarter angle"),
        p("Menghadap depan", "front-facing camera angle"),
        p("Over shoulder", "over-the-shoulder sports angle"),
        p("Close-up dada jersey", "close-up chest jersey angle"),
        p("Full body eye level", "full-body eye-level angle"),
        p("Wide angle lingkungan", "wide environmental angle"),
        p("Tracking shot natural", "natural tracking shot angle"),
        p("Low angle action", "low angle action sports shot"),
        p("Side profile portrait", "side profile portrait angle"),
        p("Diagonal dynamic angle", "dynamic diagonal action angle"),
        p("Candid dari jauh", "candid telephoto angle from distance"),
        p("Bench level", "bench-level sports angle"),
        p("Tunnel depth angle", "stadium tunnel depth angle"),
        p("Top-down ringan", "subtle top-down athletic angle"),
        p("Product-first angle", "product-first jersey visibility angle"),
    ],
    "lens_look": [
        p("35mm realistis", "realistic 35mm lens look"),
        p("50mm portrait", "50mm portrait lens look"),
        p("85mm premium portrait", "85mm professional portrait lens look"),
        p("24-70mm campaign", "24-70mm sports campaign lens look"),
        p("Background blur halus", "shallow depth of field"),
        p("Editorial tajam", "crisp editorial sports photography"),
        p("Dokumenter natural", "natural documentary sports photography"),
        p("Commercial high-end", "high-end commercial sportswear photography"),
    ],
    "outfit": [
        p("Celana olahraga senada", "matching athletic shorts"),
        p("Celana pendek hitam", "black athletic shorts"),
        p("Celana pendek putih", "white athletic shorts"),
        p("Training pants", "training pants"),
        p("Legging kompresi", "compression leggings"),
        p("Kaos kaki dan sepatu bola", "football socks and boots"),
        p("Sepatu futsal", "futsal shoes and sport socks"),
        p("Styling campaign bersih", "clean sportswear campaign styling"),
        p("Celana running pendek", "running shorts"),
        p("Tight running shorts", "performance running shorts"),
        p("Celana badminton", "badminton shorts"),
        p("Rok olahraga wanita", "women's athletic skirt"),
        p("Celana padel", "padel athletic shorts"),
        p("Celana basket", "basketball shorts"),
        p("Celana voli", "volleyball shorts"),
        p("Jogger sport", "sport jogger pants"),
        p("Base layer lengan panjang", "long sleeve base layer under jersey"),
        p("Compression arm sleeve", "compression arm sleeve"),
        p("Headband / wristband", "headband and wristband sport styling"),
        p("Sepatu training modern", "modern training shoes"),
        p("Sepatu running", "running shoes"),
        p("Sepatu court indoor", "indoor court shoes"),
    ],
    "mood": [
        p("Photoshoot profesional realistis", "realistic professional photoshoot"),
        p("Suasana match day", "natural match day atmosphere"),
        p("Campaign sportswear premium", "premium sportswear campaign"),
        p("Cinematic olahraga", "cinematic sports editorial"),
        p("Pengumuman klub modern", "clean modern club announcement"),
        p("Latihan penuh energi", "high energy training session"),
        p("Identitas tim percaya diri", "confident team identity campaign"),
        p("Grassroots natural", "authentic grassroots sport mood"),
        p("Luxury minimal", "luxury minimal sportswear mood"),
        p("Urban street sport", "urban street sport mood"),
        p("Fresh morning training", "fresh morning training mood"),
        p("Intense competition", "intense competition mood"),
        p("Friendly community sport", "friendly community sport mood"),
        p("Elite athlete campaign", "elite athlete campaign mood"),
        p("Clean catalog product", "clean product catalog mood"),
        p("Rainy dramatic sport", "rainy dramatic sports mood"),
        p("Youth academy energy", "youth academy energy mood"),
        p("Team unity", "team unity mood"),
        p("Performance lab", "performance testing lab mood"),
        p("Confident personal branding", "confident personal branding mood"),
        p("Documentary candid", "documentary candid sport mood"),
    ],
    "output": [
        p("Portrait Instagram 4:5", "portrait Instagram 4:5, optimized for feed post"),
        p("Landscape 16:9", "landscape 16:9, wide campaign banner style"),
        p("Square 1:1", "square 1:1, balanced social media post"),
        p("Story vertikal 9:16", "vertical story 9:16, full-body composition with safe margins"),
    ],
}


QUICK_PRESETS = {
    "Match Day": {
        "tampilan_foto": "Jersey dipakai atlet/model",
        "tema_produk": "Jersey tampak depan penuh",
        "olahraga": "Sepak bola",
        "jenis_model": "Atlet pria profesional",
        "jumlah_model": "1 orang",
        "pose": "Berjalan ke arah kamera",
        "ekspresi": "Fokus serius",
        "komposisi": "Cinematic match day",
        "background": "Stadion sepak bola",
        "lighting": "Cinematic stadium light",
        "camera_angle": "Sedikit dari bawah",
        "lens_look": "50mm portrait",
        "outfit": "Kaos kaki dan sepatu bola",
        "mood": "Suasana match day",
        "output": "Portrait Instagram 4:5",
    },
    "Running": {
        "tampilan_foto": "Jersey dipakai atlet/model",
        "tema_produk": "Jersey tampak depan penuh",
        "olahraga": "Lari / running",
        "jenis_model": "Runner wanita",
        "jumlah_model": "1 orang",
        "pose": "Lari di tikungan track",
        "ekspresi": "Semangat latihan",
        "komposisi": "Action shot dinamis",
        "background": "Lintasan lari",
        "lighting": "Pagi cerah",
        "camera_angle": "Tracking shot natural",
        "lens_look": "Dokumenter natural",
        "outfit": "Celana running pendek",
        "mood": "Fresh morning training",
        "output": "Portrait Instagram 4:5",
    },
    "Badminton": {
        "tampilan_foto": "Jersey dipakai atlet/model",
        "tema_produk": "Jersey dengan bola/raket",
        "olahraga": "Badminton",
        "jenis_model": "Pemain badminton pria",
        "jumlah_model": "1 orang",
        "pose": "Ayunan raket badminton",
        "ekspresi": "Intens kompetitif",
        "komposisi": "Action shot dinamis",
        "background": "Lapangan badminton indoor",
        "lighting": "Indoor arena light",
        "camera_angle": "Tiga perempat",
        "lens_look": "24-70mm campaign",
        "outfit": "Celana badminton",
        "mood": "Intense competition",
        "output": "Landscape 16:9",
    },
    "Padel": {
        "tampilan_foto": "Jersey dipakai atlet/model",
        "tema_produk": "Jersey dengan bola/raket",
        "olahraga": "Padel",
        "jenis_model": "Pemain padel wanita",
        "jumlah_model": "2 orang",
        "pose": "Ready position padel",
        "ekspresi": "Tenang dan percaya diri",
        "komposisi": "Full body seluruh badan",
        "background": "Lapangan padel modern",
        "lighting": "Cahaya siang natural",
        "camera_angle": "Sejajar mata",
        "lens_look": "35mm realistis",
        "outfit": "Celana padel",
        "mood": "Campaign sportswear premium",
        "output": "Square 1:1",
    },
    "Studio Campaign": {
        "tampilan_foto": "Katalog produk studio",
        "tema_produk": "Mockup campaign premium",
        "olahraga": "Training olahraga umum",
        "jenis_model": "Model brand ambassador",
        "jumlah_model": "1 orang",
        "pose": "Pose campaign premium",
        "ekspresi": "Tenang dan percaya diri",
        "komposisi": "Jersey jadi fokus utama",
        "background": "Studio campaign profesional",
        "lighting": "Commercial clean light",
        "camera_angle": "Sejajar mata",
        "lens_look": "85mm premium portrait",
        "outfit": "Styling campaign bersih",
        "mood": "Campaign sportswear premium",
        "output": "Square 1:1",
    },
    "Team Poster": {
        "tampilan_foto": "Jersey dipakai atlet/model",
        "tema_produk": "Mockup campaign premium",
        "olahraga": "Training olahraga umum",
        "jenis_model": "Grup atlet profesional",
        "jumlah_model": "5 orang lineup tim",
        "pose": "Lineup tim menghadap kamera",
        "ekspresi": "Bangga seperti kapten",
        "komposisi": "Poster tim",
        "background": "Stadion malam floodlight",
        "lighting": "Lampu stadion malam",
        "camera_angle": "Hero shot dari bawah",
        "lens_look": "Commercial high-end",
        "outfit": "Celana olahraga senada",
        "mood": "Identitas tim percaya diri",
        "output": "Landscape 16:9",
    },
    "Kursi Stadion": {
        "tampilan_foto": "Jersey di kursi stadion",
        "tema_produk": "Jersey di kursi stadion kosong",
        "olahraga": "Sepak bola",
        "jenis_model": "Tanpa model, fokus produk",
        "jumlah_model": "Tanpa model",
        "pose": "Jersey diletakkan di kursi",
        "ekspresi": "Tenang dan percaya diri",
        "komposisi": "Jersey jadi fokus utama",
        "background": "Kursi stadion kosong",
        "lighting": "Cahaya siang natural",
        "camera_angle": "Sedikit dari atas",
        "lens_look": "35mm realistis",
        "outfit": "Styling campaign bersih",
        "mood": "Clean catalog product",
        "output": "Portrait Instagram 4:5",
    },
    "Locker Detail": {
        "tampilan_foto": "Jersey di ruang ganti",
        "tema_produk": "Jersey digantung di locker",
        "olahraga": "Training olahraga umum",
        "jenis_model": "Tanpa model, fokus produk",
        "jumlah_model": "Tanpa model",
        "pose": "Jersey digantung natural",
        "ekspresi": "Tenang dan percaya diri",
        "komposisi": "Close-up detail bahan",
        "background": "Locker room product setup",
        "lighting": "Cahaya ruang ganti lembut",
        "camera_angle": "Menghadap depan",
        "lens_look": "50mm portrait",
        "outfit": "Styling campaign bersih",
        "mood": "Campaign sportswear premium",
        "output": "Square 1:1",
    },
    "Close-up Logo": {
        "tampilan_foto": "Close-up bahan dan logo",
        "tema_produk": "Close-up logo dada",
        "olahraga": "Training olahraga umum",
        "jenis_model": "Tanpa model, fokus produk",
        "jumlah_model": "Tanpa model",
        "pose": "Close-up logo dan sponsor",
        "ekspresi": "Tenang dan percaya diri",
        "komposisi": "Close-up detail bahan",
        "background": "Backdrop studio minimal",
        "lighting": "Soft studio light",
        "camera_angle": "Close-up dada jersey",
        "lens_look": "Background blur halus",
        "outfit": "Styling campaign bersih",
        "mood": "Clean catalog product",
        "output": "Square 1:1",
    },
    "Back Number": {
        "tampilan_foto": "Tampak belakang nama dan nomor",
        "tema_produk": "Detail nama dan nomor",
        "olahraga": "Training olahraga umum",
        "jenis_model": "Tanpa model, fokus produk",
        "jumlah_model": "Tanpa model",
        "pose": "Bagian belakang nama nomor",
        "ekspresi": "Tenang dan percaya diri",
        "komposisi": "Jersey jadi fokus utama",
        "background": "Hanger studio bersih",
        "lighting": "Commercial clean light",
        "camera_angle": "Menghadap depan",
        "lens_look": "85mm premium portrait",
        "outfit": "Styling campaign bersih",
        "mood": "Clean catalog product",
        "output": "Portrait Instagram 4:5",
    },
}


def labels_for(key):
    return [item["label"] for item in PRESETS[key]]


def prompt_for(key, label):
    for item in PRESETS[key]:
        if item["label"] == label:
            return item["prompt"]
    return str(label)


def default_values():
    return {key: values[0]["label"] for key, values in PRESETS.items()}


def valid_value(key, value):
    labels = labels_for(key)
    return value if value in labels else labels[0]


def pick_random_values():
    values = {key: random.choice(labels_for(key)) for key in PRESETS}

    product_display_labels = {
        "Detail produk jersey saja",
        "Jersey digantung",
        "Jersey di kursi stadion",
        "Jersey di ruang ganti",
        "Jersey dipegang tangan",
        "Close-up bahan dan logo",
        "Tampak belakang nama dan nomor",
        "Flat lay / jersey dibentangkan",
        "Katalog produk studio",
    }
    product_poses = [
        "Jersey dibentangkan rapi",
        "Jersey digantung natural",
        "Jersey diletakkan di kursi",
        "Jersey dipegang menghadap kamera",
        "Close-up logo dan sponsor",
        "Close-up kerah dan jahitan",
        "Close-up lengan jersey",
        "Bagian belakang nama nomor",
        "Jersey dilipat sebagian",
        "Detail kain dan motif",
    ]
    product_backgrounds = [
        "Kursi pemain / bench",
        "Kursi stadion kosong",
        "Locker room product setup",
        "Hanger studio bersih",
        "Meja katalog produk",
        "Rak apparel olahraga",
        "Lantai kayu indoor court",
        "Rumput lapangan untuk detail jersey",
        "Backdrop studio minimal",
        "Bench gym modern",
    ]
    product_compositions = [
        "Jersey jadi fokus utama",
        "Close-up detail bahan",
        "Minimal modern campaign",
        "Lookbook sportswear",
        "Hero shot brand campaign",
    ]
    athlete_model_labels = [
        label for label in labels_for("jenis_model")
        if label not in {"Tanpa model, fokus produk", "Tangan memegang jersey saja"}
    ]
    athlete_pose_labels = [
        label for label in labels_for("pose")
        if label not in product_poses
    ]

    if values["tampilan_foto"] in product_display_labels:
        values["jenis_model"] = random.choice(["Tanpa model, fokus produk", "Tangan memegang jersey saja"])
        values["jumlah_model"] = "Tanpa model"
        values["pose"] = random.choice(product_poses)
        values["background"] = random.choice(product_backgrounds)
        values["komposisi"] = random.choice(product_compositions)
        values["outfit"] = "Styling campaign bersih"
        values["mood"] = random.choice(["Clean catalog product", "Campaign sportswear premium", "Luxury minimal", "Confident personal branding"])
    else:
        values["jenis_model"] = random.choice(athlete_model_labels)
        values["pose"] = random.choice(athlete_pose_labels)
        if values["jumlah_model"] == "Tanpa model":
            values["jumlah_model"] = random.choice(["1 orang", "2 orang", "3 orang"])

    return values


def build_prompt(values, custom_note):
    note = custom_note.strip()
    note_line = f"\nAdditional direction: {note}" if note else ""

    display_type = prompt_for("tampilan_foto", values["tampilan_foto"])
    product_theme = prompt_for("tema_produk", values["tema_produk"])
    sport = prompt_for("olahraga", values["olahraga"])
    model = prompt_for("jenis_model", values["jenis_model"])
    model_count = prompt_for("jumlah_model", values["jumlah_model"])
    pose = prompt_for("pose", values["pose"])
    expression = prompt_for("ekspresi", values["ekspresi"])
    composition = prompt_for("komposisi", values["komposisi"])
    background = prompt_for("background", values["background"])
    lighting = prompt_for("lighting", values["lighting"])
    camera_angle = prompt_for("camera_angle", values["camera_angle"])
    lens_look = prompt_for("lens_look", values["lens_look"])
    outfit = prompt_for("outfit", values["outfit"])
    mood = prompt_for("mood", values["mood"])
    output = prompt_for("output", values["output"])

    return f"""Realistic professional sportswear jersey photoshoot and jersey product mockup.

Photo/mockup type: {display_type}.
Product detail theme: {product_theme}.
Sport category: {sport}.
Main subject: {model_count}, {model}.
Pose: {pose}.
Expression: {expression}.
Composition: {composition}.
Background: {background}.
Lighting: {lighting}.
Camera angle: {camera_angle}.
Lens look: {lens_look}.
Outfit styling: {outfit}.
Mood: {mood}.
Final image format: {output}.{note_line}

Jersey reference instruction:
{JERSEY_REFERENCE_TEXT}
{JERSEY_LOCK_TEXT}

Make the uploaded jersey design look like real performance sportswear fabric. The result can show the jersey worn by an athlete, displayed on a bench, hanging in a locker room, laid flat, held by hands, or shown as a close-up product detail, based on the selected photo/mockup type. The jersey can be for football, futsal, running, badminton, padel, basketball, volleyball, tennis, gym training, or other sports, based on the selected sport category. Preserve the exact uploaded jersey design while making the result natural, realistic, sharp, professional, and ready for a sports club, product catalog, client presentation, team launch, or sportswear campaign.

{NEGATIVE_PROMPT}
"""


def set_random_prompt():
    random_values = pick_random_values()
    st.session_state.selected_values = random_values
    for key, value in random_values.items():
        st.session_state[key] = value
    st.session_state.generated_prompt = build_prompt(
        random_values,
        st.session_state.get("custom_note", ""),
    )


def set_quick_preset(preset_name):
    preset_values = default_values()
    preset_values.update(QUICK_PRESETS[preset_name])
    st.session_state.selected_values = preset_values
    for key, value in preset_values.items():
        st.session_state[key] = value
    st.session_state.generated_prompt = build_prompt(
        preset_values,
        st.session_state.get("custom_note", ""),
    )


def generate_from_current_selection():
    st.session_state.selected_values = {
        key: valid_value(key, st.session_state[key]) for key in PRESETS
    }
    st.session_state.generated_prompt = build_prompt(
        st.session_state.selected_values,
        st.session_state.get("custom_note", ""),
    )


def initialize_state():
    if "selected_values" not in st.session_state:
        st.session_state.selected_values = default_values()

    st.session_state.selected_values = {
        key: valid_value(key, st.session_state.selected_values.get(key, labels_for(key)[0]))
        for key in PRESETS
    }

    for key, value in st.session_state.selected_values.items():
        st.session_state[key] = valid_value(key, st.session_state.get(key, value))

    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = build_prompt(
            st.session_state.selected_values,
            "",
        )


def apply_custom_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: #090d14;
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }

        .app-hero {
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 30px 34px;
            color: #f9fafb;
            box-shadow: none;
            margin-bottom: 18px;
        }

        .app-hero h1 {
            font-size: clamp(2rem, 4vw, 3.4rem);
            line-height: 1.05;
            margin: 0 0 10px 0;
            letter-spacing: 0;
            color: #f9fafb;
        }

        .app-hero p {
            max-width: 760px;
            font-size: 1.02rem;
            line-height: 1.6;
            margin: 0;
            color: #cbd5e1;
        }

        .step-card {
            min-height: 108px;
            background: #111827;
            border: 1px solid #243244;
            border-radius: 8px;
            padding: 16px 18px;
            box-shadow: none;
        }

        .step-card strong {
            color: #f9fafb;
            display: block;
            font-size: 0.95rem;
            margin-bottom: 6px;
        }

        .step-card span {
            color: #94a3b8;
            line-height: 1.45;
            font-size: 0.92rem;
        }

        .section-title {
            color: #f9fafb;
            font-size: 1.2rem;
            font-weight: 700;
            margin: 14px 0 4px 0;
        }

        .soft-note {
            background: #101820;
            border-left: 4px solid #22c55e;
            border-radius: 8px;
            padding: 13px 15px;
            color: #d1d5db;
            margin: 10px 0 18px 0;
        }

        .mini-note {
            background: #0f172a;
            border: 1px solid #233044;
            border-radius: 8px;
            padding: 10px 12px;
            color: #cbd5e1;
            margin-bottom: 12px;
            font-size: 0.93rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #243244;
            box-shadow: none;
            background: #0f172a;
        }

        .stButton > button {
            background: #1f2937;
            border: 1px solid #334155;
            color: #f9fafb;
            border-radius: 8px;
            min-height: 42px;
            font-weight: 700;
        }

        .stButton > button:hover {
            background: #263244;
            border-color: #64748b;
            color: #ffffff;
        }

        .stButton > button[kind="primary"] {
            background: #22c55e;
            border-color: #22c55e;
            color: #07110b;
        }

        .stButton > button[kind="primary"]:hover {
            background: #16a34a;
            border-color: #16a34a;
            color: #061008;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: #94a3b8;
        }

        label, p, span, li {
            color: #d1d5db;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #f9fafb;
        }

        .stTextArea textarea {
            background: #050812;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #e5e7eb;
            font-size: 0.95rem;
            line-height: 1.55;
        }

        .stTextArea textarea:focus {
            border-color: #22c55e;
            box-shadow: 0 0 0 1px #22c55e;
        }

        div[data-baseweb="select"] > div {
            background: #050812;
            border-color: #334155;
            border-radius: 8px;
            color: #e5e7eb;
        }

        div[data-baseweb="select"] span {
            color: #e5e7eb;
        }

        div[data-baseweb="tab-list"] button {
            color: #cbd5e1;
        }

        section[data-testid="stSidebar"] {
            background: #050812;
            border-right: 1px solid #1f2937;
        }

        div[data-testid="stAlert"] {
            background: #111827;
            color: #d1d5db;
            border: 1px solid #243244;
        }

        @media (max-width: 720px) {
            .app-hero {
                padding: 24px 20px;
            }
            .step-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_step_cards():
    step_1, step_2, step_3 = st.columns(3)
    with step_1:
        st.markdown(
            """
            <div class="step-card">
                <strong>1. Pilih olahraga</strong>
                <span>Tentukan jersey ini untuk bola, running, badminton, padel, dan lainnya.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_2:
        st.markdown(
            """
            <div class="step-card">
                <strong>2. Atur gaya foto</strong>
                <span>Pilih model, pose, lokasi, cahaya, dan mood dengan bahasa sederhana.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_3:
        st.markdown(
            """
            <div class="step-card">
                <strong>3. Pakai prompt</strong>
                <span>Upload desain jersey, lalu tempel prompt ke image generator.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_copy_prompt_button(prompt_text):
    prompt_json = json.dumps(prompt_text)
    components.html(
        f"""
        <button id="copyPromptButton" type="button">Copy Hasil Prompt</button>
        <div id="copyPromptStatus" aria-live="polite"></div>

        <script>
        const promptText = {prompt_json};
        const button = document.getElementById("copyPromptButton");
        const statusText = document.getElementById("copyPromptStatus");

        async function copyPrompt() {{
            try {{
                await navigator.clipboard.writeText(promptText);
                statusText.textContent = "Prompt berhasil dicopy.";
            }} catch (error) {{
                const helper = document.createElement("textarea");
                helper.value = promptText;
                helper.style.position = "fixed";
                helper.style.left = "-9999px";
                document.body.appendChild(helper);
                helper.focus();
                helper.select();
                document.execCommand("copy");
                document.body.removeChild(helper);
                statusText.textContent = "Prompt berhasil dicopy.";
            }}
        }}

        button.addEventListener("click", copyPrompt);
        </script>

        <style>
        body {{
            margin: 0;
            background: transparent;
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}

        #copyPromptButton {{
            width: 100%;
            min-height: 44px;
            border: 1px solid #22c55e;
            border-radius: 8px;
            background: #22c55e;
            color: #061008;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
        }}

        #copyPromptButton:hover {{
            background: #16a34a;
            border-color: #16a34a;
        }}

        #copyPromptStatus {{
            min-height: 22px;
            padding-top: 8px;
            color: #86efac;
            font-size: 13px;
        }}
        </style>
        """,
        height=82,
    )


def render_select(label, key, help_text=None):
    current_value = valid_value(key, st.session_state.selected_values[key])
    st.selectbox(
        label,
        labels_for(key),
        index=labels_for(key).index(current_value),
        key=key,
        help=help_text,
    )


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="SJ",
    layout="wide",
)

initialize_state()
apply_custom_style()

st.markdown(
    f"""
    <div class="app-hero">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE} Bisa untuk foto jersey dipakai atlet, mockup produk, detail logo, tampak belakang nama nomor, jersey di kursi stadion, locker room, dan katalog campaign dari desain jersey yang Anda upload.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_step_cards()

st.markdown(
    '<div class="soft-note">Tips utama: upload desain jersey Anda di image generator, lalu gunakan prompt dari aplikasi ini. Prompt sudah mengunci warna, motif, logo, sponsor, nama, nomor, dan detail jersey lainnya agar tidak berubah.</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Mulai Cepat</div>', unsafe_allow_html=True)
preset_columns = st.columns(3)
for index, preset_name in enumerate(QUICK_PRESETS.keys()):
    with preset_columns[index % 3]:
        st.button(
            preset_name,
            use_container_width=True,
            on_click=set_quick_preset,
            args=(preset_name,),
        )

config_column, result_column = st.columns([1.02, 0.98], gap="large")

with config_column:
    with st.container(border=True):
        st.markdown('<div class="section-title">Atur Detail Photoshoot</div>', unsafe_allow_html=True)
        st.caption("Pilihan dibuat dalam bahasa Indonesia. Anda bisa membuat hasil berupa atlet memakai jersey atau mockup detail produk jersey.")

        render_select("Jenis olahraga", "olahraga", "Pilih cabang olahraga utama untuk jersey ini.")
        render_select("Jenis hasil foto", "tampilan_foto", "Pilih apakah jersey dipakai model atau ditampilkan sebagai detail produk.")
        render_select("Tema detail produk", "tema_produk", "Cocok untuk mockup jersey, katalog, presentasi klien, atau promosi.")

        tab_subject, tab_scene, tab_style = st.tabs(["Model & Pose", "Lokasi & Foto", "Style & Output"])

        with tab_subject:
            render_select("Jenis model", "jenis_model", "Siapa yang memakai jersey.")
            render_select("Jumlah model", "jumlah_model", "Jumlah orang di dalam foto.")
            render_select("Pose", "pose", "Gerakan atau posisi tubuh model.")
            render_select("Ekspresi", "ekspresi", "Mood wajah model.")

        with tab_scene:
            render_select("Komposisi foto", "komposisi", "Cara foto disusun agar jersey tetap terlihat jelas.")
            render_select("Background / latar sport", "background", "Lokasi photoshoot bertema olahraga.")
            render_select("Lighting", "lighting", "Arah dan rasa pencahayaan.")
            render_select("Camera angle", "camera_angle", "Sudut pengambilan kamera.")

        with tab_style:
            render_select("Lens look", "lens_look", "Karakter lensa dan kedalaman foto.")
            render_select("Outfit / bawahan", "outfit", "Bawahan dan styling pendukung.")
            render_select("Mood photoshoot", "mood", "Rasa visual keseluruhan.")
            render_select("Tipe output", "output", "Rasio gambar akhir.")

        st.text_area(
            "Catatan tambahan opsional",
            key="custom_note",
            placeholder="Contoh: make the jersey front clearly visible, add subtle rain, club announcement style",
            height=90,
        )

        action_column_1, action_column_2 = st.columns(2)
        with action_column_1:
            st.button(
                "Generate Prompt",
                type="primary",
                use_container_width=True,
                on_click=generate_from_current_selection,
            )
        with action_column_2:
            st.button(
                "Generate Random",
                use_container_width=True,
                on_click=set_random_prompt,
            )

prompt_text = st.session_state.generated_prompt

with result_column:
    with st.container(border=True):
        st.markdown('<div class="section-title">Hasil Prompt</div>', unsafe_allow_html=True)
        st.caption("Prompt siap ditempel ke ChatGPT atau image generator bersama desain jersey Anda.")
        st.markdown(
            '<div class="mini-note">Dropdown memakai bahasa Indonesia. Teks prompt dibuat dalam bahasa Inggris supaya lebih mudah dipahami oleh banyak image generator.</div>',
            unsafe_allow_html=True,
        )

        st.text_area(
            "Prompt siap pakai",
            value=prompt_text,
            height=520,
            help="Blok teks ini lalu salin jika ingin copy manual.",
        )

        render_copy_prompt_button(prompt_text)

        with st.expander("Lihat negative prompt otomatis"):
            st.write(NEGATIVE_PROMPT)

with st.sidebar:
    st.markdown("## Ringkasan")
    st.write("Aplikasi ini untuk prompt mockup dan photoshoot jersey olahraga realistis, tidak hanya jersey bola.")
    st.markdown("### Data preset")
    st.write(f"Jenis hasil foto: {len(PRESETS['tampilan_foto'])} pilihan")
    st.write(f"Tema detail produk: {len(PRESETS['tema_produk'])} pilihan")
    st.write(f"Jenis model: {len(PRESETS['jenis_model'])} pilihan")
    st.write(f"Pose: {len(PRESETS['pose'])} pilihan")
    st.write(f"Background: {len(PRESETS['background'])} pilihan")
    st.write(f"Lighting: {len(PRESETS['lighting'])} pilihan")
    st.write(f"Camera angle: {len(PRESETS['camera_angle'])} pilihan")
    st.write(f"Mood: {len(PRESETS['mood'])} pilihan")
    st.write(f"Outfit: {len(PRESETS['outfit'])} pilihan")
    st.write(f"Komposisi: {len(PRESETS['komposisi'])} pilihan")
    st.markdown("### Alur pakai")
    st.write("1. Pilih jenis olahraga.")
    st.write("2. Pilih preset atau klik Generate Random.")
    st.write("3. Upload desain jersey di image generator.")
    st.write("4. Tempel prompt hasil aplikasi.")
    st.markdown("### Instruksi penting")
    st.info(
        "Desain jersey diarahkan agar mengikuti file referensi yang Anda upload, termasuk warna, motif, logo, sponsor, nama, dan nomor."
    )
