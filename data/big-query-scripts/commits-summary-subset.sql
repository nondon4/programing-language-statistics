SELECT
  repository, total_commits, total_committers
FROM
  LangStats.commits_summary
WHERE
  RAND() < 0.1
ORDER BY
  total_committers DESC;