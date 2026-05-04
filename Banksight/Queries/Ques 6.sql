#Question 6
#How many failed transactions occurred for each transaction type?
SELECT txn_type,
       COUNT(*) AS failed_count
FROM transactions
WHERE status = 'Failed'
GROUP BY txn_type;