# 3Dev
3D graphical development software designed for constructing scenes and rendering semi-realistic ray-traced images
## Features
- Settings Menu
  - Render Preferences
  - Gallery
- Scene Creator
  - Object Manager
  - Object Addition Menu
  - Importing Assets
  - Scene Previews
  - Render Queue / Parallel Rendering
- Textures
- Effects
- Path Tracing
- Version Control
## Structure
```bash
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
      │	├── metadata/ 
      │ └── unique assets/ 
      └── common assets/
```
## User Requirements
Since PyOpenGL and the rust ray-tracing code will both make use of the GPU in order to render images, the user would require a graphics card to run my software. This limits the number of devices my program can run on but is necessary to render images of high quality in realistic amounts of time because of the GPUs parallel processing capabilities.
