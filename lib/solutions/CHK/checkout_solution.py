

def get_basket(sku_string):
    ''' convert a string of SKU_values to a dict item:count '''

    # all the valid items, this would be some kind of database is valid sku lookup function
    #
    items_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F':0}
    for item in sku_string:
        if item not in items_count.keys():
            return None  # not a valid sku, return
        items_count[item] = items_count[item] + 1
    return items_count


def get_sku_lookup():  # normally would have to query a database or something, will cheat and return a dict
    ''' get a dict of all the {skus:prices}'''
    sku_lookup = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'E': 40, 'F':10}
    return sku_lookup

def get_special_offers():

    # quickly work out the differencs of things.
    #
    # special_offers = {'A':{3: -20}, {'B':{2, -15}}} # for every  {x:{y:z}} for every y of x add z
    # special_offers = {'A':{3: 130}, {'B':{2, 45}}} // for every  {x:{y:z}} for every y of x add z
    special_offers = {'A': {5: 200, 3: 130}, 'B': {2: 45}}
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
                    basket[item] =  basket[item] - \
                        (special_offer_item_count * offer_count)
                    total = total + (special_offer_price * offer_count)
    return basket, total


def buy_x_get_x_free(basket):
    ''' take care of by X of item Y get Z of W free
                    input arguement basket: dict of item:count
                    return modified dict, current basket total
    '''
    total = 0
    special_offers = {'E': [2, ['B', 1]], 'F':[2,['F',1]]}  # for every '2' 'E' get 1 'B'
    for key in special_offers.keys():
        if key in basket:
            # we have a special offer item to process;
            required_for_offer_count = special_offers[key][0]
            basket_count = basket[key]

            while required_for_offer_count <= basket_count :
                #number_of_offers = int(basket_count/ required_for_offer_count)

                # add the value of the purchases special offer items
                total = total + get_sku_lookup()[
                    key] * (required_for_offer_count)

                # save on a modulo.
                basket_count = basket_count - required_for_offer_count
                
                basket[key] = basket_count
                free_item_key = special_offers[key][1][0]
                free_item_count = special_offers[key][1][1]
                # take free_item_count free_item_keys from basket.
                if free_item_key in basket:
                    basket_count = max(
                        0, ( basket[free_item_key]-free_item_count))
                basket[key] = basket_count
    return basket, total


def get_total_for_elements_in_basket(basket):

    # should be able to use an accumulate style algorithm for this.
    total = 0
    prices = get_sku_lookup()
    for sku in basket.keys():
        item_count = basket[sku]
        if sku in prices.keys():
            total = total + (item_count * prices[key])
            basket.pop(sku)
    return total, basket  # basket should be empty


def checkout(skus):  # TO DO : Optimise
    'supermarket checkout caluclator, returns cost of items skus'
    # illegal input return -1
    # caluclate the value of item factoring in special offers.

    # we actually want to keep a count of the different items
    if len(skus) == 0:
        return 0

    basket = get_basket(skus)
    if basket == None:
        # invalid sku in skus
        return -1

    #  more functional approach
    basket, total = buy_x_get_x_free(basket)
    basket, special_offer_total = process_special_offers(basket)
    total = total + special_offer_total

    sku_prices = get_sku_lookup()
    for item in basket.keys():
        total = total + (sku_prices[item] * basket[item])
    return total

    # special_offers = get_special_offers()
    # total = 0
    # for item in set(skus):
    # if item in special_offers.keys() and items_count[item] >= special_offers[item].keys():
    # # calculate the prices for every amount of items that reach the deal.
    # # if we have 7 items, and every 3 have a speial price
    # # 7 / 3  = 2, so its 2* special price, then the remainder * the original price.
    # total = total + \
    # (special_offers[item][1] *
    # int(items_count[item]/special_offers[item][0]))
    # total = total + \
    # ((items_count[item] % special_offers[item][0]) * prices[item])
    # else:
    # total = total + (items_count[item] * prices[item])
    # return total


# tests
if __name__ == "__main__":
	print(checkout("CDFFAECBDEAB"));
    #print(checkout("FFF")) # = 20
    #print(checkout("FFFF")) # = 30
    #print(checkout("FFFFF")) # = 40
    #print(checkout("FFFFFF")) # = 40
    #print(checkout("EEEEBB"))# 160, got: 190
    #print(checkout("BEBEEE"))# 160, got: 190
    # print(checkout("EE"))  # 40
    # print(checkout("EEB")) # expected: 80, got: 40
    # print(checkout("ABCDEABCDE"))  # expected: 280, got: 210
    # print(checkout("ABCDE"))  # 155
    # print(checkout("AAAAA"))  # 200
    # print(checkout("AAAAAA"))  # 260
    # print(checkout("AAAAAAA"))  # 300
    # print( checkout("AAAAA") )
    # print( checkout("") == 0)
    # print( checkout("A") == 50)
    # print( checkout("B") == 30)
    # print( checkout("C") == 20)
    # print( checkout("D") == 15)
    # print( checkout("E") == -1)
    # print( checkout("a") == -1)
    # print( checkout("-") == -1)
    # print( checkout("ABCa") == -1)
    # print( checkout("AxA") == -1)
    # print( checkout("ABCDE") == -1)
    # print( checkout("A") == 50)
    # print( checkout("AA") == 100)
    # print( checkout("AAA") == 130.0)
    # print( checkout("AAAA") == 173.33333333333331)
    # print( checkout("AAAAA") == 216.66666666666669)
    # print( checkout("AAAAAA") == 260.0)
    # print( checkout("AAAAAAA") == 303.33333333333337)
    # print( checkout("AAAAAAAA") == 346.66666666666663)
    # print( checkout("AAAAAAAAA") == 390.0)
    # print( checkout("AAAAAAAAAA") == 433.33333333333337)
    # print( checkout("EE") == -1)
    # print( checkout("EEB") == -1)
    # print( checkout("EEEB") == -1)
    # print( checkout("EEEEBB") == -1)
    # print( checkout("BEBEEE") == -1)
    # print( checkout("A") == 50)
    # print( checkout("AA") == 100)
    # print( checkout("AAA") == 130.0)
    # print( checkout("AAAA") == 173.33333333333331)
    # print( checkout("AAAAA") == 216.66666666666669)
    # print( checkout("AAAAAA") == 260.0)
    # print( checkout("B") == 30)
    # print( checkout("BB") == 45.0)
    # print( checkout("BBB") == 67.5)
    # print( checkout("BBBB") == 90.0)
    # print( checkout("ABCDEABCDE") == -1)
    # print( checkout("CCADDEEBBA") == -1)
    # print( checkout("AAAAAEEBAAABB") == -1)
    # print( checkout("ABCDECBAABCABBAAAEEAA") == -1)

