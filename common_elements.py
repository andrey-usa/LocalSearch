def common(list1, list2):
    list_with_dubs = [item for item in list1 if item in list2]
    return list(set(list_with_dubs))

def main():
    # Same tests as the doctests above, but can be run from the terminal:
    # python3 common_elements.py
    print(common(['a'], ['a']))                             # should print ['a']
    print(common(['a', 'b', 'c'], ['x', 'a', 'z', 'c']))    # should print ['a', 'c']
    print(common(['a', 'b', 'c'], ['x', 'y', 'z']))         # should print []
    print(common(['a', 'a', 'b'], ['a', 'a', 'x']))         # should print ['a']

if __name__ == '__main__':
    main()