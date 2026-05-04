# Question 5
# What is the total transaction volume (sum of amounts) by transaction type?

SELECT txn_type,
       SUM(amount) AS total_volume
FROM transactions GROUP BY txn_type;
