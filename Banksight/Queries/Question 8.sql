#Question 8
#Which accounts have 5 or more high-value transactions above ₹20,000?
SELECT customer_id,
       COUNT(*) AS high_value_txn
FROM transactions
WHERE amount > 20000
GROUP BY customer_id
HAVING COUNT(*) >= 5;



DESCRIBE transactions;