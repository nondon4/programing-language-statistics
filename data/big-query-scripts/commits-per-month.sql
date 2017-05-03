SELECT
  C.repo_name AS repository,
  YEAR(C.date) AS year,
  MONTH(C.date) AS month,
  COUNT(C.commit) AS count,
  COUNT(DISTINCT c.email) as committers
FROM (
  SELECT
    repo_name,
    commit,
    author.date AS date,
    author.email as email,
  FROM
    FLATTEN([bigquery-public-data:github_repos.commits], repo_name)) AS C
GROUP BY
  repository,
  year,
  month;