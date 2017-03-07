# /usr/bin/env python
# -*- coding: utf-8 -* 

MAP_1 = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5:'F', 6: 'G', 7:"H", 8:"K"}
MAP_2 = {0: 'J', 1: 'D', 2: 'F', 3: 'N', 4: 'V', 5: 'R', 6: 'Z', 7: 'H', 8: 'P', 9: 'M', 10: '8', 11: 'K', 12: 'C', 13: 'X', 14: 'W', 15: 'Y', 16: '3', 17: 'E', 18: 'T', 19: '7', 20: 'B', 21: '2', 22: '6', 23: 'S', 24: 'A', 25: 'Q', 26: '5', 27: 'G', 28: '4', 29: '9', 30: 'U'}
MAP_3 = {0: 'S', 1: 'P', 2: '8', 3: 'J', 4: 'H', 5: '6', 6: 'N', 7: 'B', 8: 'C', 9: 'M', 10: 'G', 11: '3', 12: 'U', 13: 'Y', 14: 'W', 15: 'X', 16: 'T', 17: 'Z', 18: 'V', 19: 'F', 20: '5', 21: 'D', 22: '4', 23: 'R', 24: 'E', 25: '7', 26: 'A', 27: 'Q', 28: '9', 29: '2', 30: 'K'}
MAP_4 = {0: 'K', 1: '5', 2: '7', 3: 'A', 4: 'S', 5: 'R', 6: 'P', 7: '3', 8: 'Z', 9: 'V', 10: 'N', 11: 'E', 12: 'H', 13: '4', 14: 'J', 15: 'D', 16: 'T', 17: '9', 18: '2', 19: 'G', 20: 'C', 21: '8', 22: 'X', 23: 'Q', 24: 'B', 25: '6', 26: 'W', 27: 'F', 28: 'Y', 29: 'M', 30: 'U'}
MAP_5 = {0: 'P', 1: 'C', 2: 'Y', 3: 'F', 4: '8', 5: 'W', 6: '5', 7: 'R', 8: '6', 9: 'T', 10: 'Q', 11: 'E', 12: '7', 13: 'B', 14: 'S', 15: 'J', 16: 'M', 17: '9', 18: 'D', 19: 'N', 20: 'H', 21: 'K', 22: '3', 23: '4', 24: 'V', 25: 'G', 26: 'A', 27: 'U', 28: 'X', 29: 'Z', 30: '2'}
MAP_6 = {0: 'G', 1: '6', 2: 'W', 3: '8', 4: 'A', 5: 'Y', 6: 'Q', 7: '7', 8: 'K', 9: 'C', 10: 'F', 11: 'T', 12: 'P', 13: 'D', 14: 'R', 15: '4', 16: 'M', 17: 'V', 18: '3', 19: 'E', 20: 'B', 21: 'U', 22: '2', 23: 'Z', 24: 'X', 25: '5', 26: 'S', 27: 'J', 28: '9', 29: 'N', 30: 'H'}
MAP_7 = {0: 'U', 1: 'M', 2: 'C', 3: 'R', 4: '2', 5: 'P', 6: 'Z', 7: '8', 8: 'W', 9: 'T', 10: '4', 11: 'V', 12: 'J', 13: 'S', 14: '3', 15: '9', 16: 'H', 17: 'N', 18: 'Y', 19: 'F', 20: 'G', 21: '7', 22: 'X', 23: 'Q', 24: 'A', 25: '5', 26: '6', 27: 'B', 28: 'D', 29: 'K', 30: 'E'}
MAP_8 = {0: '8', 1: '7', 2: 'W', 3: 'H', 4: '6', 5: 'X', 6: 'R', 7: 'K', 8: 'C', 9: 'A', 10: '5', 11: 'S', 12: 'U', 13: 'E', 14: '3', 15: 'J', 16: 'Z', 17: 'T', 18: '9', 19: 'F', 20: 'D', 21: 'G', 22: 'B', 23: '2', 24: 'N', 25: 'M', 26: 'P', 27: 'Y', 28: 'V', 29: '4', 30: 'Q'}
MAP_9 = {0: 'K', 1: '5', 2: '7', 3: 'A', 4: 'S', 5: 'R', 6: 'P', 7: '3', 8: 'Z', 9: 'V', 10: 'N', 11: 'E', 12: 'H', 13: '4', 14: 'J', 15: 'D', 16: 'T', 17: '9', 18: '2', 19: 'G', 20: 'C', 21: '8', 22: 'X', 23: 'Q', 24: 'B', 25: '6', 26: 'W', 27: 'F', 28: 'Y', 29: 'M', 30: 'U'}
MAP_10 = {0: 'P', 1: 'C', 2: 'Y', 3: 'F', 4: '8', 5: 'W', 6: '5', 7: 'R', 8: '6', 9: 'T', 10: 'Q', 11: 'E', 12: '7', 13: 'B', 14: 'S', 15: 'J', 16: 'M', 17: '9', 18: 'D', 19: 'N', 20: 'H', 21: 'K', 22: '3', 23: '4', 24: 'V', 25: 'G', 26: 'A', 27: 'U', 28: 'X', 29: 'Z', 30: '2'}

MAP_R_1 = dict([(v,k) for k,v in MAP_1.items()])
MAP_R_2 = dict([(v,k) for k,v in MAP_2.items()])
MAP_R_3 = dict([(v,k) for k,v in MAP_3.items()])
MAP_R_4 = dict([(v,k) for k,v in MAP_4.items()])
MAP_R_5 = dict([(v,k) for k,v in MAP_5.items()])
MAP_R_6 = dict([(v,k) for k,v in MAP_6.items()])
MAP_R_7 = dict([(v,k) for k,v in MAP_7.items()])
MAP_R_8 = dict([(v,k) for k,v in MAP_8.items()])
MAP_R_9 = dict([(v,k) for k,v in MAP_9.items()])
MAP_R_10 = dict([(v,k) for k,v in MAP_10.items()])

random_list = [
    {
        'f': [MAP_2, MAP_3, MAP_4, MAP_5, MAP_6, MAP_7, MAP_8, MAP_9, MAP_10],
        't': [MAP_R_2, MAP_R_3, MAP_R_4, MAP_R_5, MAP_R_6, MAP_R_7, MAP_R_8, MAP_R_9, MAP_R_10],
    },
    {
        'f': [MAP_3, MAP_4, MAP_5, MAP_6, MAP_7, MAP_8, MAP_9, MAP_10, MAP_2],
        't': [MAP_R_3, MAP_R_4, MAP_R_5, MAP_R_6, MAP_R_7, MAP_R_8, MAP_R_9, MAP_R_10, MAP_R_2],
    },
    {
        'f': [MAP_4, MAP_5, MAP_6, MAP_7, MAP_8, MAP_9, MAP_10, MAP_2, MAP_3],
        't': [MAP_R_4, MAP_R_5, MAP_R_6, MAP_R_7, MAP_R_8, MAP_R_9, MAP_R_10, MAP_R_2, MAP_R_3],
    },
    {
        'f': [MAP_5, MAP_6, MAP_7, MAP_8, MAP_9, MAP_10, MAP_2, MAP_3, MAP_4],
        't': [MAP_R_5, MAP_R_6, MAP_R_7, MAP_R_8, MAP_R_9, MAP_R_10, MAP_R_2, MAP_R_3, MAP_R_4],
    },
    {
        'f': [MAP_6, MAP_7, MAP_8, MAP_9, MAP_10, MAP_2, MAP_3, MAP_4, MAP_5],
        't': [MAP_R_6, MAP_R_7, MAP_R_8, MAP_R_9, MAP_R_10, MAP_R_2, MAP_R_3, MAP_R_4, MAP_R_5],
    },
    {
        'f': [MAP_7, MAP_8, MAP_9, MAP_10, MAP_2, MAP_3, MAP_4, MAP_5, MAP_6],
        't': [MAP_R_7, MAP_R_8, MAP_R_9, MAP_R_10, MAP_R_2, MAP_R_3, MAP_R_4, MAP_R_5, MAP_R_6],
    },
    {
        'f': [MAP_8, MAP_9, MAP_10, MAP_2, MAP_3, MAP_4, MAP_5, MAP_6, MAP_7],
        't': [MAP_R_8, MAP_R_9, MAP_R_10, MAP_R_2, MAP_R_3, MAP_R_4, MAP_R_5, MAP_R_6, MAP_R_7],
    },
    {
        'f': [MAP_9, MAP_10, MAP_2, MAP_3, MAP_4, MAP_5, MAP_6, MAP_7, MAP_8],
        't': [MAP_R_9, MAP_R_10, MAP_R_2, MAP_R_3, MAP_R_4, MAP_R_5, MAP_R_6, MAP_R_7, MAP_R_8],
    },
    {
        'f': [MAP_10, MAP_2, MAP_3, MAP_4, MAP_5, MAP_6, MAP_7, MAP_8, MAP_9],
        't': [MAP_R_10, MAP_R_2, MAP_R_3, MAP_R_4, MAP_R_5, MAP_R_6, MAP_R_7, MAP_R_8, MAP_R_9],
    },
]

def compress(raw_data):
    if isinstance(raw_data, basestring) and raw_data.isdigit():
        raw_data = int(raw_data)
    elif isinstance(raw_data, int) or isinstance(raw_data, long):
        raw_data = int(raw_data)
    else:
        raise 'data error'

    data = ''
    start_index = raw_data % 9
    data_list = []
    while raw_data >= 1:
        data_list.insert(0, raw_data % 31)
        raw_data /= 31

    if len(data_list) < 9:
        data_list = [0]*(9-len(data_list))+data_list

    data += MAP_1[start_index]
    random_data = random_list[start_index]
    for index, number in enumerate(data_list):
        data += random_data['f'][index][number]

    return data
    #return 'a'*(6-len(data_list)) + ''.join(data_list)

def decompress(data):
    if not isinstance(data, basestring) and len(data) != 10:
        raise 'data error'

    if not data:
        return 0

    data = list(data)
    start_index = data[0]
    data = data[1:10]
 
    random_data = random_list[MAP_R_1[start_index]]
    data_id = 0
    for index, s in enumerate(data):
        data_id += random_data['t'][index][s]*pow(31, (8-index))

    return data_id

if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser()
    parser.add_option("-d", "--decompress",
                      help = "Short data to ID")
    parser.add_option("-c", "--compress",
                      help = "ID to short data")
    parser.add_option("-t", "--test",
                      help = "ID test")
    (options, args) = parser.parse_args()

    if len(args):
        parser.error("Unexpected arguments encountered.")

    if options.decompress:
        print u"Short data:%s" % options.decompress
        print u"ID:%s" % decompress(options.decompress)

    if options.compress:
        print u"ID:%s" % options.compress
        print u"Short data:%s" % compress(options.compress)

    if options.test:
        error_n = 0
        for i in xrange(1, int(options.test)):
            c = compress(i)
            d = decompress(c)
            if i != d:
                error_n += 1
            print "%s -----> %s ----> %s" %(i, c, d)

        print "error number is %s" % error_n
