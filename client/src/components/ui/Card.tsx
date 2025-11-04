import React from 'react';
import { motion } from 'framer-motion';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  withHover?: boolean;
}

export const Card: React.FC<CardProps> = ({ 
  children, 
  className = '', 
  withHover = false,
  ...props 
}) => {
  return (
    <motion.div
      className={`glass-card rounded-lg border border-slate-200/50 dark:border-slate-800/50 shadow-card ${className}`}
      whileHover={withHover ? { scale: 1.02, y: -4 } : {}}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
      {...props}
    >
      {children}
    </motion.div>
  );
};