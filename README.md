# Static Site Generator

A minimal static site generator built as a learning project.\
It takes static assets and source files and produces a ready-to-serve
static website.

The focus of this project is simplicity: shell scripts, clear structure,
and no external frameworks.

------------------------------------------------------------------------

## Motivation

This project was created to better understand how static site generators
work internally and practice file manipulation, using simple tools and shell 
scripts instead of large frameworks.

------------------------------------------------------------------------

## Features

-   Generates a fully static website
-   Copies and organizes static assets (CSS, images, etc.)
-   Simple shell-based build process
-   Easy to understand and extend

------------------------------------------------------------------------

## Project Structure

```
static-site-generator/
├── static/        # Static assets (css, images, fonts, etc.)
├── docs/          # Generated site output
├── main.sh        # Build script
└── README.md
```

------------------------------------------------------------------------

## Usage

### 1. Clone the repository

```
git clone https://github.com/gonmpr/static-site-generator.git
cd static-site-generator
```

### 2. Add your files

-   Place all static assets inside the `static/` directory.
-   Organize files according to the existing structure.

Example:

```
static/
├── index.css
├── images/
│   └── tolkien.png
```

### 3. Build the site

Run the build script:

```
./main.sh
```

This script will: - Clean the output directory - Copy static files -
Generate the final site inside the `public/` directory

After running it, `public/` will contain the complete static website.

### 4. Preview locally

You can preview the generated site using a simple local server:

```
cd public
python -m http.server
```

Then open `http://localhost:8000` in your browser.

------------------------------------------------------------------------

## Deployment

The output consists only of static files, so deployment is
straightforward.

### Deploy using shell scripts

1.  Build the site:

``` 
./main.sh
```

2.  Upload the contents of the `public/` directory to your server or
    hosting provider.

Example using `scp`:

```
scp -r public/* user@server:/var/www/html
```

### GitHub Pages (example)

```
./main.sh
git add public
git commit -m "Build static site"
git push origin main
```

Configure GitHub Pages to serve from the `public/` directory.

