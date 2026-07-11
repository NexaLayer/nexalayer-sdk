import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const banned = [
  /out_dynamic_1/,
  /docs\.nexalayer\.com/,
  /api\.nexalayer\.com/,
  /https:\/\/nexalayer\.com/,
  /\/Users\//,
  /railway\.internal/,
  /agk_[A-Za-z0-9_-]{12,}/,
  /socks5:\/\/[^@\s]+:[^@\s]+@/,
];

const ignoredDirs = new Set([".git", ".pytest_cache", "dist", "node_modules"]);
const ignoredFiles = new Set([path.join("scripts", "validate-public-content.mjs")]);
const scannedSuffixes = [".md", ".py", ".ts", ".js", ".mjs", ".json", ".yml", ".yaml", ".toml", ".example"];

function walk(dir) {
  const entries = [];
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    if (item.isDirectory() && ignoredDirs.has(item.name)) continue;
    const full = path.join(dir, item.name);
    if (item.isDirectory()) entries.push(...walk(full));
    else entries.push(full);
  }
  return entries;
}

const files = walk(root).filter((file) => {
  const relative = path.relative(root, file);
  return scannedSuffixes.some((suffix) => file.endsWith(suffix)) && !ignoredFiles.has(relative);
});

const problems = [];
for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  for (const pattern of banned) {
    if (pattern.test(text)) {
      problems.push(`${path.relative(root, file)}: banned pattern ${pattern}`);
    }
  }
}

if (problems.length) {
  console.error(problems.join("\n"));
  process.exit(1);
}

console.log(`Validated ${files.length} public SDK files.`);
