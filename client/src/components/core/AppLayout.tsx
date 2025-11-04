import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { MoonIcon, SunIcon, ArrowLeftOnRectangleIcon } from "@heroicons/react/24/outline";
import { useTheme } from "../../contexts/ThemeProvider";
import { useAuthStore } from "../../hooks/useAuthStore";
import { Button } from "../ui/Button";

const navLinks = [
  { path: "/", label: "Dashboard" },
  { path: "/transactions", label: "Transactions" },
  { path: "/insights", label: "AI Insights" },
  { path: "/goals", label: "Goals" },
];

const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { resolvedTheme, setTheme } = useTheme();
  const { logout, user } = useAuthStore();
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside className="w-64 bg-card border-r border-slate-200/50 dark:border-slate-800/50 p-6 hidden md:flex flex-col justify-between">
        <div>
          <h2 className="text-2xl font-serif font-bold mb-8 bg-clip-text text-transparent bg-primary-gradient">
            FinAI
          </h2>
          <nav className="space-y-2">
            {navLinks.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `block px-3 py-2 rounded-md transition ${
                    isActive
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-slate-100 dark:hover:bg-slate-800"
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="space-y-4">
          <div className="text-sm text-muted">{user?.email || "Guest"}</div>
          <Button
            variant="ghost"
            icon={<ArrowLeftOnRectangleIcon className="h-5 w-5" />}
            onClick={() => {
              logout();
              navigate("/login");
            }}
          >
            Logout
          </Button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-6">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-serif font-bold">FinAI</h1>
          <Button
            variant="icon"
            onClick={() => setTheme(resolvedTheme === "light" ? "dark" : "light")}
          >
            {resolvedTheme === "light" ? (
              <MoonIcon className="h-5 w-5" />
            ) : (
              <SunIcon className="h-5 w-5" />
            )}
          </Button>
        </header>

        <div>{children}</div>
      </main>
    </div>
  );
};

export default AppLayout;
