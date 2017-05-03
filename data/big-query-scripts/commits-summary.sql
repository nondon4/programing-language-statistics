SELECT
  repository,
  SUM(commits) AS total_commits,
  SUM(committers) AS total_committers
FROM
  LangStats.all_commits
GROUP BY
  repository
ORDER BY
  total_committers DESC;