![Making Better Decision Buying a House](https://media.licdn.com/mpr/mpr/jc/AAEAAQAAAAAAAAaSAAAAJGZhNWI4N2U0LWNkOGItNDJjOS1hMGJiLWQyODc2ZGQxYThkNw.jpg)
#Making Better Decision Buying a House

Buying a house is an important decision and sometimes a though one when money is scarce.

This time I created a [Python Script](https://github.com/jansenicus/python-scripts/blob/master/HOUSE/getHouseforSale.py) to collect data of house in "House for Sale" website.

You can use it to gather house data within a certain price range.
You want to know what building area or land area is provided within that price range.

##Example Case
You have opted to gather data of house with price ranging from 600 to 700 million rupiahs.
You want to know which house is the best to buy.


![Command Line Screenshot of getHouseforSale.py](https://github.com/jansenicus/python-scripts/blob/master/HOUSE/houseforsale.png)


Once your data of interest has been put to a csv file, you can do anything with it:

* You can analyze it using a spreadsheet;
* or write an R program to recommend you which house is the best to buy;
* make a visualization to see the fluctuation of price vs land or building area;

You can make an additional column that contains averaged data:

* the average price within that range in million or billion rupiahs;
* the average land area in square meters;
* the average building area in square meters.

The best house option to select is where the lower price meets the upper specification:

* the price is less than the average price;
* the building is greater than the average building area;
* the land area is greater than the average land area.

If you are blessed, you will find one or a few houses that matches that criteria.

But if you can not find house that matches that criteria, still you can choose:

* the largest building area in square meters or;
* the largest land area in square meters

that is available within the price or a price range you have selected.

Of course you are still human and have certain subjective preference to make the decision of buying a house, 
but looking at the data may help you to make better decision.

[More...](https://github.com/jansenicus/python-scripts/blob/master/HOUSE/depok.md)
