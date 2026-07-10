---
name: "sdlc-conventions"
description: "JavaScript/Node.js project conventions covering ES modules, file organization, and model/service/utility patterns."
version: "1.0.0"
---
# JavaScript/Node.js SDLC conventions

## Runtime and module system

- Target Node.js 20+.
- Use ES module syntax only (`import`/`export`). Do not use CommonJS (`require`/`module.exports`).
- Prefer built-in Node.js modules for core functionality. Add external dependencies only when they are explicitly approved.

## Code style

- Use 2-space indentation.
- Use single quotes for strings.
- Use `const` by default; use `let` only when reassignment is required. Never use `var`.
- Add JSDoc comments to exported functions, classes, and public methods.

## Error handling

- Use `try/catch` around operations that may fail when you need to recover, translate, or log the error.
- Throw `Error` or `TypeError` instances with descriptive messages. Never throw plain strings.
- Log errors with `console.error`, not `console.log`.

## Testing

- For lightweight Node.js projects, prefer the built-in test runner (`node --test`) and `node:assert`.
- Name test files `*.test.js`.
- Keep each test focused on exactly one behavior and cover both success and error paths.

## File organization conventions

### `src/models/**`

- Export a single class per file.
- Validate constructor arguments and throw a `TypeError` with a descriptive message for invalid inputs.
- Include a `toJSON()` method that returns a plain object.
- Generate unique IDs with `crypto.randomUUID()` when a model is responsible for identity creation.
- Add JSDoc comments to the class and every public method.

### `src/services/**`

- Export functions, not classes.
- Every function that modifies data must return the modified object.
- Return copies of data instead of direct references to internal state.
- Throw descriptive errors for invalid input and not-found cases.
- Keep functions small so each one handles a single operation.

### `src/utils/**`

- Export pure functions only; avoid side effects.
- Validate inputs and throw a `TypeError` for invalid arguments.
- Include at least two usage examples in each JSDoc comment.

## Design patterns

- Organize files by responsibility so paths communicate intent: models define domain entities, services coordinate operations, and utilities stay pure and reusable.
- Keep designs minimal and add only the files and abstractions the current feature requires.
- Entry points may use `console.log` to demonstrate behavior, but reusable modules should stay side-effect free unless their purpose requires otherwise.
