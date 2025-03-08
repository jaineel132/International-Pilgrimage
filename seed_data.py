from app import create_app
from extensions import db
from models import Pilgrimage

def seed_pilgrimages():
    pilgrimages = [
       {
    'name': 'Santiago de Compostela',
    'location': 'Galicia, Spain',
    'description': 'The endpoint of the Camino de Santiago, a famous Christian pilgrimage route to the shrine of St. James.',
    'duration': '1-4 weeks (depending on the route)',
    'best_time': 'Spring or Fall',
    'image_url': '/static/images/santiago.jpg'
},
{
    'name': 'Mecca',
    'location': 'Saudi Arabia',
    'description': 'The holiest city in Islam, visited during the Hajj pilgrimage, a pillar of Islamic faith.',
    'duration': '5-7 days',
    'best_time': 'During the annual Hajj season',
    'image_url': 'https://example.com/mecca.jpg'
},
{
    'name': 'Varanasi',
    'location': 'Uttar Pradesh, India',
    'description': 'A sacred city on the Ganges River, important in Hinduism and known for its ghats and temples.',
    'duration': '2-4 days',
    'best_time': 'October to March',
    'image_url': 'https://example.com/varanasi.jpg'
},
{
    'name': 'Lourdes',
    'location': 'Hautes-Pyrénées, France',
    'description': 'A Catholic pilgrimage site known for its Marian apparitions and healing waters.',
    'duration': '2-3 days',
    'best_time': 'April to October',
    'image_url': 'https://example.com/lourdes.jpg'
},
{
    'name': 'Bodh Gaya',
    'location': 'Bihar, India',
    'description': 'The place where Siddhartha Gautama attained enlightenment under the Bodhi Tree.',
    'duration': '1-3 days',
    'best_time': 'October to February',
    'image_url': 'https://example.com/bodhgaya.jpg'
},
{
    'name': 'Golden Temple',
    'location': 'Amritsar, India',
    'description': 'The holiest site in Sikhism, also known as Harmandir Sahib, famous for its gold-plated structure.',
    'duration': '1-2 days',
    'best_time': 'November to March',
    'image_url': 'https://example.com/goldentemple.jpg'
},
{
    'name': 'Western Wall',
    'location': 'Jerusalem, Israel',
    'description': 'A sacred site for Jewish prayer, believed to be the last remnant of the Second Temple.',
    'duration': '1-2 days',
    'best_time': 'Year-round',
    'image_url': 'https://example.com/westernwall.jpg'
},
{
    'name': 'Mount Kailash',
    'location': 'Tibet, China',
    'description': 'A sacred peak for Hindus, Buddhists, Jains, and Bon followers, associated with divine powers.',
    'duration': '2-3 weeks (including travel)',
    'best_time': 'May to September',
    'image_url': 'https://example.com/mountkailash.jpg'
},
{
    'name': 'Medina',
    'location': 'Saudi Arabia',
    'description': 'The city of the Prophet Muhammad and home to Al-Masjid an-Nabawi, his burial place.',
    'duration': '2-3 days',
    'best_time': 'Year-round (except during peak Hajj season)',
    'image_url': 'https://example.com/medina.jpg'
},
{
    'name': 'Rameswaram',
    'location': 'Tamil Nadu, India',
    'description': 'A sacred Hindu site associated with Lord Rama and the Ramanathaswamy Temple.',
    'duration': '2-4 days',
    'best_time': 'October to April',
    'image_url': 'https://example.com/rameswaram.jpg'
},
{
    'name': 'Jerusalem',
    'location': 'Israel',
    'description': 'A holy city for Judaism, Christianity, and Islam, featuring sites like the Church of the Holy Sepulchre and Dome of the Rock.',
    'duration': '3-5 days',
    'best_time': 'Spring or Fall',
    'image_url': 'https://example.com/jerusalem.jpg'
},
{
    'name': 'Shikoku Pilgrimage',
    'location': 'Shikoku Island, Japan',
    'description': 'A Buddhist pilgrimage that spans 88 temples dedicated to Kobo Daishi.',
    'duration': '1-2 months (full circuit)',
    'best_time': 'Spring or Fall',
    'image_url': 'https://example.com/shikoku.jpg'
},
{
    'name': 'Karbala',
    'location': 'Iraq',
    'description': 'A holy city for Shia Muslims, home to the shrine of Imam Hussein.',
    'duration': '2-3 days',
    'best_time': 'During Arbaeen (40 days after Ashura)',
    'image_url': 'https://example.com/karbala.jpg'
},
{
    'name': 'Chartres Cathedral',
    'location': 'Chartres, France',
    'description': 'A UNESCO World Heritage Site and an important Marian pilgrimage destination.',
    'duration': '1-2 days',
    'best_time': 'April to October',
    'image_url': 'https://example.com/chartres.jpg'
},
{
    'name': 'Fatima',
    'location': 'Portugal',
    'description': 'A Marian pilgrimage site where apparitions of the Virgin Mary were reported in 1917.',
    'duration': '2-3 days',
    'best_time': 'May to October',
    'image_url': 'https://example.com/fatima.jpg'
},
{
    'name': 'Tirupati',
    'location': 'Andhra Pradesh, India',
    'description': 'Home to the Tirumala Venkateswara Temple, one of the wealthiest and most visited Hindu temples.',
    'duration': '1-3 days',
    'best_time': 'September to February',
    'image_url': 'https://example.com/tirupati.jpg'
},
{
    'name': 'Mount Sinai',
    'location': 'Egypt',
    'description': 'Believed to be the biblical mountain where Moses received the Ten Commandments.',
    'duration': '1-2 days',
    'best_time': 'March to May or September to November',
    'image_url': 'https://example.com/mountsinai.jpg'
},
{
    'name': 'Ise Grand Shrine',
    'location': 'Mie Prefecture, Japan',
    'description': 'The most sacred Shinto shrine, dedicated to the sun goddess Amaterasu.',
    'duration': '1-2 days',
    'best_time': 'Spring or Fall',
    'image_url': 'https://example.com/ise.jpg'
},
{
    'name': 'Canterbury Cathedral',
    'location': 'Canterbury, England',
    'description': 'A significant Christian pilgrimage site, associated with St. Thomas Becket.',
    'duration': '1-2 days',
    'best_time': 'April to September',
    'image_url': 'https://example.com/canterbury.jpg'
},
{
    'name': 'Ajmer Sharif Dargah',
    'location': 'Ajmer, India',
    'description': 'The shrine of Sufi saint Moinuddin Chishti, a major pilgrimage for Muslims and people of all faiths.',
    'duration': '1-2 days',
    'best_time': 'October to March',
    'image_url': 'https://example.com/ajmer.jpg'
},
{
    'name': 'Adam’s Peak (Sri Pada)',
    'location': 'Sri Lanka',
    'description': 'A sacred site for Buddhists, Hindus, Muslims, and Christians, known for the footprint-shaped mark at its summit.',
    'duration': '1-2 days',
    'best_time': 'December to May',
    'image_url': 'https://example.com/adamspeak.jpg'
},
{
    'name': 'Kumano Kodo',
    'location': 'Wakayama, Japan',
    'description': 'A network of ancient pilgrimage routes leading to the Kumano Sanzan shrines.',
    'duration': '3-7 days',
    'best_time': 'Spring or Fall',
    'image_url': 'https://example.com/kumanokodo.jpg'
},
{
    'name': 'Pashupatinath Temple',
    'location': 'Kathmandu, Nepal',
    'description': 'A sacred Hindu temple dedicated to Lord Shiva, located along the Bagmati River.',
    'duration': '1-2 days',
    'best_time': 'October to March',
    'image_url': 'https://example.com/pashupatinath.jpg'
},
{
    'name': 'Mount Athos',
    'location': 'Greece',
    'description': 'An Orthodox Christian monastic state, accessible only to male pilgrims.',
    'duration': '3-5 days',
    'best_time': 'April to October',
    'image_url': 'https://example.com/athos.jpg'
},
{
    'name': 'Sri Harmandir Sahib (Golden Temple)',
    'location': 'Amritsar, India',
    'description': 'The holiest gurdwara of Sikhism, attracting millions of devotees worldwide.',
    'duration': '1-2 days',
    'best_time': 'November to March',
    'image_url': 'https://example.com/goldentemple.jpg'
},
{
    'name': 'Saint Catherine’s Monastery',
    'location': 'Sinai, Egypt',
    'description': 'A UNESCO World Heritage Site at the base of Mount Sinai, linked to Moses and the Burning Bush.',
    'duration': '1-2 days',
    'best_time': 'March to May or September to November',
    'image_url': 'https://example.com/catherine.jpg'
},
{
    'name': 'Vaishno Devi',
    'location': 'Jammu and Kashmir, India',
    'description': 'A Hindu pilgrimage site dedicated to Goddess Vaishno Devi, nestled in the Trikuta Mountains.',
    'duration': '2-3 days',
    'best_time': 'March to October',
    'image_url': 'https://example.com/vaishnodevi.jpg'
},
{
    'name': 'Chichen Itza',
    'location': 'Yucatán, Mexico',
    'description': 'An ancient Mayan pilgrimage center with the iconic Temple of Kukulcán.',
    'duration': '1-2 days',
    'best_time': 'November to March',
    'image_url': 'https://example.com/chichenitza.jpg'
}

    ]

    for pilgrimage_data in pilgrimages:
        pilgrimage = Pilgrimage(**pilgrimage_data)
        db.session.add(pilgrimage)
    
    db.session.commit()
    print("Sample pilgrimages have been added to the database.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_pilgrimages()

