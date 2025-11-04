import React from "react";
import { Card } from "../ui/Card";

interface ChartCardProps {
  title: string;
  children: React.ReactNode;
}

export const ChartCard: React.FC<ChartCardProps> = ({ title, children }) => {
  return (
    <Card className="p-6" withHover>
      <h3 className="text-xl font-bold font-serif mb-4">{title}</h3>
      <div className="h-[350px]">{children}</div>
    </Card>
  );
};
