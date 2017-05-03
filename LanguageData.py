import datetime
import json
import pickle

from collections import Counter, defaultdict

REPOSITORY_DATA = "repo-languages.json"
REPOSITORY_PICKLE = "repo-languages.pickle"

COMMIT_DATA = "data/commits-subset.json"
COMMIT_PICKLE = "data/commits-subset.pickle"

DATE_START = datetime.date(year=2009, month=1, day=1)
DATE_END = datetime.date(year=2017, month=3, day=1)


class Repository:
    def __init__(self, data):
        if not data["language"]:
            raise ValueError
        self.name = data["repo_name"]
        total_bytes = 0
        languages = {}
        for language in data["language"]:
            self.languages_set.append(language["name"])
            language_bytes = int(language["bytes"])
            total_bytes += language_bytes
            languages[language["name"]] = language_bytes

        if total_bytes <= 0:
            raise ValueError
        self.languages = {}
        for language, language_bytes in languages.items():
            self.languages[language] = int(language_bytes / total_bytes * 100)

    @staticmethod
    def load_repositories(path):
        repositories = {}
        for line in open(path):
            data = json.loads(line)
            try:
                repositories[data["repo_name"]] = Repository(data)
            except ValueError:
                continue
        return repositories

    @staticmethod
    def get_repositories():
        try:
            repositories = pickle.load(open(REPOSITORY_PICKLE, "rb"))
        except FileNotFoundError:
            repositories = Repository.load_repositories(REPOSITORY_DATA)
            pickle.dump(repositories, open(REPOSITORY_PICKLE, "wb"))
        return repositories

    @staticmethod
    def get_language_pairs(repositories):
        # collect all the edges
        edges = Counter()
        for repo in repositories.values():
            languages = list(repo.languages.keys())
            languages.sort(reverse=True)
            while len(languages) > 1:
                edge1 = languages.pop()
                for edge2 in languages:
                    edges[(edge1, edge2)] += 1

        return edges

    @staticmethod
    def get_all_languages(repositories):
        languages = set()
        for repo, data in repositories.items():
            for lang in data.languages.keys():
                languages.add(lang)
        return languages


class Commits:
    def __init__(self):
        self.commits = defaultdict(dict)

    def add(self, data):
        month = datetime.date(year=int(data["c_year"]), month=int(data["c_month"]), day=1)
        if not DATE_START <= month <= DATE_END:
            return
        commit_count = int(data["c_commits"])
        committer_count = int(data["c_committers"])
        repository = data["c_repository"]
        self.commits[repository][month] = {}
        self.commits[repository][month]["commits"] = commit_count
        self.commits[repository][month]["committers"] = committer_count

    @staticmethod
    def load_commits(path):
        commits = Commits()
        for line in open(path):
            data = json.loads(line)
            commits.add(data)
        return commits

    @staticmethod
    def get_commits():
        try:
            commits = pickle.load(open(COMMIT_PICKLE, "rb"))
        except FileNotFoundError:
            commits = Commits.load_commits(COMMIT_DATA)
            pickle.dump(commits, open(COMMIT_PICKLE, "wb"))
        return commits


class LanguageTimeline:
    def __init__(self, commits, repositories):
        self.languages_commits = defaultdict(Counter)
        self.languages_committers = defaultdict(Counter)
        for repository, counts_per_month in commits.commits.items():
            try:
                repository_data = repositories[repository]
            except KeyError:
                continue
            for month, counts in counts_per_month.items():
                for language, scalar in repository_data.languages.items():
                    self.languages_commits[language][month] += counts["commits"] * scalar
                    self.languages_committers[language][month] += counts["committers"] * scalar

    def get_language_totals(self):
        totals = Counter()
        for language, months in self.languages_commits.items():
            for month, count in months.items():
                totals[language] += count
        return totals


print("Loading Commits")
commits = Commits.get_commits()

print("Loading Repositories")
repositories = Repository.get_repositories()

print("Loading Timeline")
timeline = LanguageTimeline(commits, repositories)

print("Loading Language Pairs")
language_pairs = Repository.get_language_pairs(repositories)

print("Loading All Languages")
all_languages = Repository.get_all_languages(repositories)
