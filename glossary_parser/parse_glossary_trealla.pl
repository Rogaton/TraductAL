#!/usr/bin/env tpl
% parse_glossary_trealla.pl
% Standalone Trealla Prolog script to parse Glossaire Vaudois
% Compatible with Trealla Prolog syntax
%
% Usage: tpl parse_glossary_trealla.pl input.txt output.csv

:- initialization(main).

% Simplified DCG grammar for 1861 glossary format
% Focuses on extracting: HEADWORD, part_of_speech. Definition

%% Main entry patterns
parse_line(Line, entry(Headword, POS, Definition)) :-
    atom_string(Line, Str),
    string_codes(Str, Codes),
    phrase(entry(Headword, POS, Definition), Codes),
    !.
parse_line(_, none).

%% DCG Rules

% Pattern 1: WORD, s.m./s.f./v.a. etc. Definition
entry(Headword, POS, Definition) -->
    uppercase_word(HW),
    optional_spaces,
    ",",
    optional_spaces,
    pos_marker(POS),
    optional_spaces,
    definition_text(Def),
    { atom_string(Headword, HW),
      atom_string(Definition, Def) }.

% Pattern 2: WORD. Definition (no POS)
entry(Headword, unknown, Definition) -->
    uppercase_word(HW),
    optional_spaces,
    ".",
    optional_spaces,
    definition_text(Def),
    { atom_string(Headword, HW),
      atom_string(Definition, Def) }.

%% Uppercase word (headword)
uppercase_word(Word) -->
    uppercase_letter(C),
    word_chars(Cs),
    { string_codes(Word, [C|Cs]) }.

uppercase_letter(C) -->
    [C],
    { char_type(C, upper) }.

word_chars([C|Cs]) -->
    word_char(C),
    word_chars(Cs).
word_chars([]) --> [].

word_char(C) -->
    [C],
    { (char_type(C, alpha) ; C = 45 ; C = 32 ; C = 40 ; C = 41) }.
    % letters, hyphen, space, parentheses

%% POS markers
pos_marker('noun_masculine') -->
    "s", optional_spaces, ".", optional_spaces, "m", optional_spaces, ".".
pos_marker('noun_feminine') -->
    "s", optional_spaces, ".", optional_spaces, "f", optional_spaces, ".".
pos_marker('noun_neuter') -->
    "s", optional_spaces, ".", optional_spaces, "n", optional_spaces, ".".
pos_marker('verb_active') -->
    "v", optional_spaces, ".", optional_spaces, "a", optional_spaces, ".".
pos_marker('verb_pronominal') -->
    "v", optional_spaces, ".", optional_spaces, "pr", optional_spaces, ".".
pos_marker('verb_neutral') -->
    "v", optional_spaces, ".", optional_spaces, "n", optional_spaces, ".".
pos_marker('verb') -->
    "v", optional_spaces, ".".
pos_marker('adjective') -->
    "adj", optional_spaces, ".".
pos_marker('adverb') -->
    "adv", optional_spaces, ".".

%% Definition text (everything until end)
definition_text(Def) -->
    def_chars(Codes),
    { string_codes(Def, Codes) }.

def_chars([C|Cs]) -->
    [C],
    { \+ end_of_def(C) },
    def_chars(Cs).
def_chars([]) --> [].

end_of_def(10).  % newline
end_of_def(13).  % carriage return

%% Whitespace
optional_spaces --> [C], { char_type(C, space) }, optional_spaces.
optional_spaces --> [].

%% Main parsing and export

main :-
    current_prolog_flag(argv, Args),
    catch(
        (parse_args(Args, InputFile, OutputFile),
         process_file(InputFile, OutputFile)),
        Error,
        (format(user_error, 'Error: ~w~n', [Error]), halt(1))
    ),
    halt(0).

parse_args([Input, Output|_], Input, Output) :- !.
parse_args(_, _, _) :-
    format(user_error, 'Usage: tpl parse_glossary_trealla.pl input.txt output.csv~n', []),
    halt(1).

process_file(InputFile, OutputFile) :-
    format('📖 Parsing glossary with Trealla: ~w~n', [InputFile]),

    % Read input
    read_file_to_string(InputFile, Content, []),
    split_string(Content, "\n", "", Lines),
    length(Lines, TotalLines),
    format('   Total lines: ~w~n', [TotalLines]),

    % Parse entries
    parse_lines(Lines, 1, TotalLines, Entries),
    length(Entries, EntryCount),
    format('   ✅ Parsed ~w entries~n', [EntryCount]),

    % Export to CSV
    export_csv(OutputFile, Entries),
    format('   💾 Saved to: ~w~n', [OutputFile]),
    format('~n✅ Trealla parsing complete!~n', []).

parse_lines([], _, _, []).
parse_lines([Line|Rest], N, Total, Entries) :-
    (   N mod 500 =:= 0
    ->  format('   Processing line ~w/~w...~n', [N, Total])
    ;   true
    ),

    (   parse_line(Line, entry(HW, POS, Def)),
        HW \= '',
        Def \= ''
    ->  Entries = [entry(HW, POS, Def)|RestEntries]
    ;   Entries = RestEntries
    ),

    N1 is N + 1,
    parse_lines(Rest, N1, Total, RestEntries).

export_csv(OutputFile, Entries) :-
    open(OutputFile, write, Stream, [encoding(utf8)]),

    % Write header
    write(Stream, 'swiss_french,standard_french,dialect,part_of_speech,definition,source,notes\n'),

    % Write entries
    forall(
        member(entry(HW, POS, Def), Entries),
        (   % Extract standard French from definition if possible
            extract_standard_french(Def, StdFr),
            % Clean and escape CSV fields
            escape_csv(HW, HWEsc),
            escape_csv(StdFr, StdFrEsc),
            escape_csv(Def, DefEsc),
            format(Stream, '~w,~w,vaud,~w,~w,Glossaire Vaudois (1861),Trealla DCG parsed~n',
                   [HWEsc, StdFrEsc, POS, DefEsc])
        )
    ),

    close(Stream).

% Extract standard French from definition (heuristics)
extract_standard_french(Def, StdFr) :-
    atom_string(Def, DefStr),
    % Look for "D." marker (on dit = correct form)
    sub_string(DefStr, Before, _, After, "D."),
    After > 0,
    sub_string(DefStr, _, After, 0, Rest),
    string_trim(Rest, StdFr),
    StdFr \= '',
    !.
extract_standard_french(_, '').

% Escape CSV fields
escape_csv(Field, Escaped) :-
    atom_string(Field, FieldStr),
    % If contains comma or quote, wrap in quotes and escape quotes
    (   (sub_string(FieldStr, _, _, _, ",") ; sub_string(FieldStr, _, _, _, "\""))
    ->  % Simple escaping - replace " with ""
        atom_chars(Field, Chars),
        escape_quotes(Chars, EscapedChars),
        atom_chars(EscapedAtom, EscapedChars),
        format(atom(Escaped), '"~w"', [EscapedAtom])
    ;   Escaped = FieldStr
    ).

escape_quotes([], []).
escape_quotes(['"'|Rest], ['"', '"'|EscRest]) :-
    !,
    escape_quotes(Rest, EscRest).
escape_quotes([C|Rest], [C|EscRest]) :-
    escape_quotes(Rest, EscRest).

string_trim(Str, Trimmed) :-
    atom_string(Str, StrAtom),
    atom_chars(StrAtom, Chars),
    trim_spaces(Chars, TrimmedChars),
    atom_chars(TrimmedAtom, TrimmedChars),
    atom_string(TrimmedAtom, Trimmed).

trim_spaces(Chars, Trimmed) :-
    trim_left(Chars, LeftTrimmed),
    reverse(LeftTrimmed, Reversed),
    trim_left(Reversed, RightTrimmed),
    reverse(RightTrimmed, Trimmed).

trim_left([], []).
trim_left([C|Rest], Trimmed) :-
    char_type(C, space),
    !,
    trim_left(Rest, Trimmed).
trim_left(Chars, Chars).
