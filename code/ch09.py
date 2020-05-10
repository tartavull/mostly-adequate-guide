from adequate import Container, map, add

def c1():
    # We can't do this because the numbers are bottled up.
    add(Container(2), Container(3))
    # TypeError: unsupported operand type(s) for +: 'Maybe' and 'Maybe'

    # Let's use our trusty map
    container_of_add = map(add, Container(2))

def c2():
  return Container(2).chain(lambda two: Container(3).map(add(two)))

def c3():
    Container(add(2)).ap(Container(3))
    # Container(5)

    # all together now
    Container(2).map(add).ap(Container(3))
    # Container(5)


if __name__ == "__main__":
    print(c3())
