#Question 4
#Which customers opened accounts in 2023 with a balance above ₹1,00,000?

SELECT customers.customer_id, customers.name, customers.join_date, account_balances.account_balance
FROM account_balances 
JOIN customers ON account_balances.customer_id = customers.customer_id
WHERE YEAR(customers.join_date) = 2023
  AND account_balances.account_balance > 100000;




