import sqlite3
import os
import random
from datetime import datetime, timedelta

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            category TEXT NOT NULL DEFAULT 'human'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pharmacy_id INTEGER NOT NULL,
            category TEXT NOT NULL DEFAULT 'human',
            last_updated_timestamp TEXT NOT NULL,
            FOREIGN KEY (pharmacy_id) REFERENCES pharmacies (id) ON DELETE CASCADE
        )
    """)

    existing = cursor.execute("SELECT COUNT(*) FROM pharmacies").fetchone()[0]
    if existing > 0:
        print(f"Database already contains {existing} pharmacies. Skipping seed.")
        conn.close()
        return

    now = datetime.now()

    human_pharmacies = [
        ("MedPlus Pharmacy - T. Nagar", "No. 18, Usman Road, T. Nagar, Chennai 600017", "+91-44-24341701", 13.0418, 80.2341),
        ("Apollo Pharmacy - Anna Nagar", "No. 120, 2nd Avenue, Anna Nagar, Chennai 600040", "+91-44-26215890", 13.0850, 80.2098),
        ("Netmeds Store - Mylapore", "No. 45, Kutchery Road, Mylapore, Chennai 600004", "+91-44-24641456", 13.0339, 80.2692),
        ("Sri Lakshmi Medicals", "No. 7, Cathedral Road, Gopalapuram, Chennai 600086", "+91-44-28110134", 13.0531, 80.2530),
        ("New Jayam Medicals", "No. 89, Mount Road, Guindy, Chennai 600032", "+91-44-22337821", 13.0067, 80.2206),
        ("Chennai Pharma Hub", "No. 22, G.N. Chetty Road, T. Nagar, Chennai 600017", "+91-44-24354567", 13.0478, 80.2368),
        ("LifeLine Pharmacy", "No. 56, Velachery Main Road, Velachery, Chennai 600042", "+91-44-22435890", 12.9815, 80.2180),
        ("Jan Aushadhi Kendra - Tambaram", "No. 3, GST Road, Tambaram, Chennai 600045", "+91-44-22395678", 12.9249, 80.1278),
        ("Guardian Medicals", "No. 101, 200 Feet Road, Sholinganallur, Chennai 600119", "+91-44-24960345", 12.9010, 80.2270),
        ("Vinayaka Medicals", "No. 14, Arcot Road, Vadapalani, Chennai 600026", "+91-44-24815234", 13.0520, 80.2120),
        ("Raj Pharmacy - Adyar", "No. 33, L.B. Road, Adyar, Chennai 600020", "+91-44-24407812", 13.0062, 80.2573),
        ("KM Medicals", "No. 67, Poonamallee High Road, Kilpauk, Chennai 600010", "+91-44-26424590", 13.0789, 80.2422),
        ("Arogya Pharmacy", "No. 5, Nungambakkam High Road, Chennai 600034", "+91-44-28271678", 13.0610, 80.2450),
        ("Porur Medical Centre", "No. 28, Porur Main Road, Porur, Chennai 600116", "+91-44-24762345", 13.0358, 80.1576),
        ("Sai Medicals - Perambur", "No. 9, Broadway, Perambur, Chennai 600011", "+91-44-25375890", 13.1108, 80.2490),
        ("Sri Balaji Medicals", "No. 41, Bazaar Road, Mylapore, Chennai 600004", "+91-44-24989012", 13.0345, 80.2701),
        ("Chennai Medical Store - Chromepet", "No. 17, GST Road, Chromepet, Chennai 600044", "+91-44-22380901", 12.9516, 80.1416),
        ("Muthulakshmi Medicals", "No. 83, Anna Salai, Teynampet, Chennai 600018", "+91-44-24343456", 13.0445, 80.2498),
        ("Health First Pharmacy - ECR", "No. 12, ECR Road, Thiruvanmiyur, Chennai 600041", "+91-44-24425678", 12.9832, 80.2598),
        ("Lotus Medicals - Ashok Nagar", "No. 77, 10th Avenue, Ashok Nagar, Chennai 600083", "+91-44-24852190", 13.0380, 80.2115),
        ("Apollo Pharmacy - Besant Nagar", "No. 55, Besant Nagar 3rd Avenue, Chennai 600090", "+91-44-24918201", 13.0005, 80.2668),
        ("Kumaran Medicals - Royapettah", "No. 31, Royapettah High Road, Chennai 600014", "+91-44-28546445", 13.0512, 80.2603),
        ("Anbu Pharmacy", "No. 8, Harrington Road, Chetpet, Chennai 600031", "+91-44-28368910", 13.0715, 80.2445),
        ("Murugan Medicals - Kodambakkam", "No. 62, Arcot Road, Kodambakkam, Chennai 600024", "+91-44-24845567", 13.0489, 80.2218),
        ("Rainbow Pharmacy - Mogappair", "No. 19, Mogappair Main Road, Chennai 600037", "+91-44-26568901", 13.0865, 80.1750),
        ("MedPlus Pharmacy - Ambattur", "No. 44, Ambattur OT Road, Ambattur, Chennai 600053", "+91-44-26546234", 13.1140, 80.1578),
        ("Pallavaram Medical Store", "No. 6, Pallavaram Main Road, Pallavaram, Chennai 600043", "+91-44-22645890", 12.9680, 80.1495),
        ("Sri Ganesh Pharmacy", "No. 91, OMR, Perungudi, Chennai 600096", "+91-44-24964321", 12.9620, 80.2404),
        ("Velu Medicals - Egmore", "No. 23, Egmore High Road, Chennai 600008", "+91-44-28193456", 13.0730, 80.2595),
        ("Selvi Medical Hall", "No. 38, Rajiv Gandhi Salai, Thoraipakkam, Chennai 600097", "+91-44-24978901", 12.9340, 80.2285),
        ("City Pharmacy - Nungambakkam", "No. 115, Sterling Road, Nungambakkam, Chennai 600034", "+91-44-28277890", 13.0635, 80.2420),
        ("Grace Medicals - Triplicane", "No. 71, Triplicane High Road, Chennai 600005", "+91-44-28544890", 13.0580, 80.2730),
        ("Thirumurugan Medical Store", "No. 15, Madipakkam Main Road, Madipakkam, Chennai 600091", "+91-44-22485678", 12.9631, 80.1968),
        ("Saravana Pharmacy - K.K. Nagar", "No. 47, K.K. Nagar Main Road, Chennai 600078", "+91-44-24896789", 13.0340, 80.2080),
        ("Green Cross Medicals", "No. 82, 100 Feet Road, Guindy, Chennai 600032", "+91-44-22361234", 13.0095, 80.2130),
        ("Wellness Pharmacy - Alwarpet", "No. 29, TTK Road, Alwarpet, Chennai 600018", "+91-44-24349678", 13.0384, 80.2536),
        ("Sri Ram Medicals - Avadi", "No. 103, Avadi Main Road, Avadi, Chennai 600054", "+91-44-26546789", 13.1145, 80.1068),
        ("Durga Pharmacy - Madhavaram", "No. 53, Madhavaram High Road, Chennai 600060", "+91-44-25800123", 13.1480, 80.2310),
        ("Shanmuga Medicals - Medavakkam", "No. 16, Medavakkam Main Road, Chennai 600100", "+91-44-22810234", 12.9190, 80.1918),
        ("New Life Pharmacy - Purasawalkam", "No. 74, Purasawalkam High Road, Chennai 600007", "+91-44-26426789", 13.0825, 80.2520),
        ("Siddha Pharmacy - Washermanpet", "No. 36, Thambu Chetty Street, Washermanpet, Chennai 600021", "+91-44-25985123", 13.1150, 80.2810),
        ("Priya Medicals - Nanganallur", "No. 58, Nanganallur Main Road, Chennai 600061", "+91-44-22564890", 12.9790, 80.1850),
        ("Sakthi Medical Store - Pammal", "No. 21, Pammal Main Road, Pammal, Chennai 600075", "+91-44-22436123", 12.9600, 80.1305),
        ("Royal Pharmacy - Neelankarai", "No. 87, ECR, Neelankarai, Chennai 600115", "+91-44-24496789", 12.9510, 80.2588),
        ("Kavitha Medicals - Saidapet", "No. 42, Bridge Road, Saidapet, Chennai 600015", "+91-44-24322345", 13.0215, 80.2285),
        ("Mahalakshmi Pharmacy", "No. 11, Alandur Main Road, Alandur, Chennai 600016", "+91-44-22423456", 13.0020, 80.2058),
        ("Star Medicals - Thiruvanmiyur", "No. 95, Thiruvanmiyur Main Road, Chennai 600041", "+91-44-24441678", 12.9860, 80.2578),
        ("Ponni Pharmacy - Palavakkam", "No. 64, ECR, Palavakkam, Chennai 600041", "+91-44-24468345", 12.9710, 80.2583),
        ("Universal Medical Store", "No. 30, OMR, Navalur, Chennai 600130", "+91-44-47983456", 12.8460, 80.2265),
        ("Family Pharmacy - Perungalathur", "No. 26, Perungalathur Main Road, Chennai 600063", "+91-44-22477234", 12.9040, 80.0980),
    ]

    pet_pharmacies = [
        ("Chennai Pet Clinic & Pharmacy", "No. 12, Montieth Road, Egmore, Chennai 600008", "+91-44-28190345", 13.0720, 80.2580),
        ("Dr. Paws Veterinary Pharmacy", "No. 45, Anna Nagar West, Chennai 600040", "+91-44-26256789", 13.0890, 80.2020),
        ("Happy Tails Vet Store", "No. 8, Velachery, Chennai 600042", "+91-44-22447890", 12.9790, 80.2185),
        ("PetCare Plus - Adyar", "No. 33, Adyar Main Road, Chennai 600020", "+91-44-24452345", 13.0048, 80.2560),
        ("Animal Aid Pharmacy", "No. 71, Mylapore, Chennai 600004", "+91-44-24984567", 13.0350, 80.2680),
        ("VetMed Store - T. Nagar", "No. 19, T. Nagar, Chennai 600017", "+91-44-24364321", 13.0430, 80.2350),
        ("Furry Friends Pharmacy", "No. 55, Nungambakkam, Chennai 600034", "+91-44-28284567", 13.0598, 80.2435),
        ("Dr. Vet Clinic & Pharmacy", "No. 25, ECR, Thiruvanmiyur, Chennai 600041", "+91-44-24437890", 12.9850, 80.2595),
        ("Pet Health Medicals", "No. 41, Porur, Chennai 600116", "+91-44-24769012", 13.0350, 80.1590),
        ("Paws & Claws Store", "No. 63, Alwarpet, Chennai 600018", "+91-44-24353456", 13.0395, 80.2540),
        ("Sri Vignesh Vet Pharmacy", "No. 37, Ashok Nagar, Chennai 600083", "+91-44-24857890", 13.0370, 80.2105),
        ("PetZone Medicals - OMR", "No. 14, OMR, Perungudi, Chennai 600096", "+91-44-24962345", 12.9635, 80.2398),
        ("Vet Plus Pharmacy", "No. 82, Tambaram, Chennai 600045", "+91-44-22387890", 12.9260, 80.1285),
        ("Animal Care Centre", "No. 29, Kodambakkam, Chennai 600024", "+91-44-24849567", 13.0495, 80.2225),
        ("Companion Pet Store", "No. 16, Besant Nagar, Chennai 600090", "+91-44-24928123", 13.0010, 80.2672),
    ]

    all_pharmacies = []
    for p in human_pharmacies:
        all_pharmacies.append(p + ("human",))
    for p in pet_pharmacies:
        all_pharmacies.append(p + ("pet",))

    cursor.executemany(
        "INSERT INTO pharmacies (name, address, phone, lat, lng, category) VALUES (?, ?, ?, ?, ?, ?)",
        all_pharmacies
    )

    human_medicine_names = [
        "Dolo 650",
        "Paracetamol 500mg",
        "Crocin Advance",
        "Cetirizine 10mg",
        "Amoxicillin 250mg",
        "Azithromycin 500mg",
        "Ibuprofen 400mg",
        "Omeprazole 20mg",
        "Pan-D",
        "Montair LC",
        "Metformin 500mg",
        "Aspirin 75mg",
        "Augmentin 625",
        "Shelcal 500",
        "Combiflam",
        "Allegra 120mg",
        "Sinarest",
        "Vicks Action 500",
        "ORS Sachets",
        "Digene",
        "Rantac 150",
        "Disprin",
        "Becosules",
        "Limcee",
        "Volini Gel",
    ]

    pet_medicine_names = [
        "Drontal Plus (Dewormer)",
        "Frontline Plus (Flea & Tick)",
        "Fipronil Spray",
        "Meloxicam Oral (Pet Pain Relief)",
        "Amoxicillin Pet Drops",
        "Metronidazole Pet Suspension",
        "Ivermectin Tablets",
        "Cephalexin Pet Capsules",
        "Prednisolone Pet Tablets",
        "Pet ORS Powder",
        "Calcium Pet Supplement",
        "Nutri-Coat Pet Multivitamin",
        "Dermivet Medicated Shampoo",
        "Pet Eye Drops (Ciprofloxacin)",
        "Tick & Flea Collar",
    ]

    random.seed(42)
    medicines = []

    human_pharmacy_count = len(human_pharmacies)
    for med_name in human_medicine_names:
        num_shops = random.randint(8, 20)
        shop_ids = random.sample(range(1, human_pharmacy_count + 1), min(num_shops, human_pharmacy_count))
        for shop_id in shop_ids:
            hours_ago = random.randint(1, 48)
            timestamp = (now - timedelta(hours=hours_ago)).strftime("%Y-%m-%d %H:%M:%S")
            medicines.append((med_name, shop_id, "human", timestamp))

    pet_start_id = human_pharmacy_count + 1
    pet_pharmacy_count = len(pet_pharmacies)
    for med_name in pet_medicine_names:
        num_shops = random.randint(5, 12)
        shop_ids = random.sample(range(pet_start_id, pet_start_id + pet_pharmacy_count), min(num_shops, pet_pharmacy_count))
        for shop_id in shop_ids:
            hours_ago = random.randint(1, 48)
            timestamp = (now - timedelta(hours=hours_ago)).strftime("%Y-%m-%d %H:%M:%S")
            medicines.append((med_name, shop_id, "pet", timestamp))

    cursor.executemany(
        "INSERT INTO medicines (name, pharmacy_id, category, last_updated_timestamp) VALUES (?, ?, ?, ?)",
        medicines
    )

    conn.commit()
    conn.close()

    print(f"Database initialized at {DATABASE}")
    print(f"  -> {len(human_pharmacies)} human pharmacies")
    print(f"  -> {len(pet_pharmacies)} pet pharmacies")
    print(f"  -> {len(human_pharmacies) + len(pet_pharmacies)} total pharmacies")
    print(f"  -> {len(human_medicine_names)} human medicines")
    print(f"  -> {len(pet_medicine_names)} pet medicines")
    print(f"  -> {len(medicines)} total medicine entries")


if __name__ == '__main__':
    init_db()
