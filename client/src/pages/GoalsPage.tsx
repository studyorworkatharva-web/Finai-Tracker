import { AnimatedPage } from "../App";
import { Card } from "../components/ui/Card";

export default function GoalsPage() {
  return (
    <AnimatedPage>
      <div className="space-y-6">
        <h1 className="font-serif text-4xl font-bold">Goals</h1>
        <Card className="p-6">
          <p className="text-muted">
            You can define your financial goals here — like saving for travel,
            buying a car, or investing more.
          </p>
        </Card>
      </div>
    </AnimatedPage>
  );
}
