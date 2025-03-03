# OSRS Alch Margin Tool
#### Gets the latest Old School Runescape price data for all items and displays the top items with the largest alch margin.

##### Example output:
```
Item ID  Name                           High Alch  Buy Price  Margin    
----------------------------------------------------------------------
19604    Unstrung light ballista        30000      20000      10000     
12327    Red d'hide body (g)            6738       1          6737      
26225    Ancient ceremonial mask        30000      26250      3750      
3054     Mystic lava staff              27000      23736      3264      
23398    Adamant platebody (h3)         9984       7547       2437      
23413    Climbing boots (g)             45000      43214      1786      
4087     Dragon platelegs               162000     160576     1424      
1149     Dragon med helm                60000      58702      1298      
4585     Dragon plateskirt              162000     160941     1059      
26223    Ancient ceremonial legs        48000      46942      1058 
```

Useful websites:
https://prices.runescape.wiki/osrs/
https://prices.runescape.wiki/osrs/alchemy
https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices
https://runescape.wiki/w/Application_programming_interface#Grand_Exchange_Database_API

Example API call for price trends over 180 days:
https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=22224
https://secure.runescape.com/m=itemdb_oldschool/Extended+super+antifire+mix%281%29/viewitem?obj=22224
