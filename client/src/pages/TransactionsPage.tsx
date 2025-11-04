import { useEffect, useState } from "react";
import { transactionsApi } from "../lib/api";
import { Card } from "../components/ui/Card";
import { AnimatedPage } from "../App";

interface Transaction {
  id: number;
  description: string;
  amount: number;
  category?: string;
  date?: string;
}

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const res = await transactionsApi.get("/");
        setTransactions(res.data.transactions || []);
      } catch (err) {
        console.error("Failed to fetch transactions", err);
      }
    })();
  }, []);

  return (
    <AnimatedPage>
      <div className="space-y-6">
        <h1 className="font-serif text-4xl font-bold">Transactions</h1>
        <Card className="p-4">
          {transactions.length === 0 ? (
            <p className="text-muted">No transactions available.</p>
          ) : (
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200/50">
                  <th className="py-2">Date</th>
                  <th className="py-2">Description</th>
                  <th className="py-2">Category</th>
                  <th className="py-2 text-right">Amount</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((tx) => (
                  <tr
                    key={tx.id}
                    className="border-b border-slate-200/30 hover:bg-slate-50 dark:hover:bg-slate-800/40"
                  >
                    <td>{tx.date?.split("T")[0]}</td>
                    <td>{tx.description}</td>
                    <td>{tx.category || "-"}</td>
                    <td className="text-right font-medium">${tx.amount.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>
      </div>
    </AnimatedPage>
  );
}
