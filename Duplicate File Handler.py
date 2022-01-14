import os
import sys
import hashlib

args = sys.argv
if len(args) != 2:
    print("Directory is not specified")

file_format = input("Enter file format:\n ")
direct_sort = input("Size sorting options:\n1. Descending\n2. Ascending\n")
while (direct_sort != "1") and (direct_sort != "2"):
    direct_sort = input("Wrong option\n\nEnter a sorting option:\n")


def dict_size_path(j):
    if j == "":
        count = -1
        dict_size_file_ = {}
        for root, dirs, files in os.walk(args[1]):
            for name in files:
                path_file = os.path.join(root, name)
                size_file = os.stat(path_file).st_size
                count += 1
                size_file_mod = str(size_file) + "-" + str(count)
                dict_size_file_[size_file_mod] = path_file
        return dict_size_file_
    else:
        count = -1
        dict_size_file_ = {}
        for root, dirs, files in os.walk(args[1]):
            for name in files:
                v = name.partition(".")
                if v[2] == j:
                    path_file = os.path.join(root, name)
                    size_file = os.stat(path_file).st_size
                    count += 1
                    size_file_mod = str(size_file) + "-" + str(count)
                    dict_size_file_[size_file_mod] = path_file
        return dict_size_file_


dict_size_file = dict_size_path(file_format)


def demode(elem_key):
    _ = str(elem_key)
    o = _.partition("-")
    return [int(o[0]), int(o[2])]


def create_list(dic_to_lis, option=1):
    key_lis = []
    val_lis = []
    for i, o in dic_to_lis.items():
        key_lis.append(i)
        val_lis.append(o)
    sort_key = list(map(demode, key_lis))
    sort_key.sort()
    if option == 1:
        return sort_key
    else:
        return val_lis


def mark_list(dict_siz_path):
    marked_list = []
    a = create_list(dict_siz_path)
    for k in range(len(a)):
        if k == len(a):
            marked_list.append("*")
        marked_list.append(a[k])
        if k == len(a) - 1:
            break
        z = k + 1
        if a[k][0] != a[z][0]:
            marked_list.append("*")
    marked_list.append("*")
    return marked_list


def marker_to_list(dict_sze_path):
    marked_list_ = mark_list(dict_sze_path)
    list_in_list = []
    list_inner = []
    for i in range(len(marked_list_)):
        if marked_list_[i] == "*":
            list_in_list.append(list_inner)
            list_inner = []
        else:
            list_inner.append(marked_list_[i])
    return list_in_list


def all_size_path(dict_size_path_, t):
    v = marker_to_list(dict_size_path_)
    n = create_list(dict_size_path_, 2)
    if t == "2":
        z = v
    else:
        z = reversed(v)
    for i in z:
        f = []
        for y in range(len(i)):
            x = i[y][0]
            s = i[y][1]
            f.append(s)
        print(x, "bytes")
        for d in f:
            print(n[d])


all_size_path(dict_size_file, direct_sort)

check_duplic = input("Check for duplicates?\n")
while (check_duplic != "yes") and (check_duplic != "no"):
    check_duplic = input("Wrong option\n\nCheck for duplicates?\n")
if check_duplic == "no":
    exit()


def dict_hash(dict_size_file_, check_duplic_):
    if check_duplic_ == "yes":
        dict_hash_file = {}
        for i, k in dict_size_file_.items():
            with open(dict_size_file_[i], "rb") as f:
                g = f.read()
                h = hashlib.md5(g)
                value_tuple = (dict_size_file_[i], h.hexdigest())
                dict_hash_file[i] = value_tuple
        return dict_hash_file


def dict_duplic_sort(dict_size_file_, check_duplic_):
    dict_hash_file_ = dict_hash(dict_size_file_, check_duplic_)
    sorted_tuple = sorted(dict_hash_file_.items(), key=lambda x: x[1][1])
    return sorted_tuple


def duplic_file_tuple(dict_size_file_, check_duplic_):
    sorted_tuple_ = dict_duplic_sort(dict_size_file_, check_duplic_)
    h = []
    tuple_same_hash = []
    for i in range(len(sorted_tuple_)):
        g = i + 1
        if g < len(sorted_tuple_) and sorted_tuple_[i][1][1] == sorted_tuple_[g][1][1]:
            h.append(i)
            h.append(g)
        else:
            if h:
                tuple_same_hash.append(tuple(set(h)))
                h.clear()
    return tuple_same_hash


def sort_hash_file(dict_size_file_, check_duplic_):
    sorted_tuple_ = dict_duplic_sort(dict_size_file_, check_duplic_)
    tuple_same_hash_ = duplic_file_tuple(dict_size_file_, check_duplic_)
    o_ = []
    for i in tuple_same_hash_:
        index_ = i[0]
        _ = str(sorted_tuple_[index_][0])
        o = _.partition("-")
        r = sorted_tuple_[index_][1][1]
        b = []
        for q in i:
            p = sorted_tuple_[q][1][0]
            b.append(p)
        v = (o[0], r, tuple(b))
        o_.append(v)
    tuple_size_hash = sorted(o_, key=lambda x: x[0])
    return tuple_size_hash


number_file_hash = []


def hash_file_print(dict_size_file_, check_duplic_, direct_sort_):
    tuple_size_hash_ = sort_hash_file(dict_size_file_, check_duplic_)
    o_ = -1
    q = 0
    global number_file_hash
    number_file_hash = ["*"]
    if direct_sort_ == "1":
        tuple_size_hash_.reverse()
    for i in tuple_size_hash_:
        if i[0] != o_:
            o_ = i[0]
            print(i[0], "bytes")
        print("Hash:", i[1])
        for j in i[2]:
            q += 1
            print(f'{q}.', j)
            number_file_hash.append(j)
    number_file_hash.append(q)


hash_file_print(dict_size_file, check_duplic, direct_sort)

list_del_file = []
if check_duplic == "yes":
    del_file = input("Delete files?\n")
    while (del_file != "yes") and (del_file != "no"):
        del_file = input("Wrong option\n\nDelete files?\n")
    number_del_file = ""
    while del_file == "yes":
        number_del_file = input("Enter file numbers to delete:\n")
        list_del_file = number_del_file.split(" ")
        q = 0
        for i in list_del_file:
            if i.isdigit():
                for _ in range(1, number_file_hash[-1] + 1):
                    if i == str(_):
                        q += 1
            else:
                break
        if q == len(list_del_file):
            break
        else:
            print("Wrong format")
            continue


def remove_file(dict_size_file_, list_del_file_):
    h = {}
    for k, w in dict_size_file_.items():
        u = demode(k)
        h[w] = u[0]
    s = 0
    for i in list_del_file_:
        os.remove(number_file_hash[int(i)])
        p = number_file_hash[int(i)]
        s += h[p]
    print(f'Total freed up space: {s} bytes')


remove_file(dict_size_file, list_del_file)
