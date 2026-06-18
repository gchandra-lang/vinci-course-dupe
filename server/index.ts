import express from "express";
import { createServer } from "http";
import path from "path";
import { fileURLToPath } from "url";
import { readFileSync, writeFileSync, existsSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ── Simple password hashing ──
function simpleHash(input: string, salt: string): string {
  let combined = salt + "::" + input;
  for (let i = 0; i < 5; i++) {
    combined = Buffer.from(combined.split("").reverse().join("") + combined).toString("base64");
  }
  return Buffer.from(combined + "::" + salt).toString("base64");
}

function generateSalt(): string {
  return Buffer.from(String(Date.now()) + String(Math.random()))
    .toString("base64")
    .replace(/[^a-zA-Z0-9]/g, "")
    .slice(0, 16);
}

interface UserEntry {
  email: string;
  passwordHash?: string | null;
  salt?: string | null;
}

function loadUsers(): UserEntry[] {
  const usersPath = path.resolve(__dirname, "allowed_users.json");
  if (!existsSync(usersPath)) {
    console.warn("[auth] allowed_users.json not found.");
    return [];
  }
  try {
    const raw = readFileSync(usersPath, "utf-8");
    const data = JSON.parse(raw);
    return (data.users ?? []).map((u: any) => ({
      email: (u.email ?? "").toLowerCase().trim(),
      passwordHash: u.passwordHash || null,
      salt: u.salt || null,
    }));
  } catch (err) {
    console.error("[auth] Failed to parse allowed_users.json:", err);
    return [];
  }
}

function saveUsers(users: UserEntry[]): void {
  const usersPath = path.resolve(__dirname, "allowed_users.json");
  const data = {
    description: "Users allowed to access the Lab Workspace.",
    users,
  };
  writeFileSync(usersPath, JSON.stringify(data, null, 2), "utf-8");
}

async function startServer() {
  const app = express();
  const server = createServer(app);

  app.use(express.json());

  // ── POST /api/auth/status ──
  app.post("/api/auth/status", (_req, res) => {
    const { email } = _req.body;
    if (!email || typeof email !== "string" || !email.includes("@")) {
      res.status(400).json({ success: false, error: "A valid email address is required." });
      return;
    }
    const normalized = email.toLowerCase().trim();
    const users = loadUsers();
    const user = users.find(u => u.email === normalized);
    res.json({ whitelisted: !!user, hasPassword: !!(user?.passwordHash) });
  });

  // ── POST /api/auth/register ──
  app.post("/api/auth/register", (_req, res) => {
    const { email, password } = _req.body;
    if (!email || !password || typeof password !== "string" || password.length < 12) {
      res.status(400).json({ success: false, error: "Email and a password (12+ chars) are required." });
      return;
    }
    const normalized = email.toLowerCase().trim();
    const users = loadUsers();
    const user = users.find(u => u.email === normalized);

    if (!user) {
      res.status(403).json({ success: false, error: "This email is not authorized." });
      return;
    }
    if (user.passwordHash) {
      res.status(409).json({ success: false, error: "Password already set. Use sign-in instead." });
      return;
    }

    const salt = generateSalt();
    user.passwordHash = simpleHash(password, salt);
    user.salt = salt;
    saveUsers(users);

    console.log(`[auth] Password set for: ${normalized}`);
    res.json({ success: true, message: "Access key created." });
  });

  // ── POST /api/auth/verify ──
  app.post("/api/auth/verify", (_req, res) => {
    const { email, password } = _req.body;
    if (!email || typeof email !== "string" || !email.includes("@")) {
      res.status(400).json({ success: false, error: "A valid email address is required." });
      return;
    }
    const normalized = email.toLowerCase().trim();
    const users = loadUsers();
    const user = users.find(u => u.email === normalized);

    if (!user) {
      res.status(403).json({ success: false, error: "This email is not authorized." });
      return;
    }

    // No password set → needs to create one
    if (!user.passwordHash && !password) {
      res.json({ success: true, email: normalized, needsPassword: true });
      return;
    }

    // Password set → must match
    if (user.passwordHash && user.salt) {
      if (!password || typeof password !== "string") {
        res.status(401).json({ success: false, error: "Access key required." });
        return;
      }
      const enteredHash = simpleHash(password, user.salt);
      if (enteredHash === user.passwordHash) {
        console.log(`[auth] Access granted: ${normalized}`);
        res.json({ success: true, email: normalized, message: "Access granted." });
      } else {
        console.log(`[auth] Wrong password: ${normalized}`);
        res.status(401).json({ success: false, error: "Invalid access key." });
      }
      return;
    }

    // Fallback: whitelisted, no password
    res.json({ success: true, email: normalized });
  });

  // Serve static files from dist/public in production
  const staticPath =
    process.env.NODE_ENV === "production"
      ? path.resolve(__dirname, "public")
      : path.resolve(__dirname, "..", "dist", "public");

  app.use(express.static(staticPath));

  // Handle client-side routing
  app.get("*", (_req, res) => {
    res.sendFile(path.join(staticPath, "index.html"));
  });

  const port = process.env.PORT || 3000;
  server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}/`);
  });
}

startServer().catch(console.error);