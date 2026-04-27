INSERT INTO invert02 (doc_id, keyword)
SELECT DISTINCT id, s.keyword AS keyword
FROM docs02 AS D, unnest(string_to_array(lower(D.doc), ' ')) AS s(keyword)
WHERE s.keyword NOT IN (SELECT word FROM stop_words)
ORDER BY id;