# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Giuseppe Barbalinardo's personal portfolio website - a static HTML/CSS/JavaScript site showcasing data science work, research, and blog posts. The site is hosted at https://giuseppe.barbalinardo.com.

## Architecture

- **Static Website**: No build system or package management - pure HTML/CSS/JS
- **Main Entry Point**: `index.html` - the primary portfolio page
- **Blog Posts**: Individual HTML files (01-blog-genai.html, 02-blog-aging.html, etc.)
- **Assets Structure**:
  - `css/` - Stylesheets including Bootstrap, Font Awesome, and custom styles
  - `js/` - JavaScript libraries (jQuery, Bootstrap, particles.js, etc.) and custom scripts
  - `img/` - Images, photos, and graphics organized by category
  - `fonts/` - Font Awesome web fonts

## Development Workflow

Since this is a static site with no build process:

- **No build commands needed** - files can be edited directly
- **No package.json or dependency management**
- **Testing**: Open HTML files directly in browser or use a simple HTTP server
- **Deployment**: Files are served as-is (likely via GitHub Pages given the CNAME file)

## Key Files

- `index.html` - Main portfolio page with all sections
- `css/style.css` - Custom styles (others are third-party libraries)
- `js/scripts.js` - Custom JavaScript functionality
- `CNAME` - Domain configuration for GitHub Pages hosting

## Content Structure

The site includes:
- Personal/professional bio and photo
- Portfolio projects with images
- Blog posts about AI, aging research, and data science
- Contact information and social links

## Editing Guidelines

- Maintain the existing Bootstrap-based responsive layout
- Image assets are organized in themed subdirectories under `img/`
- Blog posts follow a numbered naming convention (01-blog-*, 02-blog-*, etc.)
- Keep consistent styling with the existing design system