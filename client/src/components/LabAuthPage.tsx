import { useState } from "react";
import {
  Shield, Lock, Activity, AlertTriangle,
  CheckCircle2, Clock, Mail, Key, Eye, EyeOff,
  ArrowRight, UserPlus, LogIn
} from "lucide-react";

interface LabAuthPageProps {
  onAuthSuccess: (email: string) => void;
}

type Step = "email" | "set-password" | "enter-password" | "success";

export default function LabAuthPage({ onAuthSuccess }: LabAuthPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [step, setStep] = useState<Step>("email");
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // ── Step 1: Check if email is whitelisted ──
  const handleCheckEmail = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (!email.includes("@") || !email.includes(".")) {
      setErrorMessage("Please enter a valid email address.");
      return;
    }

    setSubmitting(true);

    try {
      const res = await fetch("/api/auth/status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });
      const data = await res.json();

      if (res.ok && data.whitelisted) {
        if (data.hasPassword) {
          setSubmitting(false);
        setStep("enter-password");
        } else {
          setSubmitting(false);
        setStep("set-password");
        }
      } else {
        setErrorMessage(
          "This email is not authorized to access the Lab Workspace. Contact your administrator for access."
        );
        setSubmitting(false);
        setStep("email");
      }
    } catch {
      setErrorMessage("Could not reach the auth server. Please try again.");
      setSubmitting(false);
        setStep("email");
    }
  };

  // ── Step 2a: Create password ──
  const handleSetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (password.length < 12 || !/[A-Z]/.test(password)) {
      setErrorMessage("Password must be 12+ characters with an uppercase letter.");
      return;
    }
    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match.");
      return;
    }

    setSubmitting(true);

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password }),
      });
      const data = await res.json();

      if (res.ok && data.success) {
        setStep("success");
        setTimeout(() => onAuthSuccess(email.trim()), 800);
      } else {
        setErrorMessage(data.error || "Failed to create access key.");
        setSubmitting(false);
        setStep("set-password");
      }
    } catch {
      setErrorMessage("Could not reach the auth server.");
      setSubmitting(false);
        setStep("set-password");
    }
  };

  // ── Step 2b: Verify password ──
  const handleVerifyPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");

    if (password.length < 12 || !/[A-Z]/.test(password)) {
      setErrorMessage("Password must be 12+ characters with an uppercase letter.");
      return;
    }

    setSubmitting(true);

    try {
      const res = await fetch("/api/auth/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password }),
      });
      const data = await res.json();

      if (res.ok && data.success) {
        setStep("success");
        setTimeout(() => onAuthSuccess(email.trim()), 800);
      } else {
        setErrorMessage(data.error || "Invalid access key.");
        setSubmitting(false);
        setStep("enter-password");
      }
    } catch {
      setErrorMessage("Could not reach the auth server.");
      setSubmitting(false);
        setStep("enter-password");
    }
  };

  const isPending = submitting;

  return (
    <div className="flex-1 flex flex-col items-center justify-start relative min-h-[60vh] py-8 px-4">
      {/* Diagonal Watermark */}
      <div className="vinci-watermark opacity-40" />

      <div className="relative z-10 w-full max-w-lg">
        {/* Header */}
        <div className="text-center mb-8">
          <div className={`inline-flex items-center justify-center h-14 w-14 rounded-full border mb-4 transition-colors ${
            step === "set-password"
              ? "bg-[#B58C3D]/10 border-[#B58C3D]/20"
              : "bg-primary/10 border-primary/20"
          }`}>
            {step === "set-password"
              ? <UserPlus className="h-6 w-6 text-[#B58C3D]" />
              : <Lock className="h-6 w-6 text-primary" />
            }
          </div>
          <h2 className="font-serif text-2xl lg:text-3xl font-bold text-foreground tracking-tight">
            {step === "set-password"
              ? "Create Your Access Key"
              : step === "enter-password"
              ? "Enter Access Key"
              : "Lab Workspace Authorization"
            }
          </h2>
          <p className="text-sm text-muted-foreground mt-2 font-sans max-w-xs mx-auto leading-relaxed">
            {step === "set-password"
              ? "Set a key to protect your lab workspace access"
              : step === "enter-password"
              ? `Welcome back — enter your key for ${email}`
              : "Enter your authorized email to access the lab environment"
            }
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-card border border-border rounded-lg p-6 shadow-sm">
          {/* Step 1: Email entry */}
          {(step === "email") && (
            <form onSubmit={handleCheckEmail} className="space-y-5">
              <div className="space-y-1.5">
                <label className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold block">
                  Authorized Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/50" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="researcher@vinci.ai"
                    disabled={isPending}
                    className="w-full pl-10 pr-3 py-2.5 border border-input rounded bg-background text-foreground font-sans text-sm
                               placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                               transition-colors disabled:opacity-60"
                  />
                </div>
              </div>

              {errorMessage && (
                <div className="flex items-start gap-2 p-3 rounded bg-destructive/10 border border-destructive/20 text-destructive text-xs font-sans">
                  <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0 mt-0.5" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={isPending}
                className={`w-full flex items-center justify-center gap-2 py-2.5 rounded font-sans text-sm font-bold transition-all
                  ${isPending
                    ? "bg-amber-500/20 text-amber-400 cursor-wait border border-amber-500/30"
                    : "bg-primary text-primary-foreground hover:bg-primary/90 border border-primary"
                  }`}
              >
                {isPending ? (
                  <><Activity className="h-4 w-4 animate-spin" /> Checking...</>
                ) : (
                  <><ArrowRight className="h-4 w-4" /> Continue</>
                )}
              </button>
            </form>
          )}

          {/* Step 2a: Set password (new user) */}
          {(step === "set-password") && (
            <form onSubmit={handleSetPassword} className="space-y-5">
              <div className="flex items-center gap-2 p-3 rounded bg-primary/5 border border-primary/10 text-xs font-mono text-primary">
                <Mail className="h-3.5 w-3.5 flex-shrink-0" />
                <span className="truncate">{email}</span>
                <button
                  type="button"
                  onClick={() => { setSubmitting(false);
        setStep("email"); setErrorMessage(""); setPassword(""); setConfirmPassword(""); }}
                  className="ml-auto text-[10px] text-muted-foreground hover:text-foreground underline flex-shrink-0"
                >
                  Change
                </button>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] uppercase tracking-widest font-mono text-[#B58C3D] font-bold block">
                  Create Access Key
                </label>
                <div className="relative">
                  <Key className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/50" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="••••••••••••"
                    disabled={isPending}
                    className="w-full pl-10 pr-10 py-2.5 border border-input rounded bg-background text-foreground font-mono text-sm
                               placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-[#B58C3D]/30 focus:border-[#B58C3D]
                               transition-colors disabled:opacity-60"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] uppercase tracking-widest font-mono text-[#B58C3D] font-bold block">
                  Confirm Access Key
                </label>
                <input
                  type={showPassword ? "text" : "password"}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  placeholder="••••••••••••"
                  disabled={isPending}
                  className="w-full px-3 py-2.5 border border-input rounded bg-background text-foreground font-mono text-sm
                             placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-[#B58C3D]/30 focus:border-[#B58C3D]
                             transition-colors disabled:opacity-60"
                />
                {confirmPassword && password !== confirmPassword && (
                  <p className="text-[10px] text-destructive font-mono">Passwords do not match</p>
                )}
              </div>

              <p className="text-[10px] text-muted-foreground font-mono">
                12+ characters with uppercase letter required
              </p>

              {errorMessage && (
                <div className="flex items-start gap-2 p-3 rounded bg-destructive/10 border border-destructive/20 text-destructive text-xs font-sans">
                  <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0 mt-0.5" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={isPending}
                className={`w-full flex items-center justify-center gap-2 py-2.5 rounded font-sans text-sm font-bold transition-all
                  ${isPending
                    ? "bg-amber-500/20 text-amber-400 cursor-wait border border-amber-500/30"
                    : "bg-[#B58C3D] text-white hover:bg-[#9a6f2e] border border-[#B58C3D]"
                  }`}
              >
                {isPending ? (
                  <><Activity className="h-4 w-4 animate-spin" /> Creating...</>
                ) : (
                  <><UserPlus className="h-4 w-4" /> Create Access Key</>
                )}
              </button>
            </form>
          )}

          {/* Step 2b: Enter password (returning user) */}
          {(step === "enter-password") && (
            <form onSubmit={handleVerifyPassword} className="space-y-5">
              <div className="flex items-center gap-2 p-3 rounded bg-primary/5 border border-primary/10 text-xs font-mono text-primary">
                <Mail className="h-3.5 w-3.5 flex-shrink-0" />
                <span className="truncate">{email}</span>
                <button
                  type="button"
                  onClick={() => { setSubmitting(false);
        setStep("email"); setErrorMessage(""); setPassword(""); }}
                  className="ml-auto text-[10px] text-muted-foreground hover:text-foreground underline flex-shrink-0"
                >
                  Change
                </button>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold block">
                  Access Key
                </label>
                <div className="relative">
                  <Key className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/50" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="••••••••••••"
                    disabled={isPending}
                    className="w-full pl-10 pr-10 py-2.5 border border-input rounded bg-background text-foreground font-mono text-sm
                               placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
                               transition-colors disabled:opacity-60"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {errorMessage && (
                <div className="flex items-start gap-2 p-3 rounded bg-destructive/10 border border-destructive/20 text-destructive text-xs font-sans">
                  <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0 mt-0.5" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={isPending}
                className={`w-full flex items-center justify-center gap-2 py-2.5 rounded font-sans text-sm font-bold transition-all
                  ${isPending
                    ? "bg-amber-500/20 text-amber-400 cursor-wait border border-amber-500/30"
                    : "bg-primary text-primary-foreground hover:bg-primary/90 border border-primary"
                  }`}
              >
                {isPending ? (
                  <><Activity className="h-4 w-4 animate-spin" /> Verifying...</>
                ) : (
                  <><LogIn className="h-4 w-4" /> Access Lab Workspace</>
                )}
              </button>
            </form>
          )}

          {/* Success state */}
          {step === "success" && (
            <div className="flex flex-col items-center py-6 gap-3">
              <div className="h-12 w-12 rounded-full bg-[#589C7E]/15 border border-[#589C7E]/30 flex items-center justify-center">
                <CheckCircle2 className="h-6 w-6 text-[#589C7E]" />
              </div>
              <span className="font-serif text-lg font-bold text-foreground">Access Granted</span>
              <span className="text-xs text-muted-foreground font-mono">Loading workspace...</span>
            </div>
          )}
        </div>

        {/* Status Indicator Bar */}
        <div className="flex flex-wrap items-center justify-center gap-2.5 mt-5">
          <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full border text-[11px] font-mono font-bold transition-all
            ${step === "success"
              ? "bg-[#509BB4]/15 border-[#509BB4]/40 text-[#509BB4]"
              : "bg-muted/30 border-border text-muted-foreground/50"
            }`}>
            <div className={`h-1.5 w-1.5 rounded-full ${step === "success" ? "bg-[#509BB4]" : "bg-muted-foreground/30"}`} />
            Active Session
          </div>

          <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full border text-[11px] font-mono font-bold transition-all
            ${isPending
              ? "bg-[#B58C3D]/15 border-[#B58C3D]/40 text-[#B58C3D]"
              : step !== "success"
              ? "bg-[#B58C3D]/10 border-[#B58C3D]/25 text-[#B58C3D]/80"
              : "bg-muted/30 border-border text-muted-foreground/50"
            }`}>
            <div className={`h-1.5 w-1.5 rounded-full ${
              isPending ? "bg-[#B58C3D] animate-pulse" : step !== "success" ? "bg-[#B58C3D]/60" : "bg-muted-foreground/30"
            }`} />
            {isPending ? "Processing..." : "Pending Verification"}
          </div>

          <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full border text-[11px] font-mono font-bold transition-all
            ${step === "set-password"
              ? "bg-[#8A69AD]/10 border-[#8A69AD]/25 text-[#8A69AD]/80"
              : "bg-muted/30 border-border text-muted-foreground/50"
            }`}>
            <div className={`h-1.5 w-1.5 rounded-full ${step === "set-password" ? "bg-[#8A69AD]/60" : "bg-muted-foreground/30"}`} />
            {step === "set-password" ? "Key Setup" : "Invitation Only"}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between mt-4 pt-4 border-t border-border flex-wrap gap-2">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#589C7E]/10 border border-[#589C7E]/20 text-[#589C7E] text-[11px] font-mono font-bold">
            <Shield className="h-3 w-3" />
            Secure Connection
          </div>
          <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground font-mono">
            <Clock className="h-3 w-3" />
            <span>Session expires in 15 min</span>
          </div>
        </div>
      </div>
    </div>
  );
}