# 3Dev - 3D Graphics Development Software

**3Dev** is a 3D graphics development software currently under development, designed for constructing 3D scenes and rendering semi-realistic ray-traced images. This application aims to provide a comprehensive suite of tools for 3D environment creation and visualization.

---

## Implemented Features

Here's a breakdown of the features currently implemented in **3Dev**:

### Settings Menu

-   **Theme Customization**:
    -   Switch between Dark, Light, and System themes.
-   **User Preferences**:
    -   Theme selection.
    -   Autosave functionality (implementation may vary).
-   **Render Preferences**:
    -   Adjust basic render settings:
        -   Image Width
        -   Aspect Ratio
        -   Focus Distance
        -   Aperture
        -   Max Depth
        -   Samples per Pixel
    -   *Note: Backend implementation for render settings may be incomplete.*
-   **Security Settings**:
    -   Username and password change functionalities.
    -   Logout button.

### Dashboard Interface

-   **Top Menu**:
    -   Navigation bar for different application sections.
-   **Menu Navigation**:
    -   Buttons for:
        -   Version Control
        -   Asset Gallery
        -   Settings

### Asset Gallery

-   **Asset Cards**:
    -   Display assets with:
        -   Titles
        -   Sizes
        -   Import Dates
-   **Search Bar**:
    -   Asset filtering (functionality may be limited).
-   **Category Tabs**:
    -   Tabs for "Textures" and "Backgrounds" (category filtering may be limited).
-   **Asset Importing UI**:
    -   Basic UI for importing assets via:
        -   Drag and drop
        -   File selection
    -   *Note: Actual asset import and management may be limited.*

### Version Control

-   **Project Cards**:
    -   Display projects with:
        -   Titles
        -   Versions
        -   Creation Dates
-   **New Project Creation**:
    -   "New Scene" button in UI (project creation functionality may be limited).
-   **Project Launch**:
    -   "Launch Scene" buttons on project cards (scene launching and loading may be limited).

---

## Planned Features (Under Development)

The following features are planned for future development:

-   **Advanced Scene Creator**:
    -   Object Manager
    -   Object Addition Menu
    -   Scene Previews
    -   Render Queue
    -   Parallel Rendering

-   **Comprehensive Material and Texture System**:
    -   Texture application and customization.
    -   Material property definitions.

-   **Integrated Effects Engine**:
    -   Post-processing effects implementation.

-   **Path Tracing Renderer**:
    -   Core path tracing renderer for realistic rendering (current state and UI integration may vary).

---

## Software Structure

Project directory structure:

```
App/
└── User/
  ├── preferences/
  ├── assets/
  │ ├── textures/
  │ └── backgrounds/
  └── projects/
    └── project name/
      └── branch/
        ├── version name/
        │ ├── scene data/
        │ │ ├── metadata/
        │ │ └── unique assets/
        └── common assets/
```

---

## User Requirements

-   **Graphics Card**: A dedicated graphics card is recommended for optimal rendering performance, leveraging GPU acceleration.

---

This document provides a development status overview for 3Dev, outlining implemented UI features and planned functionalities. Continued development is underway to fully realize the potential of this 3D graphics software.
