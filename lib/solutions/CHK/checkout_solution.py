def get_basket(sku_string):
    ''' convert a string of SKU_values to a dict item:count '''

    # all the valid items, this would be some kind of database is valid sku lookup function
    #
    items_count =
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0,
        'E': 0,
        'F': 0,
        'G': 0,
        'H': 0,
        'I': 0,
        'J': 0,
        'K': 0,
        'L': 0,
        'M': 0,
        'N': 0,
        'O': 0,
        'P': 0,
        'Q': 0,
        'R': 0,
        'S': 0,
        'T': 0,
        'U': 0,
        'V': 0,
        'W': 0,
        'X': 0,
        'Y': 0,
        'Z': 0}
    for item in sku_string:
        if item not in items_count.keys():
            return None  # not a valid sku, return
        items_count[item] = items_count[item] + 1
    return items_count


def get_sku_lookup():  # normally would have to query a database or something, will cheat and return a dict
    ''' get a dict of all the {skus:prices}'''
    sku_lookup = {
        'A': 50,
        'B': 30,
        'C': 20,
        'D': 15,
        'E': 40,
        'F': 10,
        'G': 20,
        'H': 10,
        'I': 35,
        'J': 60,
        'K': 80,
        'L': 90,
        'M': 15,
        'N': 40,
        'O': 10,
        'P': 50,
        'Q': 30,
        'R': 50,
        'S': 30,
        'T': 20,
        'U': 40,
        'V': 50,
        'W': 20,
        'X': 90,
        'Y': 10,
        'Z': 50}
    return sku_lookup


def get_special_offers():

    # quickly work out the differencs of things.
    #
    # special_offers = {'A':{3: -20}, {'B':{2, -15}}} # for every  {x:{y:z}} for every y of x add z
    # special_offers = {'A':{3: 130}, {'B':{2, 45}}} // for every  {x:{y:z}} for every y of x add z
    special_offers = {
        'A': {5:200, 3:130},
        'B': {2:45}},
        'H': {10:80, 5:45},
        'K': {2:150},
        'P': {5:200},
        'Q': {3:80}
        'V': {3:130, 2:90}
        
    return special_offers


def process_special_offers(basket):
    ''' process the special offers based on prices, should be performed after buy_x_get_x_free'''
    total = 0
    special_offers = get_special_offers()
    for item in basket.keys():
        if item in special_offers:
            item_count = basket[item]
            for special_offer_item_count in special_offers[item]:
                special_offer_price = special_offers[item][special_offer_item_count]
                if item_count >= special_offer_item_count:
                    # we have enough for as special offer
                    offer_count = int(
                        basket[item] / special_offer_item_count)
                    basket[item]=basket[item] -
                        (special_offer_item_count * offer_count)
                    total=total + (special_offer_price * offer_count)
    return basket, total


def buy_x_get_x_free(basket):
    ''' take care of by X of item Y get Z of W free
                    input arguement basket: dict of item:count
                    return modified dict, current basket total
    '''
    total=0
    # for every '2' 'E' get 1 'B'
    special_offers={
        'E': [2, ['B', 1]],
        'F': [2, ['F', 1]],
        'N': [3, ['M', 1]],
        'R': [3, ['Q', 1]],
        'U': [3, ['U', 1]]
        }

    for key in special_offers.keys():
        if key in basket:
            # we have a special offer item to process
            required_for_offer_count=special_offers[key][0]
            # basket_count = basket[key]
            while required_for_offer_count <= basket[key]:
                # number_of_offers = int(basket_count/ required_for_offer_count)
                # add the value of the purchases special offer items
                total=total + (get_sku_lookup()
                               [key] * (required_for_offer_count))

                free_item_key=special_offers[key][1][0]
                free_item_count=special_offers[key][1][1]

                # decrement basket based on offer
                basket[key]=basket[key] - required_for_offer_count

                # take free_item_count free_item_keys from basket.
                if free_item_key in basket:
                    basket[free_item_key]=max(
                        0, (basket[free_item_key]-free_item_count))

    return basket, total


def get_total_for_elements_in_basket(basket):

    # should be able to use an accumulate style algorithm for this.
    total=0
    prices=get_sku_lookup()
    for sku in basket.keys():
        item_count=basket[sku]
        if sku in prices.keys():
            total=total + (item_count * prices[key])
            basket.pop(sku)
    return total, basket  # basket should be empty


def checkout(skus):  # TO DO : Optimise
    'supermarket checkout caluclator, returns cost of items skus'
    # illegal input return -1
    # caluclate the value of item factoring in special offers.
    # we actually want to keep a count of the different items
    if len(skus) == 0:
        return 0

    basket=get_basket(skus)
    if basket == None:
        # invalid sku in skus
        return -1

    #  more functional approach
    basket, total=buy_x_get_x_free(basket)
    # print(basket, total)
    basket, special_offer_total=process_special_offers(basket)
    total=total + special_offer_total
    sku_prices=get_sku_lookup()
    for item in basket.keys():
        total=total + (sku_prices[item] * basket[item])
    return total

print(checkout("NNNM"))#
# print(checkout("FFFF")) # 30 # FFFF 0 F 20 '' 30
# print(checkout("FFFFFF")) # 40
# print(checkout("FFFFFF")) # 40


