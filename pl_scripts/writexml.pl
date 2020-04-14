/* writexml.pl

This files writes out, as a list, the content of an xml tagged text, 
preserving word order but removing all tags

probando con ?- load_xml('stoa0033a.tlg028.1st1K-grc1.xml', XML, []), writexml(XML, S), tell('stoa0033a.tlg028.1st1K-grc1.txt'), write_words(S), told. 


*/


writexml([], []).
writexml([element(text, _, Text)|_], Out) :-
	writexml_s(Text, Out).  % just one Text now

writexml_s([], []).
writexml_s([element(sentence,_, Sentence)|RestS], [Sentence|Out]) :-
	writexml_s(RestS, Out).
writexml_s([element(s,_, Sentence)|RestS], [Words|Out]) :-
	writexml_t(Sentence, Words), 
	writexml_s(RestS, Out). 
writexml_s([_|RestS], Out) :-
	writexml_s(RestS, Out).


writexml_t([], []).
writexml_t([element(t,_, Word)|RestW], [Word|Out]) :- 
	writexml_t(RestW, Out).
writexml_t([_|RestW], Out) :- 
	writexml_t(RestW, Out).

write_words([]).
write_words([Word|RestW]):- 
	write_word(Word), write_words(RestW).

write_word([]).
write_word(['\n'|R]) :-
	nl, write_word(R).
write_word([[',']|R]) :-
	write_term(', ', []), write_word(R).
write_word([[.]|R]) :-
	write_term('. ', []), write_word(R).
write_word([[W]|R]) :- write(' '), 
	write_term(W, []), write_word(R). 
write_word([_|R]) :- write(' [..] '), write_word(R).

 





