import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authApi } from "../lib/api";
import { useAuthStore } from "../hooks/useAuthStore";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import toast from "react-hot-toast";
import { AnimatedPage } from "../App";

export default function LoginPage() {
  const navigate = useNavigate();
  const loginStore = useAuthStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // ✅ Send JSON request to FastAPI
      const res = await authApi.post("/auth/login", {
        email,
        password,
      });

      // ✅ Save tokens in Zustand or localStorage
      await loginStore.login(res.data);

      toast.success("Login successful");
      navigate("/"); // Redirect to dashboard or home
    } catch (err: any) {
      console.error("Login failed:", err);
      toast.error("Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatedPage>
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="glass-card p-8 rounded-xl w-full max-w-md shadow-card border border-slate-200/50 dark:border-slate-800/50">
          <h1 className="text-3xl font-serif font-bold text-center mb-6">
            Welcome Back
          </h1>

          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>

          <p className="text-sm text-center mt-4 text-muted">
            Don’t have an account?{" "}
            <Link to="/signup" className="text-primary hover:underline">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </AnimatedPage>
  );
}
