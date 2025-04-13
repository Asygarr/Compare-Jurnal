import { marked } from "marked";

export function formatMarkdownResponse(response) {
  return { __html: marked(response) };
}
