import re
from pprint import pprint


class PassportValidator(object):
    required_fields = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
    optional_fields = 'cid'

    def __init__(self):
        self.validate_field = {
            'byr': self.validate_byr,
            'iyr': self.validate_iyr,
            'eyr': self.validate_eyr,
            'hgt': self.validate_hgt,
            'hcl': self.validate_hcl,
            'ecl': self.validate_ecl,
            'pid': self.validate_pid,
            'cid': self.validate_cid
        }

    def passport_has_all_required_fields(self, passport_dict):
        return all(field in passport_dict.keys() for field in self.required_fields)

    def passport_has_all_required_fields_valid(self, passport_dict):
        if not self.passport_has_all_required_fields(passport_dict):
            return False
        return all(self.validate_field[key](value) for (key, value) in passport_dict.items())

    @staticmethod
    def get_list_of_passport_dicts(filename):
        with open(filename, 'r') as file:
            read_passports = file.read().split('\n\n')
        passports = []
        for read_passport in read_passports:
            fields_str = read_passport.replace('\n', ' ').split(' ')
            passport_dict = {field.split(':')[0]: field.split(':')[1] for field in fields_str}
            passports.append(passport_dict)
        return passports

    @staticmethod
    def validate_byr(value):
        return len(value) == 4 and 1920 <= int(value) <= 2002

    @staticmethod
    def validate_iyr(value):
        return len(value) == 4 and 2010 <= int(value) <= 2020

    @staticmethod
    def validate_eyr(value):
        return len(value) == 4 and 2020 <= int(value) <= 2030

    @staticmethod
    def validate_hgt(value):
        if value[-2:] == 'cm':
            return 150 <= int(value[:-2]) <= 193
        if value[-2:] == 'in':
            return 59 <= int(value[:-2]) <= 76
        return False

    @staticmethod
    def validate_hcl(value):
        return re.match(r'^#[\dabcdef]{6}$', value)

    @staticmethod
    def validate_ecl(value):
        valid_eye_colors = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
        return value in valid_eye_colors

    @staticmethod
    def validate_pid(value):
        return re.match(r'^[\d]{9}$', value)

    @staticmethod
    def validate_cid(value):
        return True

    def ex_04_1(self):
        passport_dict_list = self.get_list_of_passport_dicts('input.txt')
        return sum([self.passport_has_all_required_fields(passport) for passport in passport_dict_list])

    def ex_04_2(self):
        passport_dict_list = self.get_list_of_passport_dicts('input.txt')
        for index, passport in enumerate(passport_dict_list):
            success = self.passport_has_all_required_fields_valid(passport)
            if not success:
                if not self.passport_has_all_required_fields(passport):
                    pprint('Passport {} lacks required fields.'.format(index))
                    continue
                else:
                    for key, value in passport.items():
                        if not self.validate_field[key](value):
                            pprint('Passport {} failed because validation failed for field {}:{}'
                                   ''.format(index, key, value))
                            break
        return sum([self.passport_has_all_required_fields_valid(passport) for passport in passport_dict_list])


if __name__ == '__main__':
    pv = PassportValidator()
    print(pv.ex_04_1())
    print(pv.ex_04_2())
