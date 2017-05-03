from LanguageData import *
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import utils

LANGUAGE_LIMIT = 75
LANGUAGE_PAIR_THRESHOLD = 500


def generate_json_data():
    included_languages = {l[0] for l in timeline.get_language_totals().most_common(LANGUAGE_LIMIT)}

    # language-pairs.json
    edges_over_threshold = Counter()
    for edge, value in language_pairs.items():
        if value >= LANGUAGE_PAIR_THRESHOLD:
            edges_over_threshold[edge] = value

    json_pairs = []
    for pair, count in language_pairs.items():
        if pair[0] not in included_languages or pair[1] not in included_languages:
            continue
        json_pairs.append([pair[0], pair[1], count])
        json.dump(json_pairs, open("language-pairs.json", "w"))

    # months.json
    all_months = []
    current_month = DATE_START
    while current_month <= DATE_END:
        all_months.append(current_month)
        current_month = utils.add_months(current_month, 1)

    json_months = [month.strftime("%b-%Y") for month in all_months]
    json.dump(json_months, open("months.json", "w"))

    # language-timeline.json
    languages = defaultdict(list)
    for language in all_languages:
        for month in all_months:
            try:
                count = timeline.languages_commits[language][month]
            except KeyError:
                count = 0
            languages[language].append(count)

    json.dump(languages, open("language-timeline.json", "w"))

    # language-totals.json
    json.dump(timeline.get_language_totals().most_common(LANGUAGE_LIMIT), open("language-totals.json", "w"))


# Top overall languages
languages = list(zip(*timeline.get_language_totals().most_common(15)))
data = [go.Bar(x=languages[0], y=languages[1])]
figure = go.Figure(data=data, layout=go.Layout(title="Top Languages"))
py.plot(figure)

# Most popular languages
timeline.get_language_totals().most_common(15)

# Total number of commits
total = 0
for months in commits.commits.values():
    for month in months.values():
        total += month["commits"]

# Largest language pairs
language_pairs.most_common(10)

# Language pairs distribution
data = [list(language_pairs.values())]
figure = ff.create_distplot(data, ["language pairs"])
py.plot(figure)

# Percent of language pairs represented
possible_pairs = ((len(all_languages) ** 2) / 2)
len(language_pairs) / possible_pairs

# Percent of language pairs > 100
over_100 = 0
for pair, count in language_pairs.items():
    if count > 100:
        over_100 += 1
over_100/possible_pairs

# Number of languages each language is used with
languages_used = defaultdict(set)
for pair in language_pairs.keys():
    languages_used[pair[0]].add(pair[1])
    languages_used[pair[1]].add(pair[0])

languages_used_count = Counter()
for language, language_set in languages_used.items():
    languages_used_count[language] = len(language_set)

# Most generic languages
languages_used_count.most_common(20)

# Most special case languages
list(languages_used_count.most_common())[:-20:-1]