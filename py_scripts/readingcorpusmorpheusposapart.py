# readingcorpus.py
# to build a dictionary to consult a corpus from 
# https://github.com/proiel/proiel-treebank/releases/tag/20180408

from xml.dom import minidom
import json 
import collections
import requests 
# import betacode.conv

# parse an xml file by name
# mydoc = minidom.parse('hdt.xml')
#mydoc = minidom.parse('greek-nt.xml')
#mydoc = minidom.parse('greek.xml')

mydoc = minidom.parse('MorpheusUnicode.xml')


def extend(a,b):
    """Create a new dictionary with a's properties extended by b,
    without overwriting.

    >>> extend({'a':1,'b':2},{'b':3,'c':4})
    {'a': 1, 'c': 4, 'b': 2}
    """
    return dict(b,**a)

items = mydoc.getElementsByTagName('t')


    #     <parts-of-speech>
    #  <value tag="A-" summary="adjective"/>
    #  <value tag="Df" summary="adverb"/>
    #  <value tag="S-" summary="article"/>
    #  <value tag="Ma" summary="cardinal numeral"/>
    #  <value tag="Nb" summary="common noun"/>
    #  <value tag="C-" summary="conjunction"/>
    #  <value tag="Pd" summary="demonstrative pronoun"/>
    #  <value tag="F-" summary="foreign word"/>
    #  <value tag="Px" summary="indefinite pronoun"/>
    #  <value tag="N-" summary="infinitive marker"/>
    #  <value tag="I-" summary="interjection"/>
    #  <value tag="Du" summary="interrogative adverb"/>
    #  <value tag="Pi" summary="interrogative pronoun"/>
    #  <value tag="Mo" summary="ordinal numeral"/>
    #  <value tag="Pp" summary="personal pronoun"/>
    #  <value tag="Pk" summary="personal reflexive pronoun"/>
    #  <value tag="Ps" summary="possessive pronoun"/>
    #  <value tag="Pt" summary="possessive reflexive pronoun"/>
    #  <value tag="R-" summary="preposition"/>
    #  <value tag="Ne" summary="proper noun"/>
    #  <value tag="Py" summary="quantifier"/>
    #  <value tag="Pc" summary="reciprocal pronoun"/>
    #  <value tag="Dq" summary="relative adverb"/>
    #  <value tag="Pr" summary="relative pronoun"/>
    #  <value tag="G-" summary="subjunction"/>
    #  <value tag="V-" summary="verb"/>
    #  <value tag="X-" summary="unassigned"/>
    #</parts-of-speech>
univ_pos_name_variants = {
"---------" : "x",
"--p---fa-" : "x",
"--s---ma-" : "x",
"-3paia---" : "x",
"-3paim---" : "x",
"-3siia---" : "x",
"a--------" : "adj",
"a-------s" : "adj",
"a-d---fa-" : "adj",
"a-d---fd-" : "adj",
"a-d---fg-" : "adj",
"a-d---fn-" : "adj",
"a-d---ma-" : "adj",
"a-d---md-" : "adj",
"a-d---mg-" : "adj",
"a-d---mn-" : "adj",
"a-d---mnc" : "adj",
"a-d---mv-" : "adj",
"a-d---na-" : "adj",
"a-d---ng-" : "adj",
"a-d---nn-" : "adj",
"a-p----dc" : "adj",
"a-p---fa-" : "adj",
"a-p---fac" : "adj",
"a-p---fas" : "adj",
"a-p---fd-" : "adj",
"a-p---fdc" : "adj",
"a-p---fds" : "adj",
"a-p---fg-" : "adj",
"a-p---fgc" : "adj",
"a-p---fn-" : "adj",
"a-p---fnc" : "adj",
"a-p---fns" : "adj",
"a-p---fv-" : "adj",
"a-p---m--" : "adj",
"a-p---m-c" : "adj",
"a-p---ma-" : "adj",
"a-p---mac" : "adj",
"a-p---mas" : "adj",
"a-p---md-" : "adj",
"a-p---mdc" : "adj",
"a-p---mds" : "adj",
"a-p---mg-" : "adj",
"a-p---mgc" : "adj",
"a-p---mgs" : "adj",
"a-p---mn-" : "adj",
"a-p---mnc" : "adj",
"a-p---mns" : "adj",
"a-p---mv-" : "adj",
"a-p---mvs" : "adj",
"a-p---na-" : "adj",
"a-p---nac" : "adj",
"a-p---nas" : "adj",
"a-p---nd-" : "adj",
"a-p---ndc" : "adj",
"a-p---nds" : "adj",
"a-p---ng-" : "adj",
"a-p---ngs" : "adj",
"a-p---nn-" : "adj",
"a-p---nnc" : "adj",
"a-p---nns" : "adj",
"a-p---nv-" : "adj",
"a-s----d-" : "adj",
"a-s----dc" : "adj",
"a-s----g-" : "adj",
"a-s----gc" : "adj",
"a-s---fa-" : "adj",
"a-s---fac" : "adj",
"a-s---fas" : "adj",
"a-s---fd-" : "adj",
"a-s---fds" : "adj",
"a-s---fg-" : "adj",
"a-s---fgc" : "adj",
"a-s---fgs" : "adj",
"a-s---fn-" : "adj",
"a-s---fnc" : "adj",
"a-s---fns" : "adj",
"a-s---fv-" : "adj",
"a-s---m--" : "adj",
"a-s---ma-" : "adj",
"a-s---mac" : "adj",
"a-s---mas" : "adj",
"a-s---md-" : "adj",
"a-s---mdc" : "adj",
"a-s---mds" : "adj",
"a-s---mg-" : "adj",
"a-s---mgc" : "adj",
"a-s---mgs" : "adj",
"a-s---mn-" : "adj",
"a-s---mnc" : "adj",
"a-s---mns" : "adj",
"a-s---mv-" : "adj",
"a-s---mvc" : "adj",
"a-s---mvs" : "adj",
"a-s---na-" : "adj",
"a-s---nac" : "adj",
"a-s---nas" : "adj",
"a-s---nd-" : "adj",
"a-s---ndc" : "adj",
"a-s---nds" : "adj",
"a-s---ng-" : "adj",
"a-s---nn-" : "adj",
"a-s---nnc" : "adj",
"a-s---nns" : "adj",
"a-s---nv-" : "adj",
"a-s---nvs" : "adj",
"c--------" : "cconj",
"c--------" : "sconj",
"d--------" : "adv",
"d-------c" : "adv",
"d-------s" : "adv",
"g--------" : "part",
"i--------" : "intj",
"l--------" : "det",
"l-d---fa-" : "det",
"l-d---fg-" : "det",
"l-d---mg-" : "det",
"l-d---mn-" : "det",
"l-d---na-" : "det",
"l-d---nn-" : "det",
"l-p---fa-" : "det",
"l-p---fd-" : "det",
"l-p---fg-" : "det",
"l-p---fn-" : "det",
"l-p---ma-" : "det",
"l-p---md-" : "det",
"l-p---mg-" : "det",
"l-p---mn-" : "det",
"l-p---na-" : "det",
"l-p---nd-" : "det",
"l-p---ng-" : "det",
"l-p---nn-" : "det",
"l-s---fa-" : "det",
"l-s---fd-" : "det",
"l-s---fg-" : "det",
"l-s---fn-" : "det",
"l-s---ma-" : "det",
"l-s---md-" : "det",
"l-s---mg-" : "det",
"l-s---mn-" : "det",
"l-s---na-" : "det",
"l-s---nd-" : "det",
"l-s---ng-" : "det",
"l-s---nn-" : "det",
"m--------" : "num",
"m-p---m--" : "num",
"m-p---md-" : "num",
"m-p---nn-" : "num",
"n-----fg-" : "noun",
"n-----na-" : "noun",
"n-----nn-" : "noun",
"n-d----a-" : "noun",
"n-d---fa-" : "noun",
"n-d---fd-" : "noun",
"n-d---fg-" : "noun",
"n-d---fn-" : "noun",
"n-d---ma-" : "noun",
"n-d---md-" : "noun",
"n-d---mg-" : "noun",
"n-d---mn-" : "noun",
"n-d---mv-" : "noun",
"n-d---na-" : "noun",
"n-d---nn-" : "noun",
"n-p----d-" : "noun",
"n-p----g-" : "noun",
"n-p---fa-" : "noun",
"n-p---fd-" : "noun",
"n-p---fg-" : "noun",
"n-p---fn-" : "noun",
"n-p---fv-" : "noun",
"n-p---ma-" : "noun",
"n-p---md-" : "noun",
"n-p---mg-" : "noun",
"n-p---mn-" : "noun",
"n-p---mv-" : "noun",
"n-p---na-" : "noun",
"n-p---nd-" : "noun",
"n-p---ng-" : "noun",
"n-p---nn-" : "noun",
"n-p---nv-" : "noun",
"n-s----d-" : "noun",
"n-s----g-" : "noun",
"n-s----n-" : "noun",
"n-s----v-" : "noun",
"n-s---fa-" : "noun",
"n-s---fd-" : "noun",
"n-s---fg-" : "noun",
"n-s---fn-" : "noun",
"n-s---fv-" : "noun",
"n-s---m--" : "noun",
"n-s---ma-" : "noun",
"n-s---md-" : "noun",
"n-s---mg-" : "noun",
"n-s---mn-" : "noun",
"n-s---mv-" : "noun",
"n-s---na-" : "noun",
"n-s---nd-" : "noun",
"n-s---ng-" : "noun",
"n-s---nn-" : "noun",
"n-s---nv-" : "noun",
"p--------" : "pron",
"p-d----d-" : "pron",
"p-d----n-" : "pron",
"p-d---fa-" : "pron",
"p-d---fd-" : "pron",
"p-d---fg-" : "pron",
"p-d---fn-" : "pron",
"p-d---ma-" : "pron",
"p-d---md-" : "pron",
"p-d---mg-" : "pron",
"p-d---mn-" : "pron",
"p-d---mv-" : "pron",
"p-p----a-" : "pron",
"p-p----d-" : "pron",
"p-p----g-" : "pron",
"p-p----n-" : "pron",
"p-p---fa-" : "pron",
"p-p---fd-" : "pron",
"p-p---fg-" : "pron",
"p-p---fn-" : "pron",
"p-p---ma-" : "pron",
"p-p---md-" : "pron",
"p-p---mg-" : "pron",
"p-p---mn-" : "pron",
"p-p---na-" : "pron",
"p-p---nd-" : "pron",
"p-p---ng-" : "pron",
"p-p---nn-" : "pron",
"p-s----a-" : "pron",
"p-s----d-" : "pron",
"p-s----g-" : "pron",
"p-s----n-" : "pron",
"p-s---fa-" : "pron",
"p-s---fd-" : "pron",
"p-s---fg-" : "pron",
"p-s---fn-" : "pron",
"p-s---ma-" : "pron",
"p-s---md-" : "pron",
"p-s---mg-" : "pron",
"p-s---mn-" : "pron",
"p-s---mv-" : "pron",
"p-s---na-" : "pron",
"p-s---nd-" : "pron",
"p-s---ng-" : "pron",
"p-s---nn-" : "pron",
"p1p---fa-" : "pron",
"p1p---ma-" : "pron",
"p1p---md-" : "pron",
"p1p---mg-" : "pron",
"p1p---mn-" : "pron",
"p1s---fa-" : "pron",
"p1s---fd-" : "pron",
"p1s---fg-" : "pron",
"p1s---fn-" : "pron",
"p1s---ma-" : "pron",
"p1s---md-" : "pron",
"p1s---mg-" : "pron",
"p1s---mn-" : "pron",
"p2p----a-" : "pron",
"p2p----d-" : "pron",
"p2p---ma-" : "pron",
"p2p---mg-" : "pron",
"p2p---mn-" : "pron",
"p2s----a-" : "pron",
"p2s----d-" : "pron",
"p2s----g-" : "pron",
"p2s----n-" : "pron",
"p2s---ma-" : "pron",
"p2s---md-" : "pron",
"p2s---mg-" : "pron",
"p3s---fa-" : "pron",
"p3s---ma-" : "pron",
"r--------" : "adp",
"u--------" : "punct",
"v---na---" : "verb",
"v--amm---" : "verb",
"v--an----" : "verb",
"v--ana---" : "verb",
"v--ane---" : "verb",
"v--anm---" : "verb",
"v--anp---" : "verb",
"v--fna---" : "verb",
"v--fne---" : "verb",
"v--fnm---" : "verb",
"v--fnp---" : "verb",
"v--pna---" : "verb",
"v--pnd---" : "verb",
"v--pne---" : "verb",
"v--pnp---" : "verb",
"v--ppefa-" : "verb",
"v--ppemn-" : "verb",
"v--rn----" : "verb",
"v--rna---" : "verb",
"v--rne---" : "verb",
"v--rnp---" : "verb",
"v--tna---" : "verb",
"v-dapafn-" : "verb",
"v-dapama-" : "verb",
"v-dapamg-" : "verb",
"v-dapamn-" : "verb",
"v-dapmfn-" : "verb",
"v-dapmmn-" : "verb",
"v-dappma-" : "verb",
"v-dappmn-" : "verb",
"v-dppafg-" : "verb",
"v-dppama-" : "verb",
"v-dppamn-" : "verb",
"v-dppefn-" : "verb",
"v-dppema-" : "verb",
"v-dppemd-" : "verb",
"v-dppemn-" : "verb",
"v-dpppmn-" : "verb",
"v-drpama-" : "verb",
"v-drpamn-" : "verb",
"v-drpefn-" : "verb",
"v-drpemn-" : "verb",
"v-p-pmma-" : "verb",
"v-pap-mn-" : "verb",
"v-papafa-" : "verb",
"v-papafg-" : "verb",
"v-papafn-" : "verb",
"v-papama-" : "verb",
"v-papamd-" : "verb",
"v-papamg-" : "verb",
"v-papamn-" : "verb",
"v-papana-" : "verb",
"v-papand-" : "verb",
"v-papann-" : "verb",
"v-papefn-" : "verb",
"v-papema-" : "verb",
"v-papemn-" : "verb",
"v-papmfa-" : "verb",
"v-papmfg-" : "verb",
"v-papmfn-" : "verb",
"v-papmma-" : "verb",
"v-papmmd-" : "verb",
"v-papmmg-" : "verb",
"v-papmmn-" : "verb",
"v-papmna-" : "verb",
"v-papmng-" : "verb",
"v-papmnn-" : "verb",
"v-pappfd-" : "verb",
"v-pappfg-" : "verb",
"v-pappfn-" : "verb",
"v-pappma-" : "verb",
"v-pappmd-" : "verb",
"v-pappmg-" : "verb",
"v-pappmn-" : "verb",
"v-pappna-" : "verb",
"v-pappng-" : "verb",
"v-pappnn-" : "verb",
"v-pfpama-" : "verb",
"v-pfpamg-" : "verb",
"v-pfpamn-" : "verb",
"v-pfpema-" : "verb",
"v-pfpemn-" : "verb",
"v-pfpmfa-" : "verb",
"v-pfpmfn-" : "verb",
"v-pfpmma-" : "verb",
"v-pfpmmd-" : "verb",
"v-pfpmmg-" : "verb",
"v-pfpmmn-" : "verb",
"v-pfpmnn-" : "verb",
"v-pfppmn-" : "verb",
"v-ppp-mn-" : "verb",
"v-pppafa-" : "verb",
"v-pppafd-" : "verb",
"v-pppafg-" : "verb",
"v-pppafn-" : "verb",
"v-pppafv-" : "verb",
"v-pppama-" : "verb",
"v-pppamd-" : "verb",
"v-pppamg-" : "verb",
"v-pppamn-" : "verb",
"v-pppamv-" : "verb",
"v-pppana-" : "verb",
"v-pppand-" : "verb",
"v-pppang-" : "verb",
"v-pppann-" : "verb",
"v-pppefa-" : "verb",
"v-pppefd-" : "verb",
"v-pppefg-" : "verb",
"v-pppefn-" : "verb",
"v-pppefv-" : "verb",
"v-pppema-" : "verb",
"v-pppemd-" : "verb",
"v-pppemg-" : "verb",
"v-pppemn-" : "verb",
"v-pppemv-" : "verb",
"v-pppena-" : "verb",
"v-pppend-" : "verb",
"v-pppeng-" : "verb",
"v-pppenn-" : "verb",
"v-ppppma-" : "verb",
"v-ppppmd-" : "verb",
"v-ppppmn-" : "verb",
"v-prp-mn-" : "verb",
"v-prpafa-" : "verb",
"v-prpafd-" : "verb",
"v-prpafn-" : "verb",
"v-prpama-" : "verb",
"v-prpamd-" : "verb",
"v-prpamg-" : "verb",
"v-prpamn-" : "verb",
"v-prpana-" : "verb",
"v-prpang-" : "verb",
"v-prpefa-" : "verb",
"v-prpefd-" : "verb",
"v-prpefg-" : "verb",
"v-prpefn-" : "verb",
"v-prpema-" : "verb",
"v-prpemd-" : "verb",
"v-prpemg-" : "verb",
"v-prpemn-" : "verb",
"v-prpena-" : "verb",
"v-prpend-" : "verb",
"v-prpeng-" : "verb",
"v-prpenn-" : "verb",
"v-prppfn-" : "verb",
"v-prppmn-" : "verb",
"v-sagamn-" : "verb",
"v-saiamn-" : "verb",
"v-samp---" : "verb",
"v-sap-mg-" : "verb",
"v-sap-mn-" : "verb",
"v-sapafa-" : "verb",
"v-sapafd-" : "verb",
"v-sapafg-" : "verb",
"v-sapafn-" : "verb",
"v-sapama-" : "verb",
"v-sapamd-" : "verb",
"v-sapamg-" : "verb",
"v-sapamn-" : "verb",
"v-sapamv-" : "verb",
"v-sapana-" : "verb",
"v-sapang-" : "verb",
"v-sapann-" : "verb",
"v-sapanv-" : "verb",
"v-sapema-" : "verb",
"v-sapemn-" : "verb",
"v-sapmfa-" : "verb",
"v-sapmfd-" : "verb",
"v-sapmfg-" : "verb",
"v-sapmfn-" : "verb",
"v-sapmma-" : "verb",
"v-sapmmd-" : "verb",
"v-sapmmg-" : "verb",
"v-sapmmn-" : "verb",
"v-sapmna-" : "verb",
"v-sapmng-" : "verb",
"v-sapmnn-" : "verb",
"v-sappfa-" : "verb",
"v-sappfd-" : "verb",
"v-sappfg-" : "verb",
"v-sappfn-" : "verb",
"v-sappma-" : "verb",
"v-sappmd-" : "verb",
"v-sappmg-" : "verb",
"v-sappmn-" : "verb",
"v-sappna-" : "verb",
"v-sappng-" : "verb",
"v-sappnn-" : "verb",
"v-sappnv-" : "verb",
"v-sfpafa-" : "verb",
"v-sfpafd-" : "verb",
"v-sfpafn-" : "verb",
"v-sfpama-" : "verb",
"v-sfpamd-" : "verb",
"v-sfpamg-" : "verb",
"v-sfpamn-" : "verb",
"v-sfpmfa-" : "verb",
"v-sfpmfd-" : "verb",
"v-sfpmfg-" : "verb",
"v-sfpmfn-" : "verb",
"v-sfpmma-" : "verb",
"v-sfpmmg-" : "verb",
"v-sfpmmn-" : "verb",
"v-sfpmna-" : "verb",
"v-sfppma-" : "verb",
"v-spiamn-" : "verb",
"v-spp-mn-" : "verb",
"v-spp-nn-" : "verb",
"v-sppa---" : "verb",
"v-sppafa-" : "verb",
"v-sppafd-" : "verb",
"v-sppafg-" : "verb",
"v-sppafn-" : "verb",
"v-sppafv-" : "verb",
"v-sppama-" : "verb",
"v-sppamd-" : "verb",
"v-sppamg-" : "verb",
"v-sppamn-" : "verb",
"v-sppamv-" : "verb",
"v-sppana-" : "verb",
"v-sppand-" : "verb",
"v-sppang-" : "verb",
"v-sppann-" : "verb",
"v-sppanv-" : "verb",
"v-sppefa-" : "verb",
"v-sppefd-" : "verb",
"v-sppefg-" : "verb",
"v-sppefn-" : "verb",
"v-sppema-" : "verb",
"v-sppemd-" : "verb",
"v-sppemg-" : "verb",
"v-sppemn-" : "verb",
"v-sppemv-" : "verb",
"v-sppena-" : "verb",
"v-sppend-" : "verb",
"v-sppeng-" : "verb",
"v-sppenn-" : "verb",
"v-spppfa-" : "verb",
"v-spppfd-" : "verb",
"v-spppfg-" : "verb",
"v-spppfn-" : "verb",
"v-spppma-" : "verb",
"v-spppmn-" : "verb",
"v-srp-mn-" : "verb",
"v-srpafa-" : "verb",
"v-srpafd-" : "verb",
"v-srpafg-" : "verb",
"v-srpafn-" : "verb",
"v-srpama-" : "verb",
"v-srpamd-" : "verb",
"v-srpamg-" : "verb",
"v-srpamn-" : "verb",
"v-srpamv-" : "verb",
"v-srpana-" : "verb",
"v-srpand-" : "verb",
"v-srpang-" : "verb",
"v-srpann-" : "verb",
"v-srpefa-" : "verb",
"v-srpefd-" : "verb",
"v-srpefg-" : "verb",
"v-srpefn-" : "verb",
"v-srpema-" : "verb",
"v-srpemd-" : "verb",
"v-srpemg-" : "verb",
"v-srpemn-" : "verb",
"v-srpemv-" : "verb",
"v-srpena-" : "verb",
"v-srpend-" : "verb",
"v-srpeng-" : "verb",
"v-srpenn-" : "verb",
"v-srppfn-" : "verb",
"v-srppma-" : "verb",
"v-srppmn-" : "verb",
"v-srppmv-" : "verb",
"v1paia---" : "verb",
"v1paim---" : "verb",
"v1paip---" : "verb",
"v1paoa---" : "verb",
"v1paom---" : "verb",
"v1paop---" : "verb",
"v1pasa---" : "verb",
"v1pase---" : "verb",
"v1pasm---" : "verb",
"v1pasp---" : "verb",
"v1pfia---" : "verb",
"v1pfim---" : "verb",
"v1pfom---" : "verb",
"v1piia---" : "verb",
"v1piie---" : "verb",
"v1plia---" : "verb",
"v1plie---" : "verb",
"v1ppia---" : "verb",
"v1ppie---" : "verb",
"v1ppip---" : "verb",
"v1ppoa---" : "verb",
"v1ppoe---" : "verb",
"v1ppsa---" : "verb",
"v1ppse---" : "verb",
"v1pria---" : "verb",
"v1prie---" : "verb",
"v1prsa---" : "verb",
"v1prse---" : "verb",
"v1ptie---" : "verb",
"v1s-sa---" : "verb",
"v1sa-a---" : "verb",
"v1saia---" : "verb",
"v1saie---" : "verb",
"v1saim---" : "verb",
"v1saip---" : "verb",
"v1sao----" : "verb",
"v1saoa---" : "verb",
"v1saoe---" : "verb",
"v1saom---" : "verb",
"v1saop---" : "verb",
"v1sasa---" : "verb",
"v1sase---" : "verb",
"v1sasm---" : "verb",
"v1sasp---" : "verb",
"v1sfi----" : "verb",
"v1sfia---" : "verb",
"v1sfie---" : "verb",
"v1sfim---" : "verb",
"v1sfip---" : "verb",
"v1siia---" : "verb",
"v1siie---" : "verb",
"v1slia---" : "verb",
"v1slie---" : "verb",
"v1slim---" : "verb",
"v1spia---" : "verb",
"v1spie---" : "verb",
"v1spoa---" : "verb",
"v1spoe---" : "verb",
"v1spsa---" : "verb",
"v1spse---" : "verb",
"v1sria---" : "verb",
"v1srie---" : "verb",
"v1sroa---" : "verb",
"v1sroe---" : "verb",
"v1srsa---" : "verb",
"v1stie---" : "verb",
"v1stim---" : "verb",
"v2daia---" : "verb",
"v2dama---" : "verb",
"v2dasa---" : "verb",
"v2dase---" : "verb",
"v2dfia---" : "verb",
"v2dfim---" : "verb",
"v2diia---" : "verb",
"v2diie---" : "verb",
"v2dpia---" : "verb",
"v2dpma---" : "verb",
"v2dpme---" : "verb",
"v2dria---" : "verb",
"v2drma---" : "verb",
"v2paia---" : "verb",
"v2paim---" : "verb",
"v2paip---" : "verb",
"v2pama---" : "verb",
"v2pame---" : "verb",
"v2pamm---" : "verb",
"v2paoa---" : "verb",
"v2paom---" : "verb",
"v2paop---" : "verb",
"v2pasa---" : "verb",
"v2pase---" : "verb",
"v2pasm---" : "verb",
"v2pasp---" : "verb",
"v2pfia---" : "verb",
"v2pfim---" : "verb",
"v2piia---" : "verb",
"v2piie---" : "verb",
"v2ppia---" : "verb",
"v2ppie---" : "verb",
"v2ppma---" : "verb",
"v2ppme---" : "verb",
"v2ppoa---" : "verb",
"v2ppoe---" : "verb",
"v2ppsa---" : "verb",
"v2pria---" : "verb",
"v2prie---" : "verb",
"v2prma---" : "verb",
"v2prmp---" : "verb",
"v2proa---" : "verb",
"v2prsa---" : "verb",
"v2saia---" : "verb",
"v2saie---" : "verb",
"v2saim---" : "verb",
"v2saip---" : "verb",
"v2sam----" : "verb",
"v2sama---" : "verb",
"v2same---" : "verb",
"v2samm---" : "verb",
"v2samp---" : "verb",
"v2saoa---" : "verb",
"v2saoe---" : "verb",
"v2saom---" : "verb",
"v2saop---" : "verb",
"v2sasa---" : "verb",
"v2sase---" : "verb",
"v2sasm---" : "verb",
"v2sasp---" : "verb",
"v2sfi----" : "verb",
"v2sfia---" : "verb",
"v2sfie---" : "verb",
"v2sfim---" : "verb",
"v2sfip---" : "verb",
"v2siia---" : "verb",
"v2siie---" : "verb",
"v2siip---" : "verb",
"v2slia---" : "verb",
"v2slie---" : "verb",
"v2slim---" : "verb",
"v2spia---" : "verb",
"v2spie---" : "verb",
"v2spma---" : "verb",
"v2spme---" : "verb",
"v2spoa---" : "verb",
"v2spoe---" : "verb",
"v2spsa---" : "verb",
"v2spse---" : "verb",
"v2sria---" : "verb",
"v2srie---" : "verb",
"v2srma---" : "verb",
"v2srme---" : "verb",
"v2sroa---" : "verb",
"v2srsa---" : "verb",
"v2stie---" : "verb",
"v3-roe---" : "verb",
"v3daia---" : "verb",
"v3daim---" : "verb",
"v3daip---" : "verb",
"v3daoa---" : "verb",
"v3dfia---" : "verb",
"v3dfim---" : "verb",
"v3diia---" : "verb",
"v3diie---" : "verb",
"v3dlia---" : "verb",
"v3dlie---" : "verb",
"v3dlim---" : "verb",
"v3dpia---" : "verb",
"v3dpie---" : "verb",
"v3dpma---" : "verb",
"v3dpme---" : "verb",
"v3dpsa---" : "verb",
"v3dria---" : "verb",
"v3pai----" : "verb",
"v3paia---" : "verb",
"v3paie---" : "verb",
"v3paim---" : "verb",
"v3paip---" : "verb",
"v3pamm---" : "verb",
"v3paoa---" : "verb",
"v3paoe---" : "verb",
"v3paom---" : "verb",
"v3paop---" : "verb",
"v3pasa---" : "verb",
"v3pase---" : "verb",
"v3pasm---" : "verb",
"v3pasp---" : "verb",
"v3pfia---" : "verb",
"v3pfie---" : "verb",
"v3pfim---" : "verb",
"v3piia---" : "verb",
"v3piie---" : "verb",
"v3piip---" : "verb",
"v3plia---" : "verb",
"v3plie---" : "verb",
"v3plim---" : "verb",
"v3plip---" : "verb",
"v3ppia---" : "verb",
"v3ppie---" : "verb",
"v3ppip---" : "verb",
"v3ppma---" : "verb",
"v3ppme---" : "verb",
"v3ppoa---" : "verb",
"v3ppoe---" : "verb",
"v3ppsa---" : "verb",
"v3ppse---" : "verb",
"v3pria---" : "verb",
"v3prie---" : "verb",
"v3prip---" : "verb",
"v3sai----" : "verb",
"v3saia---" : "verb",
"v3saie---" : "verb",
"v3saim---" : "verb",
"v3saip---" : "verb",
"v3sama---" : "verb",
"v3samm---" : "verb",
"v3samp---" : "verb",
"v3sana---" : "verb",
"v3sao----" : "verb",
"v3saoa---" : "verb",
"v3saoe---" : "verb",
"v3saom---" : "verb",
"v3saop---" : "verb",
"v3sas----" : "verb",
"v3sasa---" : "verb",
"v3sase---" : "verb",
"v3sasm---" : "verb",
"v3sasp---" : "verb",
"v3sfi----" : "verb",
"v3sfia---" : "verb",
"v3sfie---" : "verb",
"v3sfim---" : "verb",
"v3sfip---" : "verb",
"v3sfoa---" : "verb",
"v3sii----" : "verb",
"v3siia---" : "verb",
"v3siie---" : "verb",
"v3siip---" : "verb",
"v3sli----" : "verb",
"v3slia---" : "verb",
"v3slie---" : "verb",
"v3slim---" : "verb",
"v3slip---" : "verb",
"v3spia---" : "verb",
"v3spie---" : "verb",
"v3spip---" : "verb",
"v3spma---" : "verb",
"v3spme---" : "verb",
"v3spoa---" : "verb",
"v3spoe---" : "verb",
"v3spop---" : "verb",
"v3spsa---" : "verb",
"v3spse---" : "verb",
"v3sria---" : "verb",
"v3srie---" : "verb",
"v3srip---" : "verb",
"v3srma---" : "verb",
"v3sroa---" : "verb",
"v3srsa---" : "verb",
"v3stie---" : "verb",
"v3stim---" : "verb",
"v3stip---" : "verb",
"x--------" : "x",
"x-p----d-" : "x",
"x-p---nn-" : "x",
}


def countFrequency(lemma):
    i = 0
    for elem in items:
        if elem.hasAttribute('lemma'):
            if elem.attributes['lemma'].value == lemma:
                i += 1
    return i


def getLemmas(word, pos=None):
    lemmas = []
    if pos is not None:
        for elem in items:
            if elem.hasAttribute('form'):
                if elem.attributes['form'].value == word and elem.attributes['part-of-speech'].value==pos and elem.attributes['lemma'].value not in lemmas:
                    lemmas.append(elem.attributes['lemma'].value)
    
    lemmas_freq = []           
    for lemm in lemmas:
        freq = countFrequency(lemm)
        lemmas_freq.append((lemm, freq))
        
    lemmas_freq = sorted(lemmas_freq, key = lambda x: x[1], reverse=True)
        
    return lemmas
    
    
def buildict(items):
   corpus = dict() # creates the dictionary for the corpus

   for elem in items:
        if elem.hasAttribute('form') and elem.hasAttribute('lemma') and elem.hasAttribute('part-of-speech'):
            if elem.attributes['form'].value in corpus:
                previous_items = corpus[elem.attributes['form'].value]
                #lemmas = getLemmas(elem.attributes['form'].value, elem.attributes['part-of-speech'].value)
                #(lemma, freq) = lemmas[0]
                univpos = univ_pos_name_variants[elem.attributes['part-of-speech'].value]
                new_form = extend(previous_items, { univpos : lemmas[0] }) 
                corpus.update({ elem.attributes['form'].value : new_form } )
            else:     
                lemmas = getLemmas(elem.attributes['form'].value, elem.attributes['part-of-speech'].value)
                #(lemma, freq) = lemmas[0]
                univpos = univ_pos_name_variants[elem.attributes['part-of-speech'].value]
                corpus.update({ elem.attributes['form'].value : { univpos: lemmas[0] }  })
            #print({ elem.attributes['form'].value : lemma}, freq)           
   return corpus  
   

def buildindex(items):

    index = dict()
    for pos in ["A-", "Df", "S-", "Ma", "Nb", "C-", "Pd", "F-", "Px", "N-", "I-", "Du", "Pi", "Mo", "Pp", "Pk", "Ps", "Pt", "R-", "Ne", "Py", "Pc", "Dq", "Pr", "G-", "V-", "X-"]: 
        lemmas = []
        for elem in items:
            if elem.hasAttribute('lemma') and elem.hasAttribute('part-of-speech') and elem.attributes['part-of-speech'].value==pos and elem.attributes['lemma'].value not in lemmas:
                lemmas.append(elem.attributes['lemma'].value)
                
        if pos in index:
            first_lemmas = index[pos]
            index.update({ pos : fist_lemmas+lemmas })
        else: 
            index.update({ pos : lemmas })
            
    # transforming into universal pos
    finalindex = dict()
    for pos, lemmas in index.items():       
        if univ_pos_name_variants[pos] in finalindex:
            previous_lemmas = finalindex[univ_pos_name_variants[pos]]
            finalindex.update({ univ_pos_name_variants[pos] : previous_lemmas+lemmas })
        else:
            finalindex.update({ univ_pos_name_variants[pos] : lemmas })
                
    return finalindex


def buildictdouble(items):
   corpus = dict() # creates the dictionary for the corpus

   i = 0
   for elem in items:
        if elem.hasAttribute('form') and elem.hasAttribute('lemma') and elem.hasAttribute('part-of-speech'):
            univpos = univ_pos_name_variants[elem.attributes['part-of-speech'].value]
            #univpos = elem.attributes['part-of-speech'].value
            if elem.attributes['form'].value in corpus and univpos in corpus[elem.attributes['form'].value]:
                if not elem.attributes['lemma'].value == corpus[elem.attributes['form'].value][univpos]:
                    i+=1
                    print(i, "Alert!. Replacing previous assignment of ", elem.attributes['form'].value, univpos, corpus[elem.attributes['form'].value][univpos], " with ", elem.attributes['lemma'].value) 
                new_form =  { univpos : elem.attributes['lemma'].value } 
                corpus.update({ elem.attributes['form'].value : new_form } )
            else:     
                corpus.update({ elem.attributes['form'].value : { univpos: elem.attributes['lemma'].value }  })
                
            #print(elem.attributes['form'].value, elem.attributes['part-of-speech'].value, univpos,  elem.attributes['lemma'].value)        
               
   corpus = collections.OrderedDict(sorted(corpus.items()))            
               
   return corpus 
   
def countFrequencyMorpheus(lemma):
    i = 0
    for elem in items:
        lemmaIn = elem.getElementsByTagName("l")[0].firstChild.nodeValue
        if lemmaIn == lemma:
            i += 1
    return i   
   
def getLemmasMorpheus(word, pos=None):
    lemmas = []
    if pos is not None:
        for elem in items:
            univpos = univ_pos_name_variants[elem.getElementsByTagName("p")[0].firstChild.nodeValue]
            #univpos = elem.getElementsByTagName("p")[0].firstChild.nodeValue
            form = elem.getElementsByTagName("f")[0].firstChild.nodeValue
            lemma = elem.getElementsByTagName("l")[0].firstChild.nodeValue
            if form == word and univpos==pos and lemma not in lemmas:
                lemmas.append(lemma)
    
    lemmas_freq = []           
    for lemm in lemmas:
        freq = countFrequencyMorpheus(lemm)
        lemmas_freq.append((lemm, freq))
        
    lemmas_freq = sorted(lemmas_freq, key = lambda x: x[1], reverse=True)
        
    return lemmas  
  
        
def buildictmorpheus_old(items):
    corpus = dict() # creates the dictionary for the corpus

    for elem in items:
        univpos = univ_pos_name_variants[elem.getElementsByTagName("p")[0].firstChild.nodeValue]
        #univpos = elem.getElementsByTagName("p")[0].firstChild.nodeValue
        form = elem.getElementsByTagName("f")[0].firstChild.nodeValue
        lemma = elem.getElementsByTagName("l")[0].firstChild.nodeValue
        if form in corpus:
            previous_items = corpus[form]
            new_form = extend(previous_items, { univpos : lemma }) 
            corpus.update({ form : new_form } )
        else:     
            lemmas = getLemmasMorpheus(form, univpos)
            corpus.update({ form : { univpos: lemmas[0] }  })
            
    return corpus         


def buildindexmorpheus(items):

    index = dict()
    for pos in univ_pos_name_variants.keys(): 
        lemmas = []
        for elem in items:
            thispos = elem.getElementsByTagName("p")[0].firstChild.nodeValue
            form = elem.getElementsByTagName("f")[0].firstChild.nodeValue
            lemma = elem.getElementsByTagName("l")[0].firstChild.nodeValue
            if thispos==pos and lemma not in lemmas:
                lemmas.append(lemma)
                
        if pos in index:
            first_lemmas = index[pos]
            index.update({ pos : fist_lemmas+lemmas })
        else: 
            index.update({ pos : lemmas })
            
    # transforming into universal pos
    finalindex = dict()
    for pos, lemmas in index.items():       
        if univ_pos_name_variants[pos] in finalindex:
            previous_lemmas = finalindex[univ_pos_name_variants[pos]]
            finalindex.update({ univ_pos_name_variants[pos] : previous_lemmas+lemmas })
        else:
            finalindex.update({ univ_pos_name_variants[pos] : lemmas })
                
    return finalindex
 
def whichone(form, univpos, lemma1, lemma2):
    # api-endpoint 
    # http://services.perseids.org/bsp/morphologyservice/analysis/word?lang=grc&engine=morpheusgrc&word=%E1%BC%80%CF%80%CE%BF%CE%BA%CE%B1%CE%BB%CF%8D%CF%88%CE%B5%CE%B9
    URL = "http://services.perseids.org/bsp/morphologyservice/analysis/word"
   
    # location given here 
    location = "delhi technological university"
  
    # defining a params dict for the parameters to be sent to the API 
    PARAMS = {'lang':'grc', 'engine':'morpheusgrc', 'word':form} 
  
    # sending get request and saving the response as response object 
    r = requests.get(URL, PARAMS) 
  
    # extracting data in json format 
    data = r.json() 
    #print("data:", data)
    print("======================================================================== perseids")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    encoding = 'utf-8'
    
    if "Body" in data["RDF"]["Annotation"]: # if the answer is not empty 
    
        answer = data["RDF"]["Annotation"]["Body"]["rest"]["entry"]["infl"]
    
        if 0 in answer: # it gets the first answer if many
            word = data["RDF"]["Annotation"]["Body"]["rest"]["entry"]["infl"][0]["term"]["stem"]["$"]
        else: 
            word = data["RDF"]["Annotation"]["Body"]["rest"]["entry"]["infl"]["term"]["stem"]["$"] 
            
    else:
        word = None # it chooses none. this word will be dismissed
        
    lemma = word # chr(int(word, 16))
    
    if word==lemma1: 
        print("first lemma was right", lemma1)
    elif word==lemma2:
        print("second lemma was right", lemma2)
    else:
        print("None was right. The word ", form, " will be dismissed")
    
    return lemma
      
           
def buildictmorpheus(items):
   corpus = dict() # creates the dictionary for the corpus
   filenames = dict() # creates a dictionary for the filenames and their content

   i = 0
   for elem in items:
       univpos = univ_pos_name_variants[elem.getElementsByTagName("p")[0].firstChild.nodeValue]       
       #univpos = elem.getElementsByTagName("p")[0].firstChild.nodeValue      
       form = elem.getElementsByTagName("f")[0].firstChild.nodeValue       
       lemma = elem.getElementsByTagName("l")[0].firstChild.nodeValue
       
       #print(i, form, univpos, lemma)
       
       if "lemma_lookup_"+univpos in list(filenames.keys()):
           these_lemmas = filenames["lemma_lookup_"+univpos]
       else: 
           these_lemmas = dict()
           filenames.update({"lemma_lookup_"+univpos : these_lemmas})
           
       thelemma = lemma 
       
       if form in corpus and univpos in list(corpus[form].keys()) and not lemma == corpus[form][univpos]:
           print(i, "Alert of collision! word: ", form, " pos: ", univpos, " lemma1: ", corpus[form][univpos], " lemma2: ", lemma)
           thelemma = whichone(form, univpos, corpus[form][univpos], lemma)                     
            
       
       #print("Corpus for :", univpos, " adding ", form, thelemma)  
       corpus.update({ form : { univpos: thelemma }  }) 
       these_lemmas.update({ form : thelemma })    
                 
       #filenames.update({"lemma_lookup_"+univpos : these_lemmas})
       i+=1    
       #print(i, form, univpos, lemma)
       
   for name, content in filenames.items():
       print("created filename: ", name)
   #    for word, lemma in content.items(): 
   #        print("      ", word, lemma)  
          
   return filenames  
   
   
def createfiles(filenamesdict):

    for name, content in filenamesdict.items():

        with open(name+'.json', 'w', encoding='utf-8') as f:
            corpus = collections.OrderedDict(sorted(content.items())) 
            json.dump(corpus, f, ensure_ascii=False, indent=4)
             
           
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handlePoint(point):
    print("<li>%s</li>" % getText(point.childNodes))    
    
    
createfiles(buildictmorpheus(items))    
    
           
# one specific item attribute
#print('Item #2 attribute:')
#print(items[1].attributes['form'].value)

# all item attributes
#print('\nAll attributes:')
#i = 1
#for elem in items:
#   if elem.hasAttribute('form'):
#        #elem.attributes['id'].value,
#        print(i, elem.attributes['form'].value, elem.attributes['lemma'].value)
#        i += 1

#corpus = buildict(items)

#index = buildindex(items)

#corpus = buildictdouble(items)

# convert into JSON:
#y = json.dumps(corpus, indent=4, ensure_ascii=False)


#print(json.dumps(whichone("πολύτροπον", "adj", "πολύτροπος", "b"), indent=4))


# index = buildindexmorpheus(items)

#print('\nStart of corpus:')

#print("Total amount of word:", len(items))

#with open('index.json', 'w', encoding='utf-8') as f:
#    json.dump(index, f, ensure_ascii=False, indent=4)


#i=0
#for elem in items:
#   if elem.hasAttribute('form'):
#        #elem.attributes['id'].value,
#    univpos = univ_pos_name_variants[elem.getElementsByTagName("p")[0].firstChild.nodeValue]
#    print(i, elem.getElementsByTagName("i")[0].firstChild.nodeValue, elem.getElementsByTagName("f")[0].firstChild.nodeValue, univpos, elem.getElementsByTagName("l")[0].firstChild.nodeValue, elem.getElementsByTagName("s")[0].firstChild.nodeValue)
#    i += 1

#corpus = buildictmorpheus(items)

# the result is a JSON string:
#with open('data.json', 'w', encoding='utf-8') as f:
#    json.dump(corpus, f, ensure_ascii=False, indent=4)
#print(y) 


# convert into JSON:
#y = json.dumps(index, indent=4, ensure_ascii=False)

# the result is a JSON string:
#print(y) 


#for elem in corpus:
    #print(elem.value, corpus[elem.value])
    #print(elem, corpus[elem])

print('\nEnd of corpus:')



