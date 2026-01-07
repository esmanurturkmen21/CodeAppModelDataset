README

Project Title: MAZEESCAPE+: ONLINE A* SEARCH FOR AN INTELLIGENT AGENT IN PARTIALLY KNOWN GRID WORLDS

Student Name: Esmanur Türkmen
Department: Software Engineering Department
University: Istanbul Atlas University
Student ID: 210504025

1. Project Description

MazeEscape+ is a classical Artificial Intelligence project that investigates grid-based maze navigation under partial observability. The project formulates navigation as a symbolic search and planning problem rather than a machine learning task.
The agent operates in a grid-world environment and applies both Offline A* search (with full environment knowledge) and Online (Repeated) A* search, where replanning is performed dynamically as new obstacles are discovered. The implementation is based on the AIMA Python search framework.

2. Code Repository

The complete and runnable source code of the project is available at the following address:
GitHub Repository: [https://github.com/esmanurturkmen21/MazeEscape-Online-AStar]

3. Dataset Information

This project does not use a machine learning dataset.
The problem environment consists of grid-based maze layouts represented as text files. These maze files define free cells, obstacles, start positions, and goal positions, and are used directly during search execution. No training, validation, or test split is required.

4. How to Run the Project (Local Execution)

4.1 System Requirements

- Python 3.8 or higher
- Standard Python libraries
- AIMA Python search framework (included in the project files)

No external machine learning libraries are required.

4.2 Execution Instructions

Romania Route-Finding Validation:
python demos/demo_romania_greedy.py
python demos/demo_romania_ucs.py
python demos/demo_romania_astar.py


Offline A* Maze Execution: python mazeescape/experiments/run_offline.py

Online (Repeated) A* Maze Execution: python mazeescape/experiments/run_online.py

5. Project Video Presentation

The project video presentation demonstrating the theoretical background, code structure, and experimental results is available at the following address:
YouTube Video Link: https://youtube.com/PUT-YOUR-VIDEO-LINK-HERE

The video duration does not exceed 10–15 minutes and demonstrates all major components of the project, including algorithms, execution flow, and outputs.

6. Large Files

All files included in this ZIP archive are smaller than 50 MB.

No external download is required. If additional large files are needed, they will be provided via Google Drive.

7. Additional Notes

- This project focuses on classical symbolic Artificial Intelligence techniques.
- No machine learning models or training processes are involved.
- All experiments are reproducible using the provided scripts and maze configurations.

8. ZIP File Contents

The submitted ZIP file includes the following files:

- ProjectProposal_updated.docx
- ProjectPaper.docx
- ProjectPresentation.pptx
- CodeAppModelDataset.zip
- readme.docx
