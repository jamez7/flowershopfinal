from app import create_app, sql_db
from app.models import Product

# Tworzenie instancji aplikacji Flask
flowerShopFlaskApp = create_app()

# Usuwa stare tabele, tworzy nowe i wypełnia przykładowymi danymi
@flowerShopFlaskApp.cli.command('init-db')
def init_db_command():
    
    sql_db.drop_all()
    sql_db.create_all()

    rose = Product(name='Róża', color='red', image_path='images/rose.png', description='Klasyczny symbol miłości i piękna.', quantity=180)
    lily = Product(name='Lilia', color='white', image_path='images/lily.png', description='Elegancka i pachnąca o dużych, efektownych płatkach.', quantity=65)
    tulip = Product(name='Tulipan', color='yellow', image_path='images/tulip.png', description='Wyraziste kwiaty symbolizujące głęboką miłość i wiosnę.', quantity=45)
    eucalyptus = Product(name='Eukaliptus', color='green', image_path='images/eucalyptus.png', description='Aromatyczne liście dodające wypełnienia i tekstury.', quantity=90)
    daisy = Product(name='Stokrotka', color='white', image_path='images/daisy.png', description='Pogodny kwiat symbolizujący niewinność i czystość.', quantity=30)
    sunflower = Product(name='Słonecznik', color='yellow', image_path='images/sunflower.png', description='Jasny i odważny kwiat oznaczający uwielbienie i lojalność.', quantity=200)
    orchid = Product(name='Storczyk', color='white', image_path='images/orchid.png', description='Egzotyczny i pełen wdzięku symbol luksusu i rzadkiego piękna.', quantity=25)
    carnation = Product(name='Goździk', color='pink', image_path='images/carnation.png', description='Trwały kwiat o falowanych płatkach, oznaczający miłość i fascynację.', quantity=110)
    hydrangea = Product(name='Hortensja', color='blue', image_path='images/hydrangea.png', description='Okazałe, chmurkowate kwiatostany symbolizujące wdzięczność i głębokie emocje.', quantity=75)
    peony = Product(name='Piwonia', color='pink', image_path='images/peony.png', description='Pachnąca, bujna piwonia będąca symbolem romansu i dostatku.', quantity=50)
    lavender = Product(name='Lawenda', color='purple', image_path='images/lavender.png', description='Aromatyczne fioletowe kwiatostany znane z kojącego zapachu i symbolu oddania.', quantity=0)
    fern = Product(name='Paproć', color='green', image_path='images/fern.png', description='Soczysto-zielone liściaste gałązki dodające tekstury i naturalnego charakteru kompozycjom.', quantity=160)
    chrysanthemum = Product(name='Chryzantema', color='yellow', image_path='images/chrysanthemum.png', description='Wyrazisty, różnorodny kwiat symbolizujący radość i długowieczność.', quantity=95)
    magnolia = Product(name='Magnolia', color='white', image_path='images/magnolia.png', description='Delikatne, kremowe płatki symbolizujące szlachetność i piękno.', quantity=20)
    iris = Product(name='Irys', color='blue', image_path='images/iris.png', description='Smukły kwiat w odcieniach błękitu, symbol wiary i nadziei.', quantity=130)
    gerbera = Product(name='Gerbera', color='red', image_path='images/gerbera.png', description='Intensywnie barwiony kwiat kojarzony z radością i energią.', quantity=170)
    freesia = Product(name='Frezja', color='pink', image_path='images/freesia.png', description='Subtelny, pachnący kwiat oznaczający delikatność i przyjaźń.', quantity=10)
    calla = Product(name='Kalia', color='yellow', image_path='images/calla.png', description='Elegancki, kielichowaty kwiat symbolizujący czystość i wyrafinowanie.', quantity=85)

    sql_db.session.add_all([
        rose,
        lily,
        tulip,
        eucalyptus,
        daisy,
        sunflower,
        orchid,
        carnation,
        hydrangea,
        peony,
        lavender,
        fern,
        chrysanthemum,
        magnolia,
        iris,
        gerbera,
        freesia,
        calla,
    ])
    sql_db.session.commit()
    print('Initialized the database with sample data.')

if __name__ == '__main__':
    flowerShopFlaskApp.run(debug=True,)