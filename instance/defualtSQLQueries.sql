SELECT * FROM user;
SELECT * FROM post;
SELECT * FROM image;

INSERT INTO user(name, email, password, date_joined)
VALUES 
("Bob", "bob@example.com", "password123", strftime('%Y-%m-%d', 'now')),
("Charlie", "charlieb@example.com", "password123", strftime('%Y-%m-%d', 'now')),
("Alice", "alice@example.com", "password123", strftime('%Y-%m-%d', 'now'));


INSERT INTO user_detail(address, bio, date_of_birth, user_id)
VALUES
("example str, 123", "Passionate dessert enthusiast with a sweet tooth and a penchant for indulgence", strftime('%Y-%m-%d', '2001-05.20'),1),

("example str, 123", "Lunch aficionado with a penchant for exploring culinary delights midday. Always on the hunt for the perfect lunch spot, 
blending taste and ambiance for the ultimate dining experience.", strftime('%Y-%m-%d', '2001-05.20'),2),

("example str, 123", "Breakfast enthusiast with a passion for starting the day with culinary creativity 
and comfort food classics. Always seeking the perfect balance of flavor and nourishment to kickstart 
mornings with joy", strftime('%Y-%m-%d', '2001-05.20'), 3);


INSERT INTO post(title, body, user_id, category, date_created)
VALUES
("Almond Cupcake with Raspberry Cheesecake Frosting", "It tastes like springtime,” said Alana, our fabulous photographer, after her first bite of this creation. This cupcake was vying for top billing as 
well, and, depending on my mood, could steal the crown. This cupcake was more delicate and dainty, where the cookie dough cupcake was bulkier, and more binge-eating worthy. The almond-flavored cake was 
delicious, and felt dense but not heavy. There was still a fluffiness to the cake, but there was enough body to make the small cupcake satisfying.This balance in baking is incredibly difficult — things 
tend to either be too fluffy and spongy, and feel like they will fall under the weight of heavy frosting, or they are so dense they feel solid and lose their spring. This was the perfect consistency. 
Occasionally crunching on raspberry seeds in the frosting was a pleasant reminder that it was the real deal. It was not overpoweringly fruity either, leaving a lot of the sugary, creamy cheesecake 
flavor to shine through, with the raspberry being the subtle top note. Together, this pairing was absolutely perfect. This would be a great cupcake for a high tea, a fancy dress birthday party with s
parkling wines, or a super classy wedding that had a jazz band or orchestra for music instead of a DJ. That’s the feel of this cupcake. Sure, you can eat it on the couch in your sweatpants, but I feel 
like this cupcake deserves better.", 1, "Dessert", strftime('%Y-%m-%d', 'now')),

("Blueberry Lemon Cupcakes", "If you’ve read my reviews before, you will know that I am not a huge fan of lemon-flavored desserts. While I can appreciate them, they’re not my thing. That said, I do 
try and be objective in my reviews. Even with my proclivities about lemon, this was a delicious cupcake. The lemon was not overpowering, much like the raspberry in the almond raspberry cheesecake was 
not overpowering. You knew lemon was there, but it wasn’t stealing the show. The cake allowed the blueberries to shine through, which were on top of the lemon frosting. Again, the frosting was not overly 
lemon, but a light lemon flavor. Blueberries are such a subtle flavor, the least tart of the berries, with a quiet sweetness that can easily be overpowered by something tart like lemon. Mundy’s creation 
lets you taste both in equal parts, subtle but flavorful, and not cloying. She did a wonderful job with this one.", 1, "Dessert", strftime('%Y-%m-%d', 'now')),

("Red Velvet Cupcake", "Red Velvet is a flavor that is difficult to pull off, but Mundy did it. Much like her other cupcakes, the cake part was moist, not too sweet, and had the right consistency to it. 
The signature cream cheese frosting that topped it really got to sing. Red velvet often ends up too sweet, too red, and off the rails. In short, it ends up being a tryhard cupcake. Not here. 
She lets the simple elegance of this classic stand on its own, and it holds up to the spotlight.", 1, "Dessert", strftime('%Y-%m-%d', 'now')),

("Burgermeister", "There are plenty of great burgers found in Berlin, but none are quite as iconic as Burgermeister’s. This joint first opened in a former public toilet outside 
the Schlesisches Tor U-Bahn station and, as a testament to its success, has now expanded to eight locations across the city. The menu is refreshingly simple, the cheesy fries 
as comforting as comfort food gets, and the mouth-watering vegan burger nothing like your token veggie option.", 2, "Lunch", strftime('%Y-%m-%d', 'now')),

("Annelies", "When it comes to picking a favourite brunch spot in Berlin, this Kreuzberg café is on everyone’s lips – whether they’re a local or an expat. 
Annelies’ specialisation is in creative fare, some seriously excellent brews, a wide selection of natural wines, and attracting a fanatical repeat crowd. 
It’s probably most famous for its buttermilk pancakes with granola, maple berry syrup and cultured cream, but we love the scrambled eggs with smoked yolk 
and fennel kimchi.", 2, "Lunch", strftime('%Y-%m-%d', 'now')),

("Lon Men's Noodle House", "If Berlin had a Chinatown, it would be Charlottenburg’s Kantstrasse. This tiny hole-in-the-wall spot knocks out Taiwanese classics such as 
noodle soups and gua bao (rice buns filled with duck) as well as more esoteric plates of dressed beef tongue or pigs’ ears sliced finely over rice 
noodles. Lon Men’s is almost always full in the evening, but the turnover is fast enough that you’ll find a seat pretty quickly.", 2, "Dinner", strftime('%Y-%m-%d', 'now')),


("Father Carpenter", "Great coffee in a not-s-hidden (anymore) courtyard in Mitte. Come for breakfast and get the smashed avocado with poached egg.", 3, "Breakfast", strftime('%Y-%m-%d', 'now')),

("Silo Coffee", "Great location and atmosphere with plenty of outside or inside seating. Exceptional breakfast and good coffee... I would definitely recommend the 
'silo' breakfast with added mushrooms", 3, "Breakfast", strftime('%Y-%m-%d', 'now')),

("Schwarzes Café", "It is a hidden treasure! Love the place, breakfast at 2pm was delicious. They got many opitons with fresh fruits. Will come back.", 3, "Breakfast", strftime('%Y-%m-%d', 'now'));


DELETE FROM user;

DELETE FROM post;
DELETE FROM image;



-- References:
-- Dessert Posts: https://qweencity.com/food-review-all-of-the-desserts/
-- Lunch/Dinner Posts: https://www.timeout.com/berlin/restaurants/best-restaurants-in-berlin
-- Breakfast Posts: https://foursquare.com/top-places/berlin/best-places-breakfast-food