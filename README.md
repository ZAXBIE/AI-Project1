# AI-Project1
Run the program in Command Prompt (not Powershell) to make sure that world.txt is utf-8 encoded
Run the following Commands to test Program:
# Generate a world (in cmd, bash, or Linux terminal)
python make_vacuum_world.py 4 5 0.1 2 > world.txt

# Run the planner with UCS
python planner.py uniform-cost world.txt

# Run with DFS
python planner.py depth-first world.txt
