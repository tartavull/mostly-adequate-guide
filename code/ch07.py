def chapter_7():
    Maybe('Malkovich Malkovich').map(findall('al'))
    Maybe(Nothing()).map(findall('al'))

    def add(d):
        d['age']=10
        return d

    Maybe({'name':'boris'}).map(add)
    Maybe(Nothing()).map(add)

    safe_head = lambda xs: Maybe(xs[0]) if len(xs) else Maybe(Nothing())

    # street_name :: Object -> Maybe String
    street_name = compose(map(prop('street')), safe_head, prop('addresses'))
    street_name({ 'addresses': [] })
    street_name({ 'addresses': [{ 'street': 'Shady Ln.', 'number': 4201 }] })

    # withdraw :: Number -> Account -> Maybe(Account)
    withdraw = curry(lambda amount, balance: Maybe(balance - amount) if balance >= amount else Maybe(Nothing()))

    # This function is hypothetical, not implemented here... nor anywhere else.
    # update_ledger :: Account -> Account
    update_ledger = lambda account: account

    # remaining_alance :: Account -> String
    remaining_balance = lambda balance: f'Your balance is {balance}'

    # finish_ransaction :: Account -> String
    finish_transaction = compose(remaining_balance, update_ledger)

    # get_twenty :: Account -> Maybe(String)
    get_twenty = compose(map(finish_transaction), withdraw(20))

    get_twenty(200.00)
    # Maybe(Your balance is $180)

    get_twenty(10.0)
    # Maybe(Nothing)
    #######################
    # maybe :: b -> (a -> b) -> Maybe a -> b
    maybe = curry(lambda v, f, m: v if m.is_nothing() else f(m.value))

    # get_twenty :: Account -> String
    get_twenty = compose(maybe('You\'re broke!', finish_transaction), withdraw(20))

    print(get_twenty(200.00))
    # 'Your balance is $180.00'

    print(get_twenty(10.00))
    # 'You\'re broke!'

# get_age :: String -> Either(String, Number)
from datetime import datetime

def get_age(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return Either(datetime.now().year - date.year)
    except ValueError:
        return Left('Birth date could no be parsed')

get_age('2005-12-12')
get_age('July 4, 2001')

##############################
concat = curry(lambda s1, s2: s1+s2)
add = curry(lambda n1, n2: n1+n2)

# fortune :: Number -> String
fortune = compose(concat('If you survive, you will be '), str, add(1))

# zoltar :: User -> Either(String, _)
zoltar = compose(map(print), map(fortune), get_age)

zoltar('2005-12-12')
# 'If you survive, you will be 16'
# Right(undefined)

zoltar('balloons!')
# Left('Birth date could not be parsed')
##############################
# either :: (a -> c) -> (b -> c) -> Either a b -> c

zoltar = compose(print, either(id, fortune), get_age)

print(zoltar('2005-12-12'))
# 'If you survive, you will be 16'

print(zoltar('balloons!'))
# Left('Birth date could not be parsed')

IO(lambda: 5).map(lambda n: n+1).value()
############################
# url :: IO String
url = IO(lambda: input("Enter url"))

# split :: String -> String -> [String]
split = curry(lambda pattern, s: s.split(pattern))

# to_pairs :: String -> [[String]]
to_pairs = compose(fmap(split('=')), split('&'))

# last :: [a] -> a
last = lambda xs: xs[-1]

# params :: String -> [[String]]
params = compose(to_pairs, last, split('?'))

# find_param :: String -> IO Maybe [String]
input_params = map(compose(Maybe, params), url)

# -- Impure calling code ----------------------------------------------

# run it by calling value()!
input_params.value()
# -> https://example.com/over/there?name=ferret&field2=value2
# Maybe([['name', 'ferret'], ['field2', 'value2']])

tmd = Task(Maybe('Rock over London'))

ctmd = Compose(tmd)

ctmd2 = map(append(', rock on, Chicago'), ctmd)

# Compose(Task(Just('Rock over London, rock on, Chicago')))

ctmd2.get_compose
# Task(Just('Rock over London, rock on, Chicago'))
