#Ques 7
#What is the total number of transactions per transaction type?
SELECT txn_type,
      count(*) as total_transactions  #Counts all rows for that transaction type
FROM transactions GROUP BY txn_type;
