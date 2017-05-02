from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, UserAccount, Category, ListItem, List

from random import randint

engine = create_engine('sqlite:///top10.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Populate database with starter data
user1 = UserAccount(name="admin")
session.add(user1)

category1 = Category(name="Video Games",
                     url="videogames",
                     public=True,
                     user_account_id="1")
session.add(category1)

category2 = Category(name="Movies",
                     url="movies",
                     public=True,
                     user_account_id="1")
session.add(category2)

category3 = Category(name="Albums",
                     url="albums",
                     public=True,
                     user_account_id="1")
session.add(category3)

category4 = Category(name="Foods",
                     url="foods",
                     public=True,
                     user_account_id="1")
session.add(category4)

session.commit()



# Data below this point is just filler data


# Create users
user2 = UserAccount(name="Carrington")
session.add(user2)

user3 = UserAccount(name="Reagan")
session.add(user3)

user4 = UserAccount(name="Geordy")
session.add(user4)

user5 = UserAccount(name="Bob")
session.add(user5)

user6 = UserAccount(name="Paul")
session.add(user6)

user7 = UserAccount(name="John")
session.add(user7)

user8 = UserAccount(name="Sam")
session.add(user8)

user9 = UserAccount(name="Adam")
session.add(user9)

user10 = UserAccount(name="Jake")
session.add(user10)

session.commit()


def createLists(titleList, category_id, list_id):
    for i in range(2, 11):
        # create list
        session.add(List(user_account_id=i,
                         category_id=category_id,
                         id=list_id))
        visited = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        for j in range(1, 11):
            # create list items
            t = getTitle(titleList, visited)
            d = descriptions[randint(0, 8)]
            session.add(ListItem(list_id=list_id,
                                 position=j,
                                 title=t,
                                 description=d,
                                 img_url="http://placehold.it/50x75"))
        list_id = list_id + 1
        session.commit()

    return list_id


def getTitle(titleList, visited):
    x = randint(0, 18)
    while (visited[x] == True):
        x = randint(0, 18)
    visited[x] = True
    return titleList[x]


videogames = ["Super Mario Sunshine", "Super Mario Galaxy", "The Last Of Us", "Uncharted 4: A Thief's End", "Uncharted 2: Among Thieves", "Horizon: Zero Dawn", "Mass Effect 2", "Portal 2", "Ni No Kuni", "Need for Speed: Most Wanted", "Infamous", "Ratchet And Clank", "FIFA 06", "Super Mario World", "Super Mario Bros. 3", "Rocket League", "Batman: Arkham Knight", "Assassin's Creed IV: Black Flag", "Watch Dogs"]
movies = ["Matrix", "Django Unchained", "Ex Machina", "Split", "Get Out", "Arrival", "Creed", "Citizen Kane", "Seven Samurai", "The Great Dictator", "Back to the Future", "The Karate Kid", "Remember The Titans", "Toy Story", "The Lord of the Rings", "Hugo", "The Dark Knight", "Inception", "Rick and Morty: The Movie"]
albums = ["Thriller", "Starboy", "DAMN.", "To Pimp A Butterfly", "A Seat at the Table", "OK Computer", "In Rainbows", "Coloring Book", "808s & Heartbreak", "Blank Face", "channel ORANGE", "The College Dropout", "Currents", "Ego Death", "The Life of Pablo", "A Moon Shaped Pool", "Take Care", "Random Access Memories", "Watch The Throne"]
foods = ["Banana", "Orange", "Apple", "Tacos", "Burgers", "Ice Cream", "Pizza", "Pasta", "Salad", "Chicken Nuggets", "Bacon", "Pancakes", "Noodles", "Rice", "Fries", "Cookies", "Chips", "Potato Salad", "Carrots"]
descriptions = ["Morbi non porttitor leo. Aliquam nulla odio, sagittis et sodales non, tristique a elit. In sit amet fermentum eros, ac malesuada est. Nulla lobortis purus eu ante congue, in facilisis.",
                "Morbi bibendum luctus augue eu aliquet. Vestibulum euismod blandit congue. Nunc justo quam, fermentum eget gravida eget, sollicitudin a erat. Nam egestas faucibus porta. Mauris vestibulum enim sapien. Proin elit libero, pharetra in euismod vel.",
                "Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce convallis cursus laoreet. Nunc sapien metus, luctus eu rutrum nec, tempus feugiat metus. Curabitur convallis laoreet ante vitae lobortis. Sed sapien arcu, faucibus a nisl sit amet, vestibulum laoreet.",
                "Aliquam ac aliquet libero. Maecenas hendrerit arcu id orci vulputate scelerisque. Cras magna orci, bibendum vitae tortor ac, fermentum sagittis nibh. Phasellus convallis eget nisi ut pharetra. Integer semper ligula tortor, non ultricies enim blandit eget. Nulla ac ipsum sem.",
                "Etiam vel nibh tincidunt, volutpat nunc quis, sagittis massa. Vestibulum pellentesque pretium nisi eget dapibus. Sed non massa ut elit lacinia convallis vitae sed eros. Curabitur vitae neque elementum, vehicula ipsum vitae, posuere felis. Praesent.",
                "Proin enim eros, cursus vel neque a, iaculis bibendum nisi. Ut eget varius tellus. Proin tincidunt luctus congue. Phasellus condimentum sed nisi eget condimentum. Fusce a aliquam erat, nec dignissim.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque laoreet consequat ipsum quis mollis. Fusce at lorem pretium, feugiat tellus quis, malesuada risus. Etiam massa dolor, consequat placerat mauris eu.",
                "Vivamus vehicula molestie vulputate. Etiam fringilla id ante id facilisis. Morbi nulla tortor, ullamcorper eget sollicitudin at, congue nec velit. In suscipit leo porttitor, volutpat orci et, pretium arcu. Phasellus iaculis vulputate dignissim. Donec bibendum.",
                "Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris diam diam, faucibus non elementum vitae, congue nec leo. In risus justo, iaculis vel ex quis, porta vulputate nisl. Nullam non sollicitudin magna. Cras ultrices faucibus."]


# Create lists
list_id = 1
list_id = createLists(videogames, 1, list_id)
list_id = createLists(movies, 2, list_id)
list_id = createLists(albums, 3, list_id)
list_id = createLists(foods, 4, list_id)


print "populated the database!"
