from adequate import (curry, compose, IO,  map, head, 
        Maybe, Nothing, chain, add)

def c0():
    #read_file :: str -> IO str
    read_file = lambda filename: IO(lambda: open(filename,'r').read())

    def  print_and_pass(x):
        print(x)
        return x

    # io_print ::  str -> IO str
    io_print = lambda x: IO(lambda: print_and_pass(x))

    # cat :: str -> IO (IO str)
    cat = compose(map(io_print), read_file)
    
    print(cat('../.git/config'))

def c1():
    #read_file :: str -> IO str
    read_file = lambda filename: IO(lambda: open(filename,'r').read())

    def  print_and_pass(x):
        print(x)
        return x

    # io_print ::  str -> IO str
    io_print = lambda x: IO(lambda: print_and_pass(x))

    # cat :: str -> IO (IO str)
    cat = compose(map(io_print), read_file)
    
    # cat_first_char :: str -> IO (IO str)
    cat_first_char = compose(map(map(head)), cat)
    print(cat_first_char('.git/config'))
    # IO(IO('['))

    print(cat_first_char('../.git/config').unsafe_perform_IO().unsafe_perform_IO())

def c2():
    # safe_value :: key -> {key: a} -> Maybe a
    safe_value = curry(lambda k, d: Maybe(d.get(k, Nothing)))

    # safe_head :: [a] -> Maybe a
    safe_head = safe_value('0')

    # first_address_street :: User -> Maybe (Maybe (Maybe Street))
    first_address_street = compose(
    	map(map(safe_value('street'))),
	map(safe_head),
	safe_value('addresses'))

    first_address_street({
        'addresses': {'0': { 'street': { 'name': 'Mulburry', 'number': 8402 }, 'postcode': 'WC2N' }}
    })
    # Maybe(Maybe(Maybe({'name': 'Mulburry', 'number': 8402})))

def c3():
    # safe_value :: key -> {key: a} -> Maybe a
    safe_value = curry(lambda k, d: Maybe(d.get(k, Nothing)))

    # safe_head :: [a] -> Maybe a
    safe_head = safe_value('0')

    # join :: Monad m => m (m a) -> m a
    join = lambda mma: mma.join()

    # first_address_street :: User -> Maybe (Maybe (Maybe Street))
    first_address_street = compose(
        join,
        map(safe_value('street')),
        join,
        map(safe_head),
        safe_value('addresses'))

    first_address_street({
        'addresses': {'0': { 'street': { 'name': 'Mulburry', 'number': 8402 }, 'postcode': 'WC2N' }}
    })
    # Maybe({'name': 'Mulburry', 'number': 8402})

def c4():
    # safe_value :: key -> {key: a} -> Maybe a
    safe_value = curry(lambda k, d: Maybe(d.get(k, Nothing)))

    # safe_head :: [a] -> Maybe a
    safe_head = safe_value('0')

    # join :: Monad m => m (m a) -> m a
    join = lambda mma: mma.join()

    # first_address_street :: User -> Maybe (Maybe (Maybe Street))
    first_address_street = compose(
        join,
        map(safe_value('street')),
        join,
        map(safe_head),
        safe_value('addresses'))

    first_address_street({
        'addresses': {'0': { 'street': { 'name': 'Mulburry', 'number': 8402 }, 'postcode': 'WC2N' }}
    })


    # map/join
    first_address_street = compose(
        join,
        map(safe_value('street')),
        join,
        map(safe_head),
        safe_value('addresses'))

    # chain
    first_address_street = compose(
      chain(safe_value('street')),
      chain(safe_head),
      safe_value('addresses'),
    );

    a = first_address_street({
        'addresses': {'0': { 'street': { 'name': 'Mulburry', 'number': 8402 }, 'postcode': 'WC2N' }}
    })
    print(a)

def c5():

    a = Maybe(3).chain(lambda three: Maybe(2).map(add(three)))
    # safe_value :: key -> {key: a} -> Maybe a
    safe_value = curry(lambda k, d: Maybe(d.get(k, Nothing)))

    a = Maybe(Nothing()) \
        .chain(safe_value('address')) \
        .chain(safe_value('street'))
    print(a)


if __name__ == '__main__':
    c5()

