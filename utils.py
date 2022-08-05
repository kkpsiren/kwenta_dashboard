def trade_side_mapper(tradesize):
    if tradesize <0 :
        return 'short'
    elif tradesize == 0:
        return 'modify_margin'
    else:
        return 'long'