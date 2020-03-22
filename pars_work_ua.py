from functions import *
from data_base import save_to_db


def main():
    page = 0

    while True:
        page += 1

        if page == 2:
            break

        payload = {
            'ss': 1,
            'page': page,
        }

        headers = user_agent_generator()

        # tegname div > a
        # class OR/AND id

        print(f'PAGE: {page}')
        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        random_sleep()
        response.raise_for_status()

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        class_ = 'card card-hover card-visited wordwrap job-link'
        cards = soup.find_all('div', class_=class_)
        cards += soup.find_all('div', class_=class_ + ' js-hot-block')

        result = []

        if not cards:
            break

        # Collecting all information about the vacancy:
        for card in cards:

            # Main information about the vacancy:
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']
            try:
                salary = card.find('div', class_='').find('b').text
            except AttributeError:
                salary = 'No information'
            company_name = card.find('div', class_='add-top-xs').find('span', class_='').find('b').text

            # Additional information about the vacancy from additional request:
            soup_additional = vacancy_review(href, headers)
            try:
                people = soup_additional.find('span', class_='add-top-xs').find('span', class_='nowrap').text
            except AttributeError:
                people = 'No information'
            try:
                address_requirements = soup_additional.find_all('p', class_='text-indent add-top-sm')
                for i in address_requirements:
                    if i.find('span', attrs={"title": "Адрес работы"}):
                        address = i.text.strip().split('.')[0]
                    elif i.find('span', attrs={"title": "Условия и требования"}):
                        requirements = i.text.strip().split('.')
                        requirements_return = ''.join(i.strip() + '. ' for i in requirements)[:-3]
            except AttributeError:
                address = 'No information'
                requirements_return = 'No information'
            try:
                description = soup_additional.find('div', id='job-description').find_all(['p', 'b', 'li'])
                description_return = ''.join(i.text + '\n' for i in description)
            except AttributeError:
                description_return = 'No information'

            # Collecting the results:
            result.append([f'Position: {title}, '
                           f'Link_id: {href}, '
                           f'Salary: {salary}, '
                           f'Company: {company_name}, '
                           f'People count: {people}, '
                           f'Address: {address}, '
                           f'Requirements: {requirements_return},'
                           f'Description: \n{description_return}'
                           ]
                          )
            save_to_db(title, href, salary, company_name, people,
                       address, requirements_return, description_return)
            data_json = {
                'title': title,
                'link': href,
                'salary': salary,
                'company': company_name,
                'people': people,
                'address': address,
                'requirements': requirements_return,
                'description': description_return
            }
            save_info_json(data_json)

        save_info(result)


if __name__ == '__main__':
    main()
