# Projet Technologies Web
## Introduction
Ce projet présente un site web pour un restaurant et propose une présentation du restaurant ainsi que les fonctionalitées pour les clients de passer des commandes et de réserver une table. Pour le staff on a la possibilité d'éditer le menu, c’est-à-dire ajouter, effacer et éditer les plats. De plus le staff peut aussi voir les commandes et les marquer comme prêtes. Les utilisateurs peuvent aussi laisser des commentaires qui seront visibles pour le staff dans la base de données. Quelques pages web sont différentes ou que accessible pour l'administrateur(staff), comme par exemple la page ***'order_management.html'*** pour gérer les commandes et les pages de manipulations des plats.

## Comment lancer le site
Afin de lancer le site web, il faut tout d'abbord lancer le serveur, avec la commande ```python main.py```. Dans la console il y aura l'addresse du site ainsi que le message ***''Le coin de Namur' is on AIR!'*** afin d'indiquer que le serveur est bien lancé.

## Fonctionalités
Comme dit avant quelques pages ne sont que accessible pour le staff, par contre toutes les fonctionalités des clients est aussi disponibles pour le staff:

### Utilisateur (Client)
- Voir les élèments du menu (sans un login)
- Création d'un compte
- Login/ Logout
- Accèder à la page Profile 
    - Changer le prènom, nom et email
    - Changer le mot de passe, en fournissont le mot de passe actuel
- Accèder à la page My Orders, pour voir les commandes de l'utilisateur
- Laisser un commentaire, en indiquant l'email ainsi que le password
- Réserver une table en indiquant le jour, l'heure ainsi que le nombre de personnes
- Passer des commandes
    - Ajouter des éléments au panier
    - Retirere des éléments du panier
    - Faire un checkout
    - Annuler la commande
    - Dans la page My Orders, suivre le status de la commande ("working", "finished")

### Administrateur (Staff)
- Manipuler le menu du restaurant via la page Menu, sur laquelle il y a des buttons uniquement visible pour les administrateurs
 - Additioner des plats au menu 
 - Supprimer des plats du menu 
 - Editer des plats du menu 
- Gérer les tables à travers le button dans la page Profile uniquement visible pour les administrateurs
    - changer la disponibilité des tables -> enlever la reservation actuelle
- Gérer les commandes à travers le button dans la page Profile uniquement visible pour les administrateurs
    - changer le status de la commande -> marquer la commande comme prête

## Fichiers

TECHWEBPROJET/
|
├── app_management/
|   ├── routes/
|   |   ├── feedback_routes.py
|   |   ├── menu_routes.py
|   |   ├── orders_routes.py
|   |   ├── table_booking_routes.py
|   |   └── users_routes.py
|   |
|   ├── schema/
|   |   └── schema.py
|   |
|   ├── services/
|   |   ├── feedback_services.py
|   |   ├── menu_services.py
|   |   ├── orders_services.py
|   |   ├── table_booking_services.py
|   |   └── users_services.py
|   |
|   ├── sql/
|   |   └── sql_models.py
|   |
|   ├── app.py
|   ├── db_manager.py
|   └── user_login.py
|
├── data/
|   └── database.sqlite
|
├── static/
|   ├── background.png
|   ├── script.js
|   └── style.css
|
├── templates/
|   ├── dishes/
|   |   ├── edit_dishes.html
|   |   ├── menu.html
|   |   ├── new_dish.html
|   |   └── remove_dish.html
|   |
|   ├── errors/
|   |   ├── 400.html
|   |   ├── 401.html
|   |   ├── 404.html
|   |   └── 422.html
|   |
|   ├── orders/
|   |   ├── order_page.html
|   |   └── orders_management.html
|   |
|   ├── tables/
|   |   ├── book_table.html
|   |   └── tables.html
|   |
|   ├── users/
|   |   ├── login_page.html
|   |   ├── my_orders.html
|   |   ├── new_user_page.html
|   |   └── profile_page.html 
|   |
|   ├── empty_page.html
|   ├── home_page.html
|   └── my_macro.html
|
├── .gitignore
|
├── main.py
|
├── README.md
|
└── requirements.txt

## Routes
### Routes pour les menus
Prefix: '/menu'
- '/all/dishes'
- '/add/dish'
- '/remove/dish'
- '/edit/dish'

### Routes pour les orders
Prefix: '/orders'
- '/order'
- '/my/orders'
- '/add/basket'
- '/remove/basket'
- '/checkout'
- '/cancel/order'
- '/get/orders'
- '/complete'

### Routes pour les table bookings
Prefix: '/table'
- '/book/table'
- '/manage'
- '/change/availability'

### Routes pour les users
Prefix: '/users'
- '/me'
- '/new/user'
- '/change/password'
- '/change/user/information'
- '/home'
- '/login'
- '/logout'
- '/profile'

### Routes pour le feedback
Prefix: '/feedbacks'
- '/feedback'

## Fonctions

### feedback_services.py
- def leave_feedback(feedback_content, email):
    - Cette fonction est responsable pour ajouter le feedback/ commentaire à la base de donnée
    - La valeur de feedbackid est le nombre de feedback dans la base de donnée +1
    - Le clientemail est l'email du client qui a fait le feedback
    - Le feedback est le contenu du commentaire

### menu_services.py
- def get_menu():
    - Cette fonction retourne tous les plats dans la base de donnée
- def add_dish(new: DishSchema):
    - Cette fonction ajoute un plat à la base de donnée
    - Le dishid est une valeur générer par la fonction generate_id()
    - Le dishname est la valeur donner par le staff
    - Le dishtype est la valeur passer par le staff, la valeur peut doit être : "Starters", "Main Dish", "Drinks" ou "Dessert"
    - Le price est la valeur donner par le staff
- def remove_dish_by_id(id_to_delete):
    - Cette fonction supprime le plat avec l'id passer comme paramètre
- def edit_dish_by_id(id_to_edit, updated_dish):
    - Cette fonction change les valeurs du plat passer comme paramètre par les nouvelles valeurs donner par le staff
    
### order_services.py
- def get_orders():
    - Cette fonction retourne toutes les commandes de la base de donnée
- def add_to_basket(dish_id, user):
    - Cette fonction permet à ajouter des plats au panier(order)
    - Elle regarde tout d'abbord si une commande de l'utilisateur actuel n'a pas été fini encore(checkout) si une commande existe alors on rajoute le plat à cette commande, sinon on crée une nouvelle commande
- def cancel_order(user):
    - Cette fonction supprime la commande actuelle de l'utilisateur actuel
- def checkout(user):
    - Cette fonction mets la valeur de "complete" comme True pour indiquer que cette commande est finie et peut etre préparer par le staff
- def remove_from_basket(dish_id, user):
    - Cette fonction permet d'enlever des elements de la commande actuelle
    - D'abbord elle regarde si une commande est en cours si oui elle enlève l'élément de la commande
- def mark_as_complete(order_id):
    - Cette fonction permet au staff de marquer une commande comme prête(ready)
    - Elle change le status de la commande à "ready"

### table_booking_services.py
- def book_table(people_count, day, time, user):
    - Cette fonction est responsable pour réserver une table
- def get_tables():
    - Cette fonction retoure toutes les tables de la base de donnée
- def change_availability(table_id):
    - Cette fonction permet de changer la disponibilité de la table avec l'id passer comme paramètre
    - Elle remet toutes les valeurs à vide et mets available à True

### users_services.py
- def get_user_by_email(email: str):
    - Cette fonction retourne l'utilisateur avec l'email passer comme paramètre
- def add_new_user(user_values: UserSchema):
    - Cette fonction permet d'ajouter un utilisateur à la base de donnée
    - L'utilisateur sera un client de base et son id est générer avec la fonction generate_id()
- def generate_id():
    - Cette fonction génère un int avec la formule "result = result + random.randint(1,10) * result" et cela 10 fois, pour donner un nombre aleatoire 
- def change_password(curr, new, user_email):
    - Cette fonction permet de changer le password de l'utilisateur avec l'email passer comme paramètre
    - Pour pouvoir changer le password, il faut indiquer le password actuel
- def change_user_information(new_firstname, new_name, new_email, user_email):
    - Cette fonction permet de changer les informations de l'utilisateur avec l'email passer comme paramètre
    - Pour changer les informations on a pas besoin d'indiquer le password