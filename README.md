# The-Jumpy-Frogs

An application that uses artificial intelligence to help the frogs that are on lily pads on a round lake to get to the shore.

![image](https://user-images.githubusercontent.com/30511514/172157070-762c5cdf-1a55-4454-9daa-2b18846e6c6e.png)

## Details about the problem

There are N frogs on lily pads at given coordinates at a lake. The lake is a circle with a given radius. The frogs can jump for their weight/3. Each jump the frogs loses one unit of weight. Some of the lily pads have food (insects) on them, each insect weights one unit. Each leaf has a maximum weight capacity. The cost of each transition is the length of all the jumps of the frogs from one state to the other. Each frog that did not reach the shore jumps once  per transition from one state to the other.

## What the app does

The app runs for multiple given input (lake, frogs, leaves) the result of multiple graph traversal algorithms, used in AI, as it follows:

:small_blue_diamond: [BFS](https://en.wikipedia.org/wiki/Breadth-first_search "Breadth-first search")

:small_blue_diamond: [DFS](https://en.wikipedia.org/wiki/Depth-first_search "Depth-first search")

:small_blue_diamond: [DFS](https://en.wikipedia.org/wiki/Depth-first_search "Depth-first search")

:small_blue_diamond: [DFSI](https://www.geeksforgeeks.org/iterative-depth-first-traversal "Iterative Depth-first search")

:small_blue_diamond: [A*](https://en.wikipedia.org/wiki/A*_search_algorithm "A*")

The algorithms use different [heuristics](https://www.techopedia.com/definition/5436/heuristic "What is an heuristic?") of wich one is a [non-admissible heuristic](https://en.wikipedia.org/wiki/Admissible_heuristic "What is an admissible heuristic?") in calculating the distance from the current configuration and a solution.
<details>
  <summary>
    Banal heuristic
  </summary>
  <br>
  This heuristic returns 1 if the current state is not a solution, 0 otherwise. It is banal because, while being admissible, it does not give any additional information of wether the state is close to being a solution or not.
</details>

<details>
  <summary>
    First heuristic
  </summary>
  <br>
  The first heuristic returns the sum of the all Euclidian distances from each frog to the shore.
</details>

<details>
  <summary>
    Second heuristic
  </summary>
  <br>
  The second heuristic returns the sum of the all Euclidian distances from each frog to the shore if the frog can reach the shore in one single jump, otherwise the value of the shortest distance for the frog (regardless of weight) to the shore making 2 jumps.
</details>

<details>
  <summary>
    Non-admissible heuristic
  </summary>
  <br>
  This heuristic is just for test purposes. It returns, for a part of the frogs, a result that is greater than the actual distance cost. It is supposed to get longer times on the search algorithms.
</details>

## How to run the application

The application can be run in cmd, as it follows:

![lma](https://user-images.githubusercontent.com/30511514/183627121-7f90682c-b71b-44ee-9749-a129913bb107.png)

Where "input" is a folder with that name inside the project directory. In the input folder there are the files that give the data of the frogs and the lake. In the "output" folder the algorthm creates an output file for each input file ("output_" + name of file).
After the folder names, there are provided 2 numbers, the first one being the number of solutions required for the problem and the second one is the maximum time each algorithm has to run.

## Input example:

🔹 The text inside the input files follows this template:

![image](https://user-images.githubusercontent.com/30511514/183637948-bb9b2cc8-836e-485c-821a-4ec9af4458df.png)

🔹 Input file example:

![image](https://user-images.githubusercontent.com/30511514/183638490-4c37faf3-6e2e-4bc0-b028-821acb8e068e.png)

## Output example:

🔹 The text inside the output files follows this template:

![image](https://user-images.githubusercontent.com/30511514/183642672-6ebb5659-f9a0-43a9-a294-636cf108bc44.png)

🔹 Output example:

![image](https://user-images.githubusercontent.com/30511514/183642788-c559c156-c68b-445e-ad95-1c56e67132c4.png)
