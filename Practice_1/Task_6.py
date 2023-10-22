# List of Observing Activities
# Activities are the records of the observing activities around the world.
# They intend to gather in a single object an observing activity in a given observing site,
# with a given telescope, a given instrument by a given observer, or collaboration or organisation.
# (https://api.arcsecond.io/activities/?page=1769)

import json
from bs4 import BeautifulSoup

str_json = ''
filename = 'text_6_var_33'
with open(filename, encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
data = data['results']


soup = BeautifulSoup('''<table>
    <tr>
        <th>id</th>
        <th>Creation_date</th>
        <th>Date</th>
        <th>Links</th>
        <th>Title</th>
        <th>Content</th>
        <th>Label</th>
        <th>Profile</th>
        <th>Observing_site</th>
        <th>Telescope</th>
        <th>Instrument</th>
        <th>Night_log</th>
        <th>Programme</th>
        <th>Programme_type</th>
        <th>Target_name</th>
        <th>Coordinates</th>
        <th>Organisation</th>
        <th>Collaboration</th>
    </tr>
</table>''', 'html.parser')

table = soup.contents[0]


for tick in data:
    tr = soup.new_tag('tr')
    for key, val in tick.items():
        td = soup.new_tag('td')
        td.string = str(val)
        tr.append(td)
    table.append(tr)


with open('r_text_6_var_33.html', 'w') as result:
    result.write(soup.prettify())
    result.write('\n')