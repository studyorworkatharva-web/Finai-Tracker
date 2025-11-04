import { AnimatedPage } from '../App';
import { Card } from '../components/ui/Card';
import { ChartCard } from '../components/specific/ChartCard';
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
import { ArrowDownLeft, ArrowUpRight, Banknote } from 'lucide-react';

// Mock data for charts
const mockChartData = [
  { name: 'Food', spend: 400 },
  { name: 'Transport', spend: 200 },
  { name: 'Shopping', spend: 300 },
  { name: 'Utilities', spend: 150 },
  { name: 'Rent', spend: 1200 },
];

export default function DashboardPage() {
  return (
    <AnimatedPage>
      <div className="space-y-6">
        {/* Page Header */}
        <h1 className="font-serif text-4xl font-bold">Welcome Back,</h1>
        
        {/* Hero Cards Grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted">Total Balance</h3>
              <Banknote className="h-5 w-5 text-muted" />
            </div>
            <div className="mt-4">
              <span className="font-serif text-4xl font-bold">$12,450.00</span>
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted">Monthly Income</h3>
              <ArrowUpRight className="h-5 w-5 text-success" />
            </div>
            <div className="mt-4">
              <span className="font-serif text-4xl font-bold text-success">$5,200.00</span>
            </div>
          </Card>
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted">Monthly Spend</h3>
              <ArrowDownLeft className="h-5 w-5 text-danger" />
            </div>
            <div className="mt-4">
              <span className="font-serif text-4xl font-bold text-danger">$2,250.80</span>
            </div>
          </Card>
        </div>
        
        {/* Charts & Insights Grid */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
          {/* Spending Chart */}
          <div className="lg:col-span-3">
            <ChartCard title="Spending by Category (Oct)">
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={mockChartData}>
                  <XAxis dataKey="name" stroke="#94A3B8" fontSize={12} />
                  <YAxis stroke="#94A3B8" fontSize={12} />
                  <Tooltip
                    contentStyle={{ 
                      backgroundColor: 'var(--color-card-bg)', 
                      backdropFilter: 'blur(10px)',
                      borderRadius: 'var(--radius-md)',
                      borderColor: 'var(--color-primary)'
                    }}
                  />
                  <Bar dataKey="spend" fill="var(--color-primary)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </div>
          
          {/* AI Insights Panel */}
          <div className="lg:col-span-2">
            <Card className="p-6" withHover>
              <h3 className="text-xl font-bold font-serif mb-4">Smart Insights</h3>
              <div className="prose prose-sm dark:prose-invert text-muted max-w-none">
                <p>
                  Your spending on <strong className="text-foreground">Food & Drink</strong> is up <strong>15%</strong> this month.
                </p>
                <ul>
                  <li>You've spent $120 at Starbucks.</li>
                  <li>Consider setting a budget for "Dining Out".</li>
                </ul>
                <Button variant="secondary" className="mt-4">
                  Ask FinAI...
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </AnimatedPage>
  );
}