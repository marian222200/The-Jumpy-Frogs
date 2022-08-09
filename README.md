# The-Jumpy-Frogs

An application that uses artificial intelligence to help the frogs that are on lily pads on a round lake to get to the shore.

![image](https://user-images.githubusercontent.com/30511514/172157070-762c5cdf-1a55-4454-9daa-2b18846e6c6e.png)

## Details about the problem

There are N frogs on lily pads at given coordinates at a lake. The lake is a circle with a given radius. The frogs can jump for their weight/3. Each jump the frogs loses one unit of weight. Some of the lily pads have food (insects) on them, each insect weights one unit. Each leaf has a maximum weight capacity.

## What the app does

The app runs for multiple given input (lake, frogs, leaves) the result of multiple graph traversal algorithms, used in AI, as it follows:

:small_blue_diamond: [BFS](https://en.wikipedia.org/wiki/Breadth-first_search "Breadth-first search")

:small_blue_diamond: [DFS](https://en.wikipedia.org/wiki/Depth-first_search "Depth-first search")

:small_blue_diamond: [DFS](https://en.wikipedia.org/wiki/Depth-first_search "Depth-first search")

:small_blue_diamond: [DFSI](https://www.geeksforgeeks.org/iterative-depth-first-traversal "Iterative Depth-first search")

:small_blue_diamond: [A*](https://en.wikipedia.org/wiki/A*_search_algorithm "A*")

The algorithms use different [heuristics](https://www.techopedia.com/definition/5436/heuristic "What is an heuristic?") in calculating the distance from the current configuration and a solution.
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
  The second heuristic returns the sum of the all Euclidian distances from each frog to the shore if the frog can reach the shore in one single jump, otherwise the value of the shortest distance for the frog (regardless of weight) to the shore making 2 jumps.
</details>

<details>
  <summary>
    [Non-admissible heuristic](https://en.wikipedia.org/wiki/Admissible_heuristic "What is an admissible heuristic?")
  </summary>
  The [Non-admissible heuristic](https://en.wikipedia.org/wiki/Admissible_heuristic "What is an admissible heuristic?") is just for test purposes. It is supposed to get longer times on the search algorithms.
</details>

## How to run the application

The application can be run in cmd, as it follows:

![lma](https://user-images.githubusercontent.com/30511514/183627121-7f90682c-b71b-44ee-9749-a129913bb107.png)

Where "input" is a folder with that name inside the project directory. In the input folder there are the files that give the data of the frogs and the lake. In the "output" folder the algorthm creates an output file for each input file ("output_" + name of file).
After the folder names, there are provided 2 numbers, the first one being the number of solutions required for the problem and the second one is the maximum time each algorithm has to run.

