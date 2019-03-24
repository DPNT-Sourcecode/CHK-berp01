

def get_sku_lookup():  # normally would have to query a database or something, will cheat and return a dict
    ''' get a dict of all the {skus:prices}'''
    sku_lookup = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    return sku_lookup


def get_special_offers():

    # quickly work out the differencs of things.
    #
    # special_offers = {'A':{3: -20}, {'B':{2, -15}}} # for every  {x:{y:z}} for every y of x add z
    # special_offers = {'A':{3: 130}, {'B':{2, 45}}} // for every  {x:{y:z}} for every y of x add z
    special_offers = {'A': [3, 130], 'B': [2, 45]}
    return special_offers

# noinspection PyUnusedLocal
# skus = unicode string


def checkout(skus):  # TO DO : Optimise
    'supermarket checkout caluclator, returns cost of items skus'
    # illegal input return -1
    # caluclate the value of item factoring in special offers.

    # we actually want to keep a count of the different items
    if len(skus) == 0:
        return -1

    prices = get_sku_lookup()
    # easier to read than count array
    items_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    basket = {}

    for item in skus:
        #item = upper(item)
        if item not in items_count.keys():
            return -1
        items_count[item] = items_count[item] + 1

    special_offers = get_special_offers()
    total = 0
    for item in set(skus):
        if item in special_offers.keys() and items_count[item] >= special_offers[item][0]:
            # calculate the prices for every amount of items that reach the deal.
            # if we have 7 items, and every 3 have a speial price
            # 7 / 3  = 2, so its 2* special price, then the remainder * the original price.
            total = total + \
                (special_offers[item][1] *
                 int(items_count[item]/special_offers[item][0]))
            total = total + \
                ((items_count[item] % special_offers[item][0]) * prices[item])
        else:
            total = total + (items_count[item] * prices[item])
    return total

'''
# tests
if __name__ == "__main__":
    print(checkout(['A', 'A', 'A']) == 130)
    print(checkout(['A', 'A', 'A', 'a']) == -1)
    print(checkout(['A', 'A', 'A', 'B', 'B']) == 175)
    print(checkout([]) == -1)
    print(checkout(['A', 'F']) == -1)
'''
