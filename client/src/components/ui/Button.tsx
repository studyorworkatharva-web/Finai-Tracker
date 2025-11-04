import React from 'react';
import { motion } from 'framer-motion';

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost' | 'icon';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  icon?: React.ReactNode;
}

const getVariantClasses = (variant: ButtonVariant) => {
  switch (variant) {
    case 'primary':
      return 'bg-primary text-primary-foreground hover:bg-primary/90 focus-visible:ring-primary';
    case 'secondary':
      return 'bg-card text-foreground border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 focus-visible:ring-primary';
    case 'danger':
      return 'bg-danger text-white hover:bg-danger/90 focus-visible:ring-danger';
    case 'ghost':
      return 'text-foreground hover:bg-slate-100 dark:hover:bg-slate-800 focus-visible:ring-primary';
    case 'icon':
      return 'p-2 rounded-full text-muted hover:text-foreground hover:bg-slate-100 dark:hover:bg-slate-800 focus-visible:ring-primary';
    default:
      return 'bg-primary text-primary-foreground hover:bg-primary/90';
  }
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', icon, children, className = '', ...props }, ref) => {
    const base =
      'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
    const size = variant === 'icon' ? 'h-10 w-10' : 'h-10 px-4 py-2';

    return (
      <motion.button
        ref={ref}
        className={`${base} ${size} ${getVariantClasses(variant)} ${className}`}
        whileTap={{ scale: 0.97 }}
        {...props}
      >
        {icon && <span className={children ? 'mr-2' : ''}>{icon}</span>}
        {children}
      </motion.button>
    );
  }
);
