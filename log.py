

class FILE_handler:
    # failed_tests = open('failed.txt', 'w')
    # passed_tests = open('passed.txt', 'w')
    
    def __init__(self):
        pass
        # global failed_tests
        # global passed_tests

    def __del__(self):
        pass
        # self.failed_tests.close()
        # self.passed_tests.close() 

    def write_f(self, text):
        print(text)
        with open('failed.txt', 'a')  as f:
            f.write(text)

    def write_p(self, text):
        print(text)
        with open('passed.txt', 'a')  as f:
            f.write(text)
