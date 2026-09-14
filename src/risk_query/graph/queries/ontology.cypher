// Canonical concept lookup
MATCH (c:Concept)
WHERE lower(c.name) = lower($text)
RETURN c

// Approved business relationship traversal
MATCH (a:Concept {id: $source})-[r:OPERATES_IN]->(g:Concept)
WHERE r.approval_status = 'approved'
RETURN g
