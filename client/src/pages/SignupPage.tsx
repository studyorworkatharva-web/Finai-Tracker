import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authApi } from "../lib/api";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import toast from "react-hot-toast";
import { AnimatedPage } from "../App";

export default function SignupPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authApi.post("/auth/signup", { email, password });
      toast.success("Account created successfully!");
      navigate("/login");
    } catch (err) {
      toast.error("Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatedPage>
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="glass-card p-8 rounded-xl w-full max-w-md shadow-card border border-slate-200/50 dark:border-slate-800/50">
          <h1 className="text-3xl font-serif font-bold text-center mb-6">
            Create Account
          </h1>
          <form onSubmit={handleSignup} className="space-y-4">
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
              {loading ? "Signing up..." : "Sign Up"}
            </Button>
          </form>
          <p className="text-sm text-center mt-4 text-muted">
            Already have an account?{" "}
            <Link to="/login" className="text-primary hover:underline">
              Log in
            </Link>
          </p>
        </div>
      </div>
    </AnimatedPage>
  );
}
