def ifelse(*args):
    arg0 = globals().get(args[0])
    arg1 = globals().get(args[1]) or args[1]
    return arg0 or arg1

result = str(ifelse(*args))
