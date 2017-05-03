SELECT
  c.repository,
  c.year,
  c.month,
  c.commits,
  c.committers
FROM
  LangStats.all_commits AS c
JOIN
  LangStats.commits_summary AS s
ON
  c.repository = s.repository
ORDER BY
  c.repository,
  c.year,
  c.month