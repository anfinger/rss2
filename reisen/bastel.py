# >>> d = [{
# ...     'name': 'Peter', 'erst': 20, 'dann': 30
# ...     },
# ...     {
# ...     'name': 'Peter', 'erst': 45, 'dann': 70
# ...     }, {
# ...     'name': 'Uwe', 'erst': 9.1, 'dann': 3.8
# ...     }, {
# ...     'name': 'Uwe', 'erst': 1.4, 'dann': 7.2
# ...     }, {
# ...     'name': 'Heinz', 'erst': 555, 'dann': 666
# ...     }]
#
# >>> res = []
# >>> i = 0
#
# >>> for di in d:
# ...     print i
# ...     if i > 0 and res[i-1]['name'] == di['name']:
# ...         res[i-1]['erst_dann'].append((di['erst'], di['dann']))
# ...     else:
# ...         res.append({'name': di['name'], 'erst_dann': [(di['erst'], di['dann']),]})
# ...         i += 1
#
# >>> for r in res:
# ...     print r
# ...
# {'name': 'Peter', 'erst_dann': [(20, 30), (45, 70)]}
# {'name': 'Uwe', 'erst_dann': [(9.1, 3.8), (1.4, 7.2)]}
# {'name': 'Heinz', 'erst_dann': [(555, 666)]}
