import vcr
import re
import pytest
from pygnparser import gnparser
import warnings


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_Smith.yaml")
def test_version():
    res = gnparser('Aus bus cus (Smith, 1999)')
    assert re.match(r'v\d+\.\d+\.\d+', res.parser_version())


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_Smith.yaml")
def test_id():
    res = gnparser('Aus bus cus (Smith, 1999)')
    assert re.match(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$', res.id())


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_Smith.yaml")
def test_parsed():
    res = gnparser('Aus bus cus (Smith, 1999)')
    assert res.parsed() is True


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_Smith.yaml")
def test_cardinality():
    res = gnparser('Aus bus cus (Smith, 1999)')
    assert res.cardinality() == 3


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_quality():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.quality() == 1


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_verbatim():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.verbatim() == 'Aus (Bus) cus dus (Smith, 1980)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_normalized():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.normalized() == 'Aus (Bus) cus dus (Smith 1980)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_canonical():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.canonical() == {'stemmed': 'Aus cus dus', 'simple': 'Aus cus dus', 'full': 'Aus cus dus'}


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_canonical_stemmed():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.canonical_stemmed() == 'Aus cus dus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_canonical_simple():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.canonical_simple() == 'Aus cus dus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_canonical_full():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.canonical_full() == 'Aus cus dus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_authorship_details():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert 'verbatim' in res.authorship_details()


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_details():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert 'infraspecies' in res.details()
    

@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_infraspecies_details():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert 'value' in res.infraspecies_details()[0]


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_words():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert 'start' in res.words()[0]


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_genus():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.genus() == 'Aus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_subgenus():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.subgenus() == 'Bus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_species():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.species() == 'cus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_infraspecies():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.infraspecies() == 'dus'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_infraspecies_rank():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.infraspecies_rank() == ''


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_var_dus.yaml")
def test_parse_infraspecies_var_rank():
    res = gnparser('Aus (Bus) cus var. dus (Smith, 1980)')
    assert res.infraspecies_rank() == 'var.'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_authorship_verbatim():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.authorship_verbatim() == '(Smith, 1980)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_authorship_normalized():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.authorship_normalized() == '(Smith 1980)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_authorship_year():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.authorship_year() == '1980'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_year():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.year() == '1980'

@vcr.use_cassette("test/vcr_cassettes/test_parse_Aus_cus_dus.yaml")
def test_parse_authorship():
    res = gnparser('Aus (Bus) cus dus (Smith, 1980)')
    assert res.authorship() == '(Smith, 1980)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_genus():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.genus() == 'Naja'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_species():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.species() == 'porphyrica'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_tail():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.tail() == ' (in error pro Coluber porphyriacus)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_authorship_verbatim():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.authorship_verbatim() == 'SCHLEGEL 1837: 479'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_authorship_normalized():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.authorship_normalized() == 'Schlegel 1837'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_authorship_year():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.authorship_year() == '1837'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Naja_porphyrica.yaml")
def test_parse_Naja_porphyrica_authorship():
    res = gnparser('Naja porphyrica SCHLEGEL 1837: 479 (in error pro Coluber porphyriacus)')
    assert res.authorship() == 'Schlegel, 1837'


@vcr.use_cassette("test/vcr_cassettes/test_parse_4_authors.yaml")
def test_parse_4_authors():
    res = gnparser('Aus bus cus (Smith, Anderson, Jones, & Ryan, 1999)')
    assert res.authorship(et_al_cutoff=5) == '(Smith, Anderson, Jones & Ryan, 1999)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_3_authors.yaml")
def test_parse_3_authors():
    res = gnparser('Aus bus cus (Smith, Anderson & Ryan, 1999)')
    assert res.authorship() == '(Smith, Anderson & Ryan, 1999)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_3_authors_no_brackets.yaml")
def test_parse_3_authors_no_brackets():
    res = gnparser('Aus bus cus Smith, Anderson & Ryan, 1999')
    assert res.authorship() == 'Smith, Anderson & Ryan, 1999'
    assert res.original_authorship() == 'Smith, Anderson & Ryan, 1999'
    assert res.combination_authorship() == ''


@vcr.use_cassette("test/vcr_cassettes/test_parse_2_authors.yaml")
def test_parse_2_authors():
    res = gnparser('Aus bus cus (Smith & Anderson, 1999)')
    assert res.authorship() == '(Smith & Anderson, 1999)'
    assert res.original_authorship() == 'Smith & Anderson, 1999'
    assert res.combination_authorship() == ''


@vcr.use_cassette("test/vcr_cassettes/test_parse_2_authors_no_brackets.yaml")
def test_parse_2_authors_no_brackets():
    res = gnparser('Aus bus cus Smith & Anderson, 1999')
    assert res.authorship() == 'Smith & Anderson, 1999'


@vcr.use_cassette("test/vcr_cassettes/test_parse_1_author.yaml")
def test_parse_1_author():
    res = gnparser('Aus bus cus (Smith, 1999)')
    assert res.authorship() == '(Smith, 1999)'


@vcr.use_cassette("test/vcr_cassettes/test_parse_1_author_no_brackets.yaml")
def test_parse_1_author_no_brackets():
    res = gnparser('Aus bus cus Smith, 1999')
    assert res.authorship() == 'Smith, 1999'


@vcr.use_cassette("test/vcr_cassettes/test_parse_in_original.yaml")
def test_parse_in_original():
    res = gnparser('Aus bus cus Smith in Richards, 1999')
    assert res.authorship() == 'Smith in Richards, 1999'


@vcr.use_cassette("test/vcr_cassettes/test_parse_in_original_comb.yaml")
def test_parse_in_original_comb():
    res = gnparser('Aus bus cus (Smith in Richards, 1999) Ryan in Anderson, Smith, & Jones, 2000')
    assert res.authorship() == '(Smith in Richards, 1999) Ryan in Anderson, Smith & Jones, 2000'


@vcr.use_cassette("test/vcr_cassettes/test_parse_Ablepharus_pannonicus.yaml")
def test_parse_Ablepharus_pannonicus():
    res = gnparser('Ablepharus pannonicus Fitzinger in Eversmann, 1823: 145 (Nom. Nud., In Error)')
    assert res.genus() == 'Ablepharus'
    assert res.species() == 'pannonicus'
    assert res.infraspecies() == ''
    assert res.authorship() == 'Fitzinger in Eversmann, 1823'
    assert res.original_authorship() == 'Fitzinger in Eversmann, 1823'
    assert res.combination_authorship() == ''
    assert res.page() == '145'
    assert res.quality_warnings() == [{'quality': 4, 'warning': 'Unparsed tail'}, {'quality': 2, 'warning': 'Ex authors are not required (ICZN only)'}, {'quality': 2, 'warning': 'Year with page info'}]
    assert res.tail().strip() == '(Nom. Nud., In Error)'
    assert res.is_hybrid() == False


@vcr.use_cassette("test/vcr_cassettes/test_parse_Aspidoscelis_neavesi.yaml")
def test_parse_Aspidoscelis_neavesi():
    res = gnparser('Aspidoscelis neavesi Cole, Taylor, Baumann & Baumann, 2014 (Part)')
    assert res.genus() == 'Aspidoscelis'
    assert res.species() == 'neavesi'
    assert res.infraspecies() == ''
    assert res.authorship() == 'Cole et al., 2014'
    assert res.original_authorship() == 'Cole et al., 2014'
    assert res.combination_authorship() == ''
    assert res.page() == ''
    assert res.tail().strip() == '(Part)'
    assert res.is_hybrid() == False


@vcr.use_cassette("test/vcr_cassettes/test_parse_Atuechosaurus_travancoricus.yaml")
def test_parse_Atuechosaurus_travancoricus():
    res = gnparser('Atuechosaurus travancoricus Beddome, 1870: 33 (Part.)')
    assert res.genus() == 'Atuechosaurus'
    assert res.species() == 'travancoricus'
    assert res.infraspecies() == ''
    assert res.authorship() == 'Beddome, 1870'
    assert res.original_authorship() == 'Beddome, 1870'
    assert res.combination_authorship() == ''
    assert res.page() == '33'
    assert res.tail().strip() == '(Part.)'
    assert res.is_hybrid() == False


@vcr.use_cassette("test/vcr_cassettes/test_parse_Calyptoprymnus_verecundus.yaml")
def test_parse_Calyptoprymnus_verecundus():
    res = gnparser('Calyptoprymnus verecundus De Vis, 1905: 46 (Fide Moody, 1977)')
    assert res.genus() == 'Calyptoprymnus'
    assert res.species() == 'verecundus'
    assert res.infraspecies() == ''
    assert res.authorship() == 'De Vis, 1905'
    assert res.page() == '46'
    assert res.tail().strip() == '(Fide Moody, 1977)'
    assert res.is_hybrid() == False


@vcr.use_cassette("test/vcr_cassettes/test_parse_Ablepharus_chernovi_ressli.yaml")
def test_parse_Ablepharus_chernovi_ressli():
    res = gnparser('Ablepharus chernovi ressli SCHMIDTLER 1997\u001d')
    assert res.quality() == 4
    assert res.genus() == 'Ablepharus'
    assert res.species() == 'chernovi'
    assert res.infraspecies() == 'ressli'
    assert res.authorship_verbatim() == ''  # GNParser's behavior is for the authorship to not parse because of the \u001d character
    assert res.authorship() == ''
    assert res.page() == ''
    assert res.is_hybrid() == False


@vcr.use_cassette("test/vcr_cassettes/test_parse_et_al_default.yaml")
def test_parse_et_al_default():
    res = gnparser('Aus bus cus (Smith, Anderson, Jones, & Peters in Richards, Shultz, Anderson & Smith, 1999) Ryan in Anderson, Smith, & Jones, 2000')
    assert res.authorship() == '(Smith et al. in Richards et al., 1999) Ryan in Anderson, Smith & Jones, 2000'
    assert res.original_authorship() == 'Smith, Anderson, Jones, & Peters in Richards, Shultz, Anderson & Smith, 1999'
    assert res.combination_authorship() == 'Ryan in Anderson, Smith & Jones, 2000'


@vcr.use_cassette("test/vcr_cassettes/test_parse_et_al_5.yaml")
def test_parse_et_al_default():
    res = gnparser('Aus bus cus (Smith, Anderson, Jones, O\'Brian & Peters in Richards, Shultz, Anderson & Smith, 1999) Ryan in Anderson, Smith, & Jones, 2000')
    assert res.authorship(et_al_cutoff=5) == '(Smith et al. in Richards, Shultz, Anderson & Smith, 1999) Ryan in Anderson, Smith & Jones, 2000'
    assert res.original_authorship(et_al_cutoff=5) == 'Smith et al. in Richards, Shultz, Anderson & Smith, 1999'
    assert res.combination_authorship(et_al_cutoff=5) == 'Ryan in Anderson, Smith & Jones, 2000'


@vcr.use_cassette("test/vcr_cassettes/test_infraspecies_rank_on_species.yaml")
def test_infraspecies_rank_on_species():
    res = gnparser('Aus bus (Smith, 1999)')
    assert res.infraspecies_rank() == ''
    assert res.infraspecies() == ''
    assert res.is_hybrid() == False


@vcr.use_cassette("test/vcr_cassettes/test_hybrid_formula.yaml")
def test_hybrid_formula():
    res = gnparser('Isoetes lacustris x stricta Gay')
    assert res.is_hybrid() == True
    assert res.hybrid() == 'HYBRID_FORMULA'
    assert res.normalized() == 'Isoetes lacustris × Isoetes stricta Gay'
    assert res.hybrid_formula_ranks() == ['species', 'species']
    assert res.hybrid_formula_genera() == ['Isoetes', 'Isoetes']
    assert res.hybrid_formula_species() == ['lacustris', 'stricta']
    assert res.hybrid_formula_infraspecies() == ['', '']
    assert res.hybrid_formula_authorship() == ['', 'Gay']
    with pytest.warns(UserWarning, match='Warning\: authorship\(\) returns empty for hybrid formulas. Use hybrid_formula_authorship\(\) instead.'):
        assert res.authorship() == ''
    #assert res.original_authorship() == ''
    #assert res.combination_authorship() == ''


@vcr.use_cassette("test/vcr_cassettes/test_hybrid_formula2.yaml")
def test_hybrid_formula_2():
    res = gnparser('Phegopteris connectilis × Dryopteris filix-mas')
    assert res.is_hybrid() == True
    assert res.hybrid() == 'HYBRID_FORMULA'
    assert res.normalized() == 'Phegopteris connectilis × Dryopteris filix-mas'


@vcr.use_cassette("test/vcr_cassettes/test_hybrid_formula3.yaml")
def test_hybrid_formula_3():
    res = gnparser('Aus bus Smith x Aus cus dus L.')
    assert res.is_hybrid() == True
    assert res.hybrid() == 'HYBRID_FORMULA'
    assert res.normalized() == 'Aus bus Smith × Aus cus dus L.'
    assert res.hybrid_formula_ranks() == ['species', 'infraspecies']
    assert res.hybrid_formula_genera() == ['Aus', 'Aus']
    assert res.hybrid_formula_species() == ['bus', 'cus']
    assert res.hybrid_formula_infraspecies() == ['', 'dus']
    assert res.hybrid_formula_authorship() == ['Smith', 'L.']


@vcr.use_cassette("test/vcr_cassettes/test_named_hybrid.yaml")
def test_named_hybrid():
    res = gnparser('× Triticosecale semisecale (Mackey) K.Hammer & Filat.')
    assert res.is_hybrid() == True
    assert res.hybrid() == 'NAMED_HYBRID'
    assert res.normalized() == '× Triticosecale semisecale (Mackey) K. Hammer & Filat.'
    assert res.canonical_full() == '× Triticosecale semisecale'
    assert res.canonical_simple() == 'Triticosecale semisecale'
    assert res.genus() == 'Triticosecale'
    assert res.species() == 'semisecale'
    assert res.authorship() == '(Mackey) K. Hammer & Filat.'
    assert res.original_authorship() == 'Mackey'
    assert res.combination_authorship() == 'K. Hammer & Filat.'


@vcr.use_cassette("test/vcr_cassettes/test_named_hybrid2.yaml")
def test_named_hybrid2():
    res = gnparser('Petunia × atkinsiana (Sweet) D. Don ex W. H. Baxter')
    assert res.is_hybrid() == True
    assert res.hybrid() == 'NAMED_HYBRID'
    assert res.normalized() == 'Petunia × atkinsiana (Sweet) D. Don ex W. H. Baxter'
    assert res.canonical_stemmed() == 'Petunia atkinsian'
    assert res.canonical_full() == 'Petunia × atkinsiana'
    assert res.canonical_simple() == 'Petunia atkinsiana'
    assert res.genus() == 'Petunia'
    assert res.species() == 'atkinsiana'
    assert res.authorship() == '(Sweet) D. Don in W. H. Baxter'
    assert res.original_authorship() == 'Sweet'
    assert res.combination_authorship() == 'D. Don in W. H. Baxter'


@vcr.use_cassette("test/vcr_cassettes/test_uninomial.yaml")
def test_uninomial():
    res = gnparser('Dennstaedtiaceae Lotsy')
    assert res._details_rank() == 'uninomial'
    assert res.uninomial() == 'Dennstaedtiaceae'
    assert res.genus() == ''
    assert res.species() == ''
    assert res.infraspecies() == ''
    assert res.authorship() == 'Lotsy'
    assert res.is_hybrid() == False


# despite Microlepia being a genus, GNParser will treat it as a uninomial
#   unless it is combined with a specific epithet, so use res.uninomial() instead of res.genus()
@vcr.use_cassette("test/vcr_cassettes/test_uninomial2.yaml")
def test_uninomial():
    res = gnparser('Microlepia C.Presl')
    assert res._details_rank() == 'uninomial'
    assert res.uninomial() == 'Microlepia'
    assert res.genus() == ''
    assert res.species() == ''
    assert res.infraspecies() == ''
    assert res.authorship() == 'C. Presl'
    assert res.is_hybrid() == False
