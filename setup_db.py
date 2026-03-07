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
        ("MedPlus Pharmacy", "No. 18, Mission Street, White Town, Puducherry 605001", "+91-413-2336701", 11.9344, 79.8300),
        ("Apollo Pharmacy - JN Street", "No. 120, Jawaharlal Nehru Street, Puducherry 605001", "+91-413-2225890", 11.9352, 79.8289),
        ("Netmeds Store", "No. 45, Rangapillai Street, Puducherry 605001", "+91-413-2331456", 11.9340, 79.8285),
        ("Sri Lakshmi Medicals", "No. 7, Kamaraj Salai, White Town, Puducherry 605001", "+91-413-2220134", 11.9330, 79.8312),
        ("New Jayam Medicals", "No. 89, Mahatma Gandhi Road, Puducherry 605001", "+91-413-2337821", 11.9365, 79.8274),
        ("Pondy Pharma", "No. 22, Lal Bahadur Shastri Street, Puducherry 605001", "+91-413-2224567", 11.9380, 79.8260),
        ("LifeLine Pharmacy", "No. 56, Anna Nagar, Puducherry 605005", "+91-413-2255890", 11.9450, 79.8150),
        ("Jan Aushadhi Kendra", "No. 3, Mudaliarpet Main Road, Puducherry 605004", "+91-413-2245678", 11.9280, 79.8190),
        ("Guardian Medicals", "No. 101, 100 Feet Road, Puducherry 605004", "+91-413-2260345", 11.9270, 79.8170),
        ("Vinayaka Medicals", "No. 14, Villianur Main Road, Puducherry 605110", "+91-413-2615234", 11.9200, 79.7980),
        ("Raj Pharmacy", "No. 33, Ariyankuppam Road, Puducherry 605007", "+91-413-2607812", 11.9150, 79.8260),
        ("KM Medicals", "No. 67, Bussy Street, Puducherry 605001", "+91-413-2334590", 11.9348, 79.8295),
        ("Arogya Pharmacy", "No. 5, Romain Rolland Street, Puducherry 605001", "+91-413-2221678", 11.9335, 79.8305),
        ("Reddiarpalayam Medical Centre", "No. 28, Reddiarpalayam Main Road, Puducherry 605010", "+91-413-2272345", 11.9410, 79.8100),
        ("Sai Medicals", "No. 9, Lawspet Main Road, Puducherry 605008", "+91-413-2275890", 11.9530, 79.8080),
        ("Sri Balaji Medicals", "No. 41, Cathedral Street, Puducherry 605001", "+91-413-2339012", 11.9356, 79.8278),
        ("Pondicherry Medical Store", "No. 17, Cuddalore Road, Puducherry 605005", "+91-413-2250901", 11.9460, 79.8120),
        ("Muthulakshmi Medicals", "No. 83, Nellithope, Puducherry 605005", "+91-413-2253456", 11.9420, 79.8130),
        ("Health First Pharmacy", "No. 12, ECR Road, Puducherry 605101", "+91-413-2645678", 11.9290, 79.8350),
        ("Lotus Medicals", "No. 77, Bharathidasan Nagar, Puducherry 605006", "+91-413-2282190", 11.9490, 79.8200),
        ("Apollo Pharmacy - MG Road", "No. 55, Mahatma Gandhi Road, Puducherry 605001", "+91-413-2338201", 11.9370, 79.8268),
        ("Kumaran Medicals", "No. 31, Muthialpet, Puducherry 605003", "+91-413-2336445", 11.9380, 79.8330),
        ("Anbu Pharmacy", "No. 8, Orleanpet, Puducherry 605001", "+91-413-2228910", 11.9300, 79.8250),
        ("Murugan Medicals", "No. 62, Kuruchikuppam, Puducherry 605012", "+91-413-2335567", 11.9320, 79.8300),
        ("Rainbow Pharmacy", "No. 19, Rainbow Nagar, Puducherry 605011", "+91-413-2268901", 11.9480, 79.8120),
        ("MedPlus Pharmacy - Lawspet", "No. 44, Lawspet, Puducherry 605008", "+91-413-2276234", 11.9540, 79.8060),
        ("Kalapet Medical Store", "No. 6, Kalapet Main Road, Puducherry 605014", "+91-413-2655890", 11.9600, 79.7950),
        ("Sri Ganesh Pharmacy", "No. 91, Solai Nagar, Puducherry 605005", "+91-413-2254321", 11.9440, 79.8180),
        ("Velu Medicals", "No. 23, Vambakeerapalayam, Puducherry 605001", "+91-413-2233456", 11.9360, 79.8310),
        ("Selvi Medical Hall", "No. 38, Kottakuppam, Puducherry 605104", "+91-413-2648901", 11.9260, 79.8380),
        ("City Pharmacy", "No. 115, Anna Salai, Puducherry 605001", "+91-413-2337890", 11.9355, 79.8275),
        ("Grace Medicals", "No. 71, Goubert Avenue, Puducherry 605001", "+91-413-2224890", 11.9330, 79.8340),
        ("Thirumurugan Medical Store", "No. 15, Thengaithittu, Puducherry 605004", "+91-413-2605678", 11.9180, 79.8300),
        ("Saravana Pharmacy", "No. 47, Mudaliarpet Bazaar, Puducherry 605004", "+91-413-2246789", 11.9275, 79.8200),
        ("Green Cross Medicals", "No. 82, 100 Feet Road, Puducherry 605004", "+91-413-2261234", 11.9265, 79.8160),
        ("Wellness Pharmacy", "No. 29, Uppalam Road, Puducherry 605001", "+91-413-2229678", 11.9395, 79.8240),
        ("Sri Ram Medicals", "No. 103, Villianur Road, Puducherry 605110", "+91-413-2616789", 11.9210, 79.7990),
        ("Durga Pharmacy", "No. 53, Sedarapet, Puducherry 605106", "+91-413-2670123", 11.9580, 79.7900),
        ("Shanmuga Medicals", "No. 16, Bahour Road, Puducherry 605402", "+91-413-2690234", 11.9100, 79.8100),
        ("New Life Pharmacy", "No. 74, Nehru Street Extension, Puducherry 605001", "+91-413-2226789", 11.9348, 79.8280),
        ("Siddha Pharmacy", "No. 36, Bharathi Street, Puducherry 605001", "+91-413-2335123", 11.9345, 79.8265),
        ("Priya Medicals", "No. 58, Nellithope Main Road, Puducherry 605005", "+91-413-2254890", 11.9425, 79.8140),
        ("Sakthi Medical Store", "No. 21, Anna Nagar 2nd Cross, Puducherry 605005", "+91-413-2256123", 11.9455, 79.8160),
        ("Royal Pharmacy", "No. 87, ECR Junction, Puducherry 605101", "+91-413-2646789", 11.9285, 79.8360),
        ("Kavitha Medicals", "No. 42, Cluny Embankment Road, Puducherry 605001", "+91-413-2222345", 11.9338, 79.8325),
        ("Mahalakshmi Pharmacy", "No. 11, Reddiarpalayam, Puducherry 605010", "+91-413-2273456", 11.9405, 79.8110),
        ("Star Medicals", "No. 95, Cuddalore Road, Puducherry 605005", "+91-413-2251678", 11.9470, 79.8110),
        ("Ponni Pharmacy", "No. 64, Ariyankuppam, Puducherry 605007", "+91-413-2608345", 11.9160, 79.8270),
        ("Universal Medical Store", "No. 30, Bharathidasan Nagar, Puducherry 605006", "+91-413-2283456", 11.9485, 79.8190),
        ("Family Pharmacy", "No. 26, Muthialpet Main Road, Puducherry 605003", "+91-413-2337234", 11.9385, 79.8320),
    ]

    pet_pharmacies = [
        ("Pondy Pet Clinic & Pharmacy", "No. 12, MG Road, Puducherry 605001", "+91-413-2220345", 11.9360, 79.8272),
        ("Dr. Paws Veterinary Pharmacy", "No. 45, Anna Nagar Main Road, Puducherry 605005", "+91-413-2256789", 11.9448, 79.8155),
        ("Happy Tails Vet Store", "No. 8, Lawspet, Puducherry 605008", "+91-413-2277890", 11.9535, 79.8075),
        ("PetCare Plus", "No. 33, 100 Feet Road, Pudaliarpet, Puducherry 605004", "+91-413-2262345", 11.9268, 79.8175),
        ("Animal Aid Pharmacy", "No. 71, Nellithope, Puducherry 605005", "+91-413-2254567", 11.9418, 79.8135),
        ("VetMed Store", "No. 19, Bharathidasan Nagar, Puducherry 605006", "+91-413-2284321", 11.9492, 79.8195),
        ("Furry Friends Pharmacy", "No. 55, Reddiarpalayam, Puducherry 605010", "+91-413-2274567", 11.9408, 79.8105),
        ("Dr. Vet Clinic & Pharmacy", "No. 25, ECR Road, Puducherry 605101", "+91-413-2647890", 11.9292, 79.8355),
        ("Pet Health Medicals", "No. 41, Rainbow Nagar, Puducherry 605011", "+91-413-2269012", 11.9478, 79.8118),
        ("Paws & Claws Store", "No. 63, White Town, Puducherry 605001", "+91-413-2223456", 11.9332, 79.8308),
        ("Sri Vignesh Vet Pharmacy", "No. 37, Mudaliarpet Main Road, Puducherry 605004", "+91-413-2247890", 11.9278, 79.8195),
        ("PetZone Medicals", "No. 14, Cuddalore Road, Puducherry 605005", "+91-413-2252345", 11.9462, 79.8115),
        ("Vet Plus Pharmacy", "No. 82, Villianur Road, Puducherry 605110", "+91-413-2617890", 11.9205, 79.7985),
        ("Animal Care Centre", "No. 29, Orleanpet, Puducherry 605001", "+91-413-2229567", 11.9305, 79.8255),
        ("Companion Pet Store", "No. 16, Muthialpet, Puducherry 605003", "+91-413-2338123", 11.9382, 79.8325),
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
