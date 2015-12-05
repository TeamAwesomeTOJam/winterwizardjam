from pkg_resources import resource_string


def main():
    print resource_string(__name__, 'res/test/test.txt')
