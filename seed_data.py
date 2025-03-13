from app import create_app
from extensions import db
from models import Pilgrimage

def seed_pilgrimages():
    
    db.session.query(Pilgrimage).delete()
    
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
    'image_url': '/static/images/mecca.jpg'
},
{
    'name': 'Varanasi',
    'location': 'Uttar Pradesh, India',
    'description': 'A sacred city on the Ganges River, important in Hinduism and known for its ghats and temples.',
    'duration': '2-4 days',
    'best_time': 'October to March',
    'image_url': 'https://t4.ftcdn.net/jpg/04/08/25/05/360_F_408250543_MVaEVGeWxb4FiFy7mEGKj8nfYkwoAZON.jpg'
},
{
    'name': 'Lourdes',
    'location': 'Hautes-Pyrénées, France',
    'description': 'A Catholic pilgrimage site known for its Marian apparitions and healing waters.',
    'duration': '2-3 days',
    'best_time': 'April to October',
    'image_url': 'https://media.istockphoto.com/id/602326164/photo/rosary-basilica-in-the-evening-in-lourdes.jpg?s=612x612&w=0&k=20&c=EbiRi7PQtb8te__k-bZ1Q52qVv_QUAEvfWewomnhu1w='
},
{
    'name': 'Bodh Gaya',
    'location': 'Bihar, India',
    'description': 'The place where Siddhartha Gautama attained enlightenment under the Bodhi Tree.',
    'duration': '1-3 days',
    'best_time': 'October to February',
    'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTjZuBEb0S9UeyqHCWcRSeBkm5e2-m1h-OCeg&s'
},
{
    'name': 'Golden Temple',
    'location': 'Amritsar, India',
    'description': 'The holiest site in Sikhism, also known as Harmandir Sahib, famous for its gold-plated structure.',
    'duration': '1-2 days',
    'best_time': 'November to March',
    'image_url': 'https://plus.unsplash.com/premium_photo-1697730324062-c012bc98eb13?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Z29sZGVuJTIwdGVtcGxlJTIwYW1yaXRzYXJ8ZW58MHx8MHx8fDA%3D'
},
{
    'name': 'Western Wall',
    'location': 'Jerusalem, Israel',
    'description': 'A sacred site for Jewish prayer, believed to be the last remnant of the Second Temple.',
    'duration': '1-2 days',
    'best_time': 'Year-round',
    'image_url': 'https://media.istockphoto.com/id/852178720/photo/jerusalem-wailing-wall-sunset.jpg?s=612x612&w=0&k=20&c=GqpDHsOIHFIZb7tPgrxjWJgcTB8zIDaV2H4LEPBRVEg='
},
{
    'name': 'Mount Kailash',
    'location': 'Tibet, China',
    'description': 'A sacred peak for Hindus, Buddhists, Jains, and Bon followers, associated with divine powers.',
    'duration': '2-3 weeks (including travel)',
    'best_time': 'May to September',
    'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpDRmR6SbsAE03puggzv4AzViyFHUm0s-TGA&s'
},
{
    'name': 'Medina',
    'location': 'Saudi Arabia',
    'description': 'The city of the Prophet Muhammad and home to Al-Masjid an-Nabawi, his burial place.',
    'duration': '2-3 days',
    'best_time': 'Year-round (except during peak Hajj season)',
    'image_url': 'https://media.istockphoto.com/id/688494594/photo/al-masjid-al-nabawi.jpg?s=612x612&w=0&k=20&c=wTrVBpUP3yB_TY1OZowiVKynWqfdol0MoIY9ZcItYoo='
},
{
    'name': 'Rameswaram',
    'location': 'Tamil Nadu, India',
    'description': 'A sacred Hindu site associated with Lord Rama and the Ramanathaswamy Temple.',
    'duration': '2-4 days',
    'best_time': 'October to April',
    'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf5EmImNe-LQEgNsllajvhI4hflOhWApwcNw&s'
},
{
    'name': 'Jerusalem',
    'location': 'Israel',
    'description': 'A holy city for Judaism, Christianity, and Islam, featuring sites like the Church of the Holy Sepulchre and Dome of the Rock.',
    'duration': '3-5 days',
    'best_time': 'Spring or Fall',
    'image_url': 'https://media.istockphoto.com/id/475018163/photo/view-to-jerusalem-old-city-israel.jpg?s=612x612&w=0&k=20&c=KohVcIp169PEnDSUS4IkAH7VEzfe3XbJ7b3994FD0yY='
},
{
    'name': 'Shikoku Pilgrimage',
    'location': 'Shikoku Island, Japan',
    'description': 'A Buddhist pilgrimage that spans 88 temples dedicated to Kobo Daishi.',
    'duration': '1-2 months (full circuit)',
    'best_time': 'Spring or Fall',
    'image_url': 'https://i.natgeofe.com/n/a0fa2967-ab95-453d-9afd-56a5a7f46182/STOCK_MF4105_2405_GettyImages-1300064416.jpg'
},
{
    'name': 'Karbala',
    'location': 'Iraq',
    'description': 'A holy city for Shia Muslims, home to the shrine of Imam Hussein.',
    'duration': '2-3 days',
    'best_time': 'During Arbaeen (40 days after Ashura)',
    'image_url': 'https://www.reviewofreligions.org/wp-content/uploads/2022/08/Karbala-small-shutterstock_1540235519.jpeg'
},
{
    'name': 'Chartres Cathedral',
    'location': 'Chartres, France',
    'description': 'A UNESCO World Heritage Site and an important Marian pilgrimage destination.',
    'duration': '1-2 days',
    'best_time': 'April to October',
    'image_url': 'https://media.istockphoto.com/id/954059700/photo/south-side-of-chartres-cathedral.jpg?s=612x612&w=0&k=20&c=sgF7b5ByN8hq75QGs5KLGebKcS862-RhFORj0H9pU04='
},
{
    'name': 'Fatima',
    'location': 'Portugal',
    'description': 'A Marian pilgrimage site where apparitions of the Virgin Mary were reported in 1917.',
    'duration': '2-3 days',
    'best_time': 'May to October',
    'image_url': 'https://joewalshtours.ie/app/uploads/2021/07/Our-Lady-of-Fatima-sanctuary-pilgrimage-Portugal-Joe-Walsh-Tours-Pilgrimages-travel-1024x683.jpg'
},
{
    'name': 'Tirupati',
    'location': 'Andhra Pradesh, India',
    'description': 'Home to the Tirumala Venkateswara Temple, one of the wealthiest and most visited Hindu temples.',
    'duration': '1-3 days',
    'best_time': 'September to February',
    'image_url': 'https://tirupatibalajitravels.co.in/wp-content/uploads/2024/02/special-entry-darshan-1.webp'
},
{
    'name': 'Mount Sinai',
    'location': 'Egypt',
    'description': 'Believed to be the biblical mountain where Moses received the Ten Commandments.',
    'duration': '1-2 days',
    'best_time': 'March to May or September to November',
    'image_url': 'https://thewanderingafro.com/wp-content/uploads/2023/09/Mount_Moses-scaled.jpg'
},
{
    'name': 'Ise Grand Shrine',
    'location': 'Mie Prefecture, Japan',
    'description': 'The most sacred Shinto shrine, dedicated to the sun goddess Amaterasu.',
    'duration': '1-2 days',
    'best_time': 'Spring or Fall',
    'image_url': 'https://www.geoex.com/app/uploads/2019/07/japan-temple-historic-geoex.jpg'
},
{
    'name': 'Canterbury Cathedral',
    'location': 'Canterbury, England',
    'description': 'A significant Christian pilgrimage site, associated with St. Thomas Becket.',
    'duration': '1-2 days',
    'best_time': 'April to September',
    'image_url': 'https://world4.eu/wp-content/uploads/2023/04/canterbury-gateway.webp'
},
{
    'name': 'Ajmer Sharif Dargah',
    'location': 'Ajmer, India',
    'description': 'The shrine of Sufi saint Moinuddin Chishti, a major pilgrimage for Muslims and people of all faiths.',
    'duration': '1-2 days',
    'best_time': 'October to March',
    'image_url': 'https://resources.thomascook.in/images/holidays/sightSeeing/ajmerdargha.jpg'
},
{
    'name': 'Adam`s Peak (Sri Pada)',
    'location': 'Sri Lanka',
    'description': 'A sacred site for Buddhists, Hindus, Muslims, and Christians, known for the footprint-shaped mark at its summit.',
    'duration': '1-2 days',
    'best_time': 'December to May',
    'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI3d9deqDnuX3awaT3XKIhmR7OcYtl69fF9A&s'
},
{
    'name': 'Kumano Kodo',
    'location': 'Wakayama, Japan',
    'description': 'A network of ancient pilgrimage routes leading to the Kumano Sanzan shrines.',
    'duration': '3-7 days',
    'best_time': 'Spring or Fall',
    'image_url': 'https://d2exd72xrrp1s7.cloudfront.net/www/collection/475/1R2aLT?width=768&height=576&crop=true'
},
{
    'name': 'Pashupatinath Temple',
    'location': 'Kathmandu, Nepal',
    'description': 'A sacred Hindu temple dedicated to Lord Shiva, located along the Bagmati River.',
    'duration': '1-2 days',
    'best_time': 'October to March',
    'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoJXVVQdO2JBsB0Wh1nY_kVcxtkdGE27r9xA&s'
},
{
    'name': 'Mount Athos',
    'location': 'Greece',
    'description': 'An Orthodox Christian monastic state, accessible only to male pilgrims.',
    'duration': '3-5 days',
    'best_time': 'April to October',
    'image_url': 'https://cdn.shopify.com/s/files/1/0254/1685/9682/t/5/assets/pf-029be620--holymountain.jpg?v=1601971240'
},
{
    'name': 'Sri Harmandir Sahib (Golden Temple)',
    'location': 'Amritsar, India',
    'description': 'The holiest gurdwara of Sikhism, attracting millions of devotees worldwide.',
    'duration': '1-2 days',
    'best_time': 'November to March',
    'image_url': 'https://s7ap1.scene7.com/is/image/incredibleindia/1-sri-harmandir-sahib-(golden-temple)-amritsar-punjab-attr-hero?qlt=82&ts=1726662069037'
},
{
    'name': 'Saint Catherine`s Monastery',
    'location': 'Sinai, Egypt',
    'description': 'A UNESCO World Heritage Site at the base of Mount Sinai, linked to Moses and the Burning Bush.',
    'duration': '1-2 days',
    'best_time': 'March to May or September to November',
    'image_url': 'https://cdn.britannica.com/51/126951-050-19056A6C/St-Catherines-Monastery-Mount-Sinai-Egypt.jpg'
},
{
    'name': 'Vaishno Devi',
    'location': 'Jammu and Kashmir, India',
    'description': 'A Hindu pilgrimage site dedicated to Goddess Vaishno Devi, nestled in the Trikuta Mountains.',
    'duration': '2-3 days',
    'best_time': 'March to October',
    'image_url': 'https://www.amritara.co.in/blog/admin/assets/img/post/image_2024-11-29-10-36-16_6749992066923.jpg'
},
{
    'name': 'Chichen Itza',
    'location': 'Yucatán, Mexico',
    'description': 'An ancient Mayan pilgrimage center with the iconic Temple of Kukulcán.',
    'duration': '1-2 days',
    'best_time': 'November to March',
    'image_url': 'https://media.istockphoto.com/id/481272289/photo/el-castillo-of-chichen-itza-at-sunset-mexico.jpg?s=612x612&w=0&k=20&c=vp5jlz0SdiCl4ow_xRUPDgZ-09TdRdWuzE4NW7v130c='
}

    ]

    for pilgrimage_data in pilgrimages:
        pilgrimage = Pilgrimage(**pilgrimage_data)
        db.session.add(pilgrimage)
    
    db.session.commit()
    print("Database has been refreshed with pilgrimage data.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_pilgrimages()