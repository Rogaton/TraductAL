% grammar.pl
% DCG grammar for parsing 1861 Glossaire Vaudois entries
% Compatible with SWI-Prolog / Janus-Prolog interface
%
% Author: Adapted for Swiss French Vaudois glossary extraction
% Format: Historical dictionary entries (1861) with:
%   - HEADWORD, part_of_speech. Definition
%   - Multi-line entries
%   - Special notations: N.P. (nous disons pas), D. (on dit), P.F. (pas français)

:- module(glossary_grammar, [
    parse_entry/2,
    parse_entry_from_string/2,
    parse_glossary_file/2
]).

:- use_module(library(dcg/basics)).
:- use_module(lexicon).

%% Main entry point: parse a single glossary entry
% parse_entry(+Text, -ParsedEntry)
parse_entry(Text, Entry) :-
    atom_codes(Text, Codes),
    phrase(entry(Entry), Codes).

parse_entry_from_string(String, Entry) :-
    string_codes(String, Codes),
    phrase(entry(Entry), Codes).

%% DCG Rules for Glossary Entries

% Main entry structure
entry(entry(Headword, POS, Definition, Metadata)) -->
    headword(Headword),
    optional_whitespace,
    optional_variant_forms(Variants),
    optional_whitespace,
    part_of_speech(POS),
    optional_whitespace,
    optional_pronunciation(Pron),
    optional_whitespace,
    definition_text(DefText),
    optional_whitespace,
    optional_notations(Notations),
    { Definition = DefText,
      Metadata = metadata(Variants, Pron, Notations) }.

% Alternative: entry without POS marker
entry(entry(Headword, unknown, Definition, Metadata)) -->
    headword(Headword),
    optional_whitespace,
    [ 0'. ],  % period
    optional_whitespace,
    definition_text(DefText),
    optional_notations(Notations),
    { Definition = DefText,
      Metadata = metadata([], none, Notations) }.

%% Headword: uppercase word, possibly with parentheses
% ABANDONNER (S')
% ABATIS ou ABBATIS
headword(Word) -->
    uppercase_word(W1),
    headword_suffix(Suffix),
    { atom_concat(W1, Suffix, Word) }.

headword_suffix(Suffix) -->
    whitespace,
    "(", uppercase_word(Inner), ")",
    { atom_concat(' (', Inner, Temp),
      atom_concat(Temp, ')', Suffix) }.
headword_suffix(Suffix) -->
    whitespace,
    "ou",
    whitespace,
    uppercase_word(Variant),
    { atom_concat(' ou ', Variant, Suffix) }.
headword_suffix('') --> [].

uppercase_word(Word) -->
    uppercase_letter(First),
    uppercase_word_rest(Rest),
    { atom_codes(Word, [First|Rest]) }.

uppercase_word_rest([C|Rest]) -->
    uppercase_or_hyphen(C),
    uppercase_word_rest(Rest).
uppercase_word_rest([]) --> [].

uppercase_letter(C) --> [C], { C >= 65, C =< 90 }.  % A-Z
uppercase_or_hyphen(C) --> [C], { (C >= 65, C =< 90) ; (C >= 97, C =< 122) ; C = 45 }.  % A-Z, a-z, hyphen

%% Optional variant forms
optional_variant_forms([Variant|Rest]) -->
    whitespace,
    "ou",
    whitespace,
    uppercase_word(Variant),
    optional_variant_forms(Rest).
optional_variant_forms([]) --> [].

%% Part of speech markers
% s.m. (substantif masculin)
% s.f. (substantif féminin)
% v.a. (verbe actif)
% v.pr. (verbe pronominal)
% adj. (adjectif)
% adv. (adverbe)

part_of_speech(pos(Type, Gender)) -->
    ",",
    optional_whitespace,
    "s.", gender_marker(Gender), ".",
    { Type = noun }.

part_of_speech(pos(verb, Form)) -->
    ",",
    optional_whitespace,
    "v.", verb_form(Form), ".",
    !.

part_of_speech(pos(adjective, _)) -->
    ",",
    optional_whitespace,
    "adj.".

part_of_speech(pos(adverb, _)) -->
    ",",
    optional_whitespace,
    "adv.".

gender_marker(masculine) --> "m".
gender_marker(feminine) --> "f".
gender_marker(neuter) --> "n".

verb_form(active) --> "a".
verb_form(neutral) --> "n".
verb_form(pronominal) --> "pr".
verb_form(reflexive) --> "réfl".

%% Optional pronunciation
% (Pr. abati.)
% (Pr. a-bé-ï.)
optional_pronunciation(pron(Text)) -->
    "(", optional_whitespace,
    "Pr.", optional_whitespace,
    pronunciation_text(Text),
    optional_whitespace,
    ")",
    !.
optional_pronunciation(none) --> [].

pronunciation_text(Text) -->
    pronunciation_chars(Codes),
    { atom_codes(Text, Codes) }.

pronunciation_chars([C|Rest]) -->
    [C],
    { C \= 41 },  % not ')'
    pronunciation_chars(Rest).
pronunciation_chars([]) --> [].

%% Definition text
% Main definition body, may include:
% - Standard French equivalent
% - Usage examples
% - Notes

definition_text(Text) -->
    definition_chars(Codes),
    { atom_codes(Text, Codes) }.

definition_chars([C|Rest]) -->
    [C],
    { \+ member(C, [78, 68, 80]) },  % Not start of N.P., D., P.F.
    definition_chars(Rest).
definition_chars([]) --> [].

%% Optional notations (N.P., D., P.F.)
% N.P. = nous (ne) disons pas (incorrect usage)
% D. = on dit (correct form)
% P.F. = pas français (not French)

optional_notations(Notations) -->
    notation_list(Notations).
optional_notations([]) --> [].

notation_list([N|Rest]) -->
    notation(N),
    optional_whitespace,
    notation_list(Rest).
notation_list([]) --> [].

notation(notation(np, Text)) -->
    "N.P.",
    optional_whitespace,
    notation_text(Text),
    !.

notation(notation(d, Text)) -->
    "D.",
    optional_whitespace,
    notation_text(Text),
    !.

notation(notation(pf, Text)) -->
    "P.F.",
    optional_whitespace,
    notation_text(Text),
    !.

notation_text(Text) -->
    notation_chars(Codes),
    { atom_codes(Text, Codes) }.

notation_chars([C|Rest]) -->
    [C],
    { C \= 78, C \= 68, C \= 80 },  % Not start of another notation
    notation_chars(Rest).
notation_chars([]) --> [].

%% Whitespace handling
optional_whitespace --> whitespace.
optional_whitespace --> [].

whitespace --> [C], { code_type(C, space) }, whitespace.
whitespace --> [C], { code_type(C, space) }.

%% Parse entire glossary file
parse_glossary_file(InputFile, Entries) :-
    read_file_to_string(InputFile, Content, []),
    split_string(Content, "\n", "", Lines),
    parse_lines(Lines, [], Entries).

parse_lines([], Acc, Entries) :-
    reverse(Acc, Entries).

parse_lines([Line|Rest], Acc, Entries) :-
    (   parse_entry_from_string(Line, Entry)
    ->  parse_lines(Rest, [Entry|Acc], Entries)
    ;   parse_lines(Rest, Acc, Entries)  % Skip unparseable lines
    ).

%% Helper predicates
extract_standard_french(Entry, StandardFrench) :-
    Entry = entry(_, _, Definition, Metadata),
    Metadata = metadata(_, _, Notations),
    member(notation(d, StandardFrench), Notations),
    !.
extract_standard_french(Entry, Definition) :-
    Entry = entry(_, _, Definition, _).
