import warnings

class Result(dict):
    def __init__(self, parsed_result):
        super().__init__()
        self.parsed_result = parsed_result
        self.update(parsed_result)


    def _key(self, key, dict=None):
        if dict is None:
            dict = self.parsed_result
        try:
            value = dict[key]
        except KeyError:
            value = ''
        except TypeError:
            value = ''
        return value

    
    def parsed(self):
        return self._key('parsed')


    def canonical(self):
        return self._key('canonical')

    
    def canonical_stemmed(self):
        return self._key('stemmed', dict=self.canonical())

    
    def canonical_simple(self):
        return self._key('simple', dict=self.canonical())

    
    def canonical_full(self):
        return self._key('full', dict=self.canonical())

    def authorship_details(self):
        if self.hybrid() == 'HYBRID_FORMULA':
            authorship = ['', '']
            for i in range(2):
                rank = next(iter(self.details()['hybridFormula'][i]))
                if 'authorship' in self.details()['hybridFormula'][i][rank]:
                    authorship[i] = self.details()['hybridFormula'][i][rank]['authorship']
                else:
                    authorship[i] = ''
        else:
            authorship = self._key('authorship')
        return authorship

    def authorship_verbatim(self):
        return self._key('verbatim', dict=self.authorship_details())

    
    def authorship_normalized(self):
        return self._key('normalized', dict=self.authorship_details())

    
    def authorship_year(self):
        return self._key('year', dict=self.authorship_details())
    

    def is_hybrid(self):
        return 'hybrid' in self


    def hybrid(self):
        return self._key('hybrid')


    def page(self):
        verbatim_authorship = self.authorship_verbatim()
        if ':' in verbatim_authorship:
            page = verbatim_authorship.split(':')[-1].strip()
        else:
            page = ''
        return page

    
    def _format_authorship(self, authorship_details, et_al_cutoff=4):
        authorship_list = authorship_details['authors']
        match len(authorship_list):
            case 0:
                authorship = ""
            case 1:
                authorship = authorship_list[0]
            case 2:
                authorship = f'{authorship_list[0]} & {authorship_list[1]}'
            case _:
                if len(authorship_list) >= et_al_cutoff:
                    authorship = ', '.join(authorship_list[:1]) + ' et al.'
                else:
                    authorship = ', '.join(authorship_list[:-1]) + f' & {authorship_list[-1]}'
        if 'year' in authorship_details:
            year = self._key('year', dict=authorship_details['year'])
            authorship += f', {year}'
        if 'exAuthors' in authorship_details:
            ex_authorship = self._format_authorship(authorship_details['exAuthors'], et_al_cutoff)
            authorship += f' in {ex_authorship}'
        return authorship


    def authorship(self, et_al_cutoff=4, authorship_details=None):
        if authorship_details is None:
            if self.hybrid() == 'HYBRID_FORMULA':
                warnings.warn('Warning: authorship() returns empty for hybrid formulas. Use hybrid_formula_authorship() instead.', UserWarning)
                return ''
            authorship_details = self.authorship_details()
        authorship = ''
        if authorship_details != '':
            if 'originalAuth' in authorship_details:
                authorship = self._format_authorship(authorship_details['originalAuth'], et_al_cutoff)
            if 'combinationAuth' in authorship_details:
                combination_authorship = self._format_authorship(authorship_details['combinationAuth'], et_al_cutoff)
                authorship = f'({authorship}) {combination_authorship}'

            # handles zoological authorship
            if 'combinationAuth' not in authorship_details and '(' in self.authorship_verbatim():
                authorship = f'({authorship})'
        return authorship
    

    def original_authorship(self, et_al_cutoff=4):
        authorship_details = self.authorship_details()
        authorship = ''
        if authorship_details != '':
            if 'originalAuth' in authorship_details:
                authorship = self._format_authorship(authorship_details['originalAuth'], et_al_cutoff)
        return authorship
    

    def combination_authorship(self, et_al_cutoff=4):
        authorship_details = self.authorship_details()
        authorship = ''
        if authorship_details != '':
            if 'combinationAuth' in authorship_details:
                authorship = self._format_authorship(authorship_details['combinationAuth'], et_al_cutoff)
        return authorship


    def year(self):
        return self.authorship_year()


    def details(self):
        return self._key('details')


    def _details_rank(self):
        return list(self.details().keys())[0]


    def words(self):
        return self._key('words')


    def parser_version(self):
        return self._key('parserVersion')


    def id(self):
        return self._key('id')


    def verbatim(self):
        return self._key('verbatim')


    def normalized(self):
        return self._key('normalized')


    def quality(self):
        return self._key('quality')


    def cardinality(self):
        return self._key('cardinality')


    def tail(self):
        return self._key('tail')


    def quality_warnings(self):
        return self._key('qualityWarnings')


    def uninomial(self):
        return self._key('uninomial', dict=self.details()[self._details_rank()])


    def genus(self):
        return self._key('genus', dict=self.details()[self._details_rank()])


    def hybrid_formula_ranks(self):
        return [next(iter(self.details()['hybridFormula'][0])),
                next(iter(self.details()['hybridFormula'][1]))]


    def hybrid_formula_genera(self):
        ranks = self.hybrid_formula_ranks()
        return [self.details()['hybridFormula'][0][ranks[0]]['genus'],
                self.details()['hybridFormula'][1][ranks[1]]['genus']]


    def subgenus(self):
        return self._key('subgenus', dict=self.details()[self._details_rank()])


    def hybrid_formula_subgenera(self):
        ranks = self.hybrid_formula_ranks()
        return [self.details()['hybridFormula'][0][ranks[0]]['subgenus'],
                self.details()['hybridFormula'][1][ranks[1]]['subgenus']]


    def species(self):
        return self._key('species', dict=self.details()[self._details_rank()])


    def hybrid_formula_species(self):
        ranks = self.hybrid_formula_ranks()
        return [self.details()['hybridFormula'][0][ranks[0]]['species'],
                self.details()['hybridFormula'][1][ranks[1]]['species']]


    def hybrid_formula_authorship(self, et_al_cutoff=4):
        ranks = self.hybrid_formula_ranks()
        authorship = ['', '']
        for i in range(2):
            try:
                if ranks[i] == 'infraspecies':
                    authorship_details = self.details()['hybridFormula'][i][ranks[i]]['infraspecies'][0]['authorship']
                else:
                    authorship_details = self.details()['hybridFormula'][i][ranks[i]]['authorship']
                authorship[i] = self.authorship(et_al_cutoff=et_al_cutoff, authorship_details=authorship_details)
            except KeyError:
                authorship[i] = ''
        return authorship


    def infraspecies_details(self):
        return self._key('infraspecies', dict=self.details()[self._details_rank()])


    def infraspecies(self):
        infraspecies_details = self.infraspecies_details()
        if infraspecies_details != '':
            return self._key('value', dict=infraspecies_details[0])
        else:
            return ''


    def hybrid_formula_infraspecies(self):
        ranks = self.hybrid_formula_ranks()
        result = ['', '']
        for i in range(2):
            try:
                result[i] = self.details()['hybridFormula'][i][ranks[i]]['infraspecies'][0]['value']
            except KeyError:
                pass
        return result


    def infraspecies_rank(self):
        rank = ''
        if self._details_rank() == 'infraspecies':
            if self._key('rank', dict=self.details()[self._details_rank()]['infraspecies'][0]) != '':
                rank = self._key('rank', dict=self.details()[self._details_rank()]['infraspecies'][0])
        return rank


    def __str__(self):
            return self.parsed_result
