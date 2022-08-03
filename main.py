from pprint import pprint
import re
import csv


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


def norm_phone_nmbr(number):
    norm_form = r'(\+7|8)?(\s*|-)\(?(\d+)\)?(\s*|\s?|-)' + r'(\d{3})(\-|\s*)(\d{2})(\-|\s*)*(\d{2})(\s\(?)?(\доб.\s*\d+)?\)?'
    return re.sub(norm_form, r'+7(\3)\5-\7-\9 \11', number)


def get_norm_list(addr_book_list):
    new_list = []
    new_list.append(addr_book_list[0])
    for item in addr_book_list[1:]:
        flg_appnd = True
        new_item = ' '.join(item[:3]).strip().split(' ')
        if len(new_item) < 3:
            while len(new_item) < 3:
                new_item.append('')
        new_item += item[3:7]
        new_item[5] = norm_phone_nmbr(item[5])
        pass
        for exist_item in new_list:
            if new_item[0] == exist_item[0] and new_item[1] == exist_item[1] and (new_item[2] == exist_item[2]
                        or new_item[2] == '' or exist_item[2] == ''):
                indx = new_list.index(exist_item)
                for i in range(2, 7):
                    test = new_list[indx][i]
                    if len(new_list[indx][i]) < 2 and len(new_item[i]) > 2:
                          new_list[indx][i] = new_item[i]
                flg_appnd = False
                break
        if flg_appnd:
            new_list.append(new_item)
    return new_list


norm_list = get_norm_list(contacts_list)


if __name__ == '__main__':
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(norm_list)
