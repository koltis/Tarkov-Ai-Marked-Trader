from random import randint

# if u are a lot of products it would be wise to add some kind of pririty on high profit products on the productlist

productList = [
    {
        'name': 'Glorious E lightweight', 'price': 29295
    },
    {
        'name': 'gingy keychain', 'price': 50400
    },
    {
        'name': 'Axel parrot', 'price': 32130
    },
    {
        'name': 'pipe grip wrench', 'price': 83160
    },
    {
        'name': 'Bottle of OLOLO Multivitamins', 'price': 15805
    },
    {
        'name': 'Flat Screwdriver (long)', 'price': 20790
    },
    {
        'name': 'Pressure gauge', 'price': 38556
    },
    {
        'name': 'roler submariner', 'price': 44760
    },
    {
        'name': 'Can of condensed milk', 'price': 15714
    },
    {
        'name': 'Battered antique book', 'price': 39708
    },
    {
        'name': 'Fuel conditioner', 'price': 38180
    }
]


""""
{
    'name': , 'price': 
},

"""""


def getNextProduct(prevProduct=""):
    nextProduct = productList[randint(0, len(productList) - 1)]
    if prevProduct:
        if nextProduct['name'] == prevProduct:
            return getNextProduct(prevProduct)
        else:
            return nextProduct
    else:
        return nextProduct
