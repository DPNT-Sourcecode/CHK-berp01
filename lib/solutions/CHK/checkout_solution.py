

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

def buy_x_get_x_free(basket):
	''' take care of by X of item Y get Z of W free
		input arguement basket: dict of item:count
		return modified dict, current basket total
	'''
	total = 0;
	special_offers = {'E':[2, ['B', 1]]} # for every '2' 'E' get 1 'B'
	for key special_offers.keys():
		if key in basket:
			# we have a special offer item to process;
			required_count = special_offers[key][0]
			basket_count = basket[key]
			if required_count <= basket_count: # does it reach the requirement
			   # how many
			   number_of_offers = required_count / basket_count;
			   total = get_sku_lookup()[key] * number_of_offers;
				
				basket[key][0] = required_count - (basket_count*required_count) # save on a modulo.
				
				
				free_item_key = special_offers[key][1][0]
				free_item_count = special_offers[key][1][1]
				
				# take free_item_count free_item_keys from basket. 
				if free_item_key in basket:
					basket[free_item_key] = min(basket[free_item_key], basket[free_item_key]-free_item_count)

def checkout(skus):  # TO DO : Optimise
    'supermarket checkout caluclator, returns cost of items skus'
    # illegal input return -1
    # caluclate the value of item factoring in special offers.

    # we actually want to keep a count of the different items
    if len(skus) == 0:
        return 0

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
        if item in special_offers.keys() and items_count[item] >= special_offers[item].keys():
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
    print(checkout("") == -1)
    print(checkout("A") == 50)
    print(checkout("B") == 30)
    print(checkout("C") == 20)
    print(checkout("D") == 15)
    print(checkout("a") == -1)
    print(checkout("-") == -1)
    print(checkout("ABCa") == -1)
    print(checkout("AxA") == -1)
    print(checkout("ABCD") == 115)
    print(checkout("A") == 50)
    print(checkout("AA") == 100)
    print(checkout("AAA") == 130)
    print(checkout("AAAA") == 180)
    print(checkout("AAAAA") == 230)
    print(checkout("AAAAAA") == 260)
    print(checkout("B") == 30)
    print(checkout("BB") == 45)
    print(checkout("BBB") == 75)
    print(checkout("BBBB") == 90)
    print(checkout("ABCDABCD") == 215)
    print(checkout("BABDDCAC") == 215)
    print(checkout("AAABB") == 175)
    print(checkout("ABCDCBAABCABBAAA") == 505)
    #
    print(checkout(""))
    print(checkout("A"))
    print(checkout("B"))
    print(checkout("C"))
    print(checkout("D"))
    print(checkout("a"))
    print(checkout("-"))
    print(checkout("ABCa"))
    print(checkout("AxA"))
    print(checkout("ABCD"))
    print(checkout("A"))
    print(checkout("AA"))
    print(checkout("AAA"))
    print(checkout("AAAA"))
    print(checkout("AAAAA"))
    print(checkout("AAAAAA"))
    print(checkout("B"))
    print(checkout("BB"))
    print(checkout("BBB"))
    print(checkout("BBBB"))
    print(checkout("ABCDABCD"))
    print(checkout("BABDDCAC"))
    print(checkout("AAABB"))
    print(checkout("ABCDCBAABCABBAAA"))
'''

