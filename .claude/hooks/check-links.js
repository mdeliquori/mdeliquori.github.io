// PostToolUse hook: after an .html file is edited, check that every local
// href/src/poster points to a file that exists with exactly matching case
// (GitHub Pages is case-sensitive; Windows is not). Reports, never blocks.
const fs = require("fs");
const path = require("path");

const SKIP = /^(https?:|\/\/|mailto:|tel:|data:|javascript:|#)/i;

function existsExactCase(target) {
  const root = path.parse(target).root;
  const parts = path.relative(root, target).split(path.sep).filter(Boolean);
  let current = root;
  for (const part of parts) {
    let entries;
    try {
      entries = fs.readdirSync(current);
    } catch {
      return false;
    }
    if (!entries.includes(part)) return false;
    current = path.join(current, part);
  }
  return true;
}

let input = "";
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  const payload = JSON.parse(input);
  const file = (payload.tool_response && payload.tool_response.filePath) || payload.tool_input.file_path;
  if (!file || !file.toLowerCase().endsWith(".html") || !fs.existsSync(file)) return;

  const html = fs.readFileSync(file, "utf8").replace(/<!--[\s\S]*?-->/g, "");
  const problems = [];
  const attr = /\b(?:href|src|poster)\s*=\s*["']([^"']+)["']/gi;
  let match;
  while ((match = attr.exec(html))) {
    const ref = match[1].trim();
    if (!ref || SKIP.test(ref)) continue;
    const clean = decodeURIComponent(ref.split(/[?#]/)[0]);
    if (!clean) continue;
    const target = path.resolve(path.dirname(file), clean);
    if (!existsExactCase(target)) problems.push(ref);
  }
  if (!problems.length) return;

  const unique = [...new Set(problems)];
  const message =
    `Link check for ${path.basename(file)}: ${unique.length} local reference(s) not found ` +
    `(missing, or filename case differs - GitHub Pages is case-sensitive): ${unique.join(", ")}. ` +
    `Ignore any that are intentional placeholders for files the user hasn't added yet.`;
  console.log(JSON.stringify({
    hookSpecificOutput: { hookEventName: "PostToolUse", additionalContext: message },
  }));
});
