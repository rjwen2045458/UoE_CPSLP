import re
import babynames_reference


class Babies:

    def __init__(self, filename):
        self.read_names_from_file(filename)

    def read_names_from_file(self, filename):
        self.database = {}
        self.database_boy = {}
        self.database_girl = {}
        try:
            for line in open(filename, 'r'):
                name_gender = re.findall(r'[a-zA-Z]+-?[a-zA-Z]*', line)
                if name_gender[0] not in self.database:
                    self.database[name_gender[0]] = [name_gender[1]]
                else:
                    self.database[name_gender[0]].append(name_gender[1])
                if name_gender[1] == 'BOY':
                    if name_gender[0] not in self.database_boy:
                        self.database_boy[name_gender[0]] = [name_gender[1]]
                    else:
                        self.database_boy[name_gender[0]].append(name_gender[1])
                else:
                    if name_gender[0] not in self.database_girl:
                        self.database_girl[name_gender[0]] = [name_gender[1]]
                    else:
                        self.database_girl[name_gender[0]].append(name_gender[1])
        except FileNotFoundError:
            print("Sorry! The file " + filename + " can't find.")
            exit(0)
        #print(self.database)

    def get_total_births(self, gender=None):
        database_in_use = None
        if gender == 'BOY':
            database_in_use = self.database_boy
        elif gender == 'GIRL':
            database_in_use = self.database_girl
        elif gender is None:
            database_in_use = self.database
        else:
            #raise ArgumentError
            print('Sorry! The gender ', gender, ' is not acceptable')
            exit(0)

        names = database_in_use.keys()
        total_births = 0
        for n in names:
            total_births += len(database_in_use[n])
        return total_births

    # individual character
    def get_names_beginning_with(self, first_char, gender=None):
        database_in_use = None
        if gender == 'BOY':
            database_in_use = self.database_boy
        elif gender == 'GIRL':
            database_in_use = self.database_girl
        elif gender is None:
            database_in_use = self.database
        else:
            print('Sorry! The gender ', gender, ' is not acceptable')
            exit(0)

        result = []
        for fc in first_char:
            names = database_in_use.keys()
            for n in names:
                if n[0].lower() == fc.lower():
                    result.append(n)
        result.sort()
        return result

    def get_top_N(self, N, gender=None):
        database_in_use = None
        if gender == 'BOY':
            database_in_use = self.database_boy
        elif gender == 'GIRL':
            database_in_use = self.database_girl
        elif gender is None:
            database_in_use = self.database
        else:
            print('Sorry! The gender ', gender, ' is not acceptable')
            exit(0)

        name_frequence = {}
        for name in database_in_use.keys():
            name_frequence[name] = len(database_in_use[name])
        result_tuple = sorted(name_frequence.items(), key=lambda item: item[1], reverse=True)
        #print(result_tuple)
        result = []
        count = 0
        # result_tuple[0:N]
        for x in result_tuple:
            result.append(x[0])
            count += 1
            if count >= N:
                break
        return result

    def get_gender_ratio(self, gender):
        if gender not in ['BOY', 'GIRL']:
            print('Sorry! The gender ', gender, ' is not acceptable')
            exit(0)
        total_babies = 0
        target_gender_babies = 0
        for name in self.database.keys():
            for gender_data in self.database[name]:
                total_babies += 1
                if gender_data == gender:
                    target_gender_babies += 1
        return target_gender_babies / total_babies

    def read_origins_from_file(self, origins_filename):
        self.database_origin = {}
        try:
            for line in open(origins_filename, 'r'):
                name_origin = re.findall(r'[A-Z][a-zA-Z]*.?[a-zA-Z]+', line)
                self.database_origin[name_origin[0]] = name_origin[1]
        except FileNotFoundError:
            print("Sorry! The file " + origins_filename + " can't find.")
            exit(0)

    def get_origin_counts(self):
        result_dict = {}
        for name in self.database.keys():
            number = len(self.database[name])
            if name in self.database_origin.keys():
                origin = self.database_origin[name]
            else:
                continue
            if origin not in result_dict:
                result_dict[origin] = number
            else:
                result_dict[origin] += number
        result = []
        for name in result_dict.keys():
            result.append((name, result_dict[name]))
        return result


    # def gender_accept(self, gender):
    #     if
    #
b = Babies('test/scotbabies2015.txt')
print(b.get_names_beginning_with('kbc'))
# bb = babynames_reference.Babies('scotbabies2015.txt')
