# Repository Guidelines

## Project Structure & Module Organization

This workspace contains multiple independent projects. Treat the specific project directory being changed (for example, `test-nextjs`, `e-commerce-laravel`, or `spring-car-rental`) as the repository root. Keep application source in the project's established source directory (`src/`, `app/`, or framework equivalent), tests in the existing test directory, and static resources in `public/`, `resources/`, or `assets/`. Do not move files across projects without an explicit reason.

## Build, Test, and Development Commands

Run commands from the selected project root and follow its manifest or README. Common examples are:

- `npm install` then `npm run dev` for JavaScript applications.
- `npm test` or `npm run lint` for JavaScript tests and checks.
- `composer install` then `php artisan serve` for Laravel applications.
- `./mvnw test` or `./gradlew test` for Spring projects.

Prefer project-provided wrapper scripts and document any required environment variables before running locally.

## Coding Style & Naming Conventions

Match the existing project formatter and linter configuration. Use four spaces for Python, two spaces for JavaScript/TypeScript, and the style already established by Java, PHP, or framework templates. Use `PascalCase` for classes and components, `camelCase` for variables and functions, and descriptive `kebab-case` names for URL-oriented files where the project uses them. Keep modules focused and avoid unrelated formatting changes.

## Testing Guidelines

Add tests beside the project's existing test suite using its established framework and naming pattern (for example, `*.test.ts`, `*_test.py`, or `*Test.java`). Run the narrowest relevant test first, then the full suite and lint checks before submitting changes. Preserve or improve existing coverage for changed behavior.

## Commit & Pull Request Guidelines

Use short, imperative commit subjects such as `Fix rental date validation` or `Add product search`. Keep commits focused. Pull requests should explain the behavior change, identify the project directory, link any issue, list validation commands, and include screenshots or API examples when UI or endpoint behavior changes.

## Security & Configuration Tips

Never commit secrets, local database files, build output, or `.env` files. Add new configuration keys to an example file such as `.env.example`, and describe safe local defaults in the project README.
