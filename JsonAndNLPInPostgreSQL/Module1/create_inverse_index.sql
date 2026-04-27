INSERT INTO invert01 (doc_id, keyword)
SELECT DISTINCT id, s.keyword as keyword
FROM docs01 AS D, unnest(string_to_array(lower(D.doc), ' ')) as s(keyword);
