% lexicon.pl
% Lexicon module for Glossaire Vaudois
% Stores extracted vocabulary in structured Prolog format
%
% Similar to Coptic lexicon structure but adapted for Swiss French dialect dictionary
% Format: lexeme(Headword, POS, StandardFrench, Definition, Features)

:- module(glossary_lexicon, [
    add_lexeme/1,
    lexeme/5,
    lookup_headword/2,
    lookup_by_pos/2,
    save_lexicon/1,
    load_lexicon/1,
    lexicon_statistics/1
]).

:- dynamic lexeme/5.

%% Lexeme structure
% lexeme(Headword, POS, StandardFrench, Definition, Features)
%
% Examples:
% lexeme('PANOSSE', pos(noun, feminine), 'serpillière', 'Pour laver le sol', [source('Glossaire 1861')]).
% lexeme('LINGE', pos(noun, masculine), 'serviette', 'Serviette de toilette', [source('Glossaire 1861')]).

%% Add a lexeme from parsed entry
add_lexeme(entry(Headword, POS, Definition, Metadata)) :-
    extract_standard_french_from_metadata(Metadata, StandardFrench),
    extract_features(Metadata, Features),
    normalize_headword(Headword, NormalizedHead),
    assertz(lexeme(NormalizedHead, POS, StandardFrench, Definition, Features)).

%% Lookup predicates
lookup_headword(Headword, Lexemes) :-
    normalize_headword(Headword, NormalizedHead),
    findall(lexeme(NormalizedHead, POS, SF, Def, Feats),
            lexeme(NormalizedHead, POS, SF, Def, Feats),
            Lexemes).

lookup_by_pos(POSPattern, Lexemes) :-
    findall(lexeme(Head, POS, SF, Def, Feats),
            (lexeme(Head, POS, SF, Def, Feats),
             match_pos(POS, POSPattern)),
            Lexemes).

match_pos(pos(Type, _), Type) :- !.
match_pos(POS, POS).

%% Extract standard French from metadata
extract_standard_french_from_metadata(metadata(_, _, Notations), StandardFrench) :-
    member(notation(d, StandardFrench), Notations),
    !.
extract_standard_french_from_metadata(_, '').

%% Extract features from metadata
extract_features(metadata(Variants, Pron, Notations), Features) :-
    Features = [
        variants(Variants),
        pronunciation(Pron),
        notations(Notations),
        source('Glossaire Vaudois 1861')
    ].

%% Normalize headword (lowercase, remove parentheses)
normalize_headword(Headword, Normalized) :-
    atom_string(Headword, HeadStr),
    downcase_atom(Headword, Lower),
    % Remove parentheses and content
    re_replace('\\([^)]*\\)'/g, '', Lower, Temp),
    % Trim whitespace
    normalize_space(atom(Normalized), Temp).

%% Persistence: save/load lexicon
save_lexicon(Filename) :-
    open(Filename, write, Stream),
    forall(
        lexeme(Head, POS, SF, Def, Feats),
        (   writeq(Stream, lexeme(Head, POS, SF, Def, Feats)),
            write(Stream, '.\n')
        )
    ),
    close(Stream).

load_lexicon(Filename) :-
    retractall(lexeme(_, _, _, _, _)),
    consult(Filename).

%% Statistics
lexicon_statistics(Stats) :-
    findall(H, lexeme(H, _, _, _, _), AllHeadwords),
    length(AllHeadwords, Total),
    findall(H, lexeme(H, pos(noun, masculine), _, _, _), MascNouns),
    length(MascNouns, MascCount),
    findall(H, lexeme(H, pos(noun, feminine), _, _, _), FemNouns),
    length(FemNouns, FemCount),
    findall(H, lexeme(H, pos(verb, _), _, _, _), Verbs),
    length(Verbs, VerbCount),
    findall(H, lexeme(H, pos(adjective, _), _, _, _), Adjs),
    length(Adjs, AdjCount),
    Stats = statistics{
        total: Total,
        nouns_masculine: MascCount,
        nouns_feminine: FemCount,
        verbs: VerbCount,
        adjectives: AdjCount
    }.

%% Export to CSV format
export_to_csv(Filename) :-
    open(Filename, write, Stream),
    write(Stream, 'swiss_french,standard_french,dialect,part_of_speech,definition,source,features\n'),
    forall(
        lexeme(Head, POS, SF, Def, Feats),
        (   format_pos(POS, POSStr),
            format(Stream, '~w,~w,vaud,~w,~w,Glossaire Vaudois (1861),~w~n',
                   [Head, SF, POSStr, Def, Feats])
        )
    ),
    close(Stream).

format_pos(pos(Type, Gender), Formatted) :-
    format(atom(Formatted), '~w (~w)', [Type, Gender]).
format_pos(unknown, 'unknown').

%% Prolog-Python interface helpers (for Janus)
% These predicates are designed to be called from Python via Janus

%% Convert lexeme to Python-friendly dict
lexeme_to_dict(lexeme(Head, POS, SF, Def, Feats), Dict) :-
    format_pos(POS, POSStr),
    Dict = _{
        headword: Head,
        pos: POSStr,
        standard_french: SF,
        definition: Def,
        features: Feats
    }.

%% Get all lexemes as Python list of dicts
get_all_lexemes_as_dicts(Dicts) :-
    findall(Dict,
            (lexeme(H, P, S, D, F),
             lexeme_to_dict(lexeme(H, P, S, D, F), Dict)),
            Dicts).

%% Search lexeme by headword (for Python)
search_by_headword(Headword, Dicts) :-
    lookup_headword(Headword, Lexemes),
    maplist(lexeme_to_dict, Lexemes, Dicts).

%% Bulk add from Python list of entries
bulk_add_entries([]).
bulk_add_entries([Entry|Rest]) :-
    add_lexeme(Entry),
    bulk_add_entries(Rest).
