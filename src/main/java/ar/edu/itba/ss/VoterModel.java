package ar.edu.itba.ss;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class VoterModel {

    private static final String RESULTS_DIR = "results";
    private static final double[] PROBABILITIES = {0.01, 0.1, 0.9};

    private static final List<Integer> results = new ArrayList<>();
    private static final Random random = new Random();

    private static int gridSize = 50;
    private static int monteCarloSteps = 100000000;
    private static int saveInterval;

    private static int[][] grid;

    private static String resultFileNameTemplate = "%%s/result_%%0%dd.txt";

    public static void main(String[] args) {
        if (args.length > 0) {
            try {
                gridSize = Integer.parseInt(args[0]);
                monteCarloSteps = Integer.parseInt(args[1]);
            } catch (NumberFormatException e) {
                System.err.println("Usage: java VoterModel <grid_size> <monte_carlo_steps>");
                System.exit(1);
            }
        }

        grid = new int[gridSize][gridSize];
        saveInterval = gridSize * gridSize;

        int resultMaxLengthTemplate = String.valueOf(monteCarloSteps).length();
        resultFileNameTemplate = String.format(resultFileNameTemplate, resultMaxLengthTemplate);

        for (double probability : PROBABILITIES) {
            results.clear();

            initializeGrid();
            runMonteCarloSimulation(probability);
            saveGeneralResults(probability);
        }
    }

    private static void initializeGrid() {
        for (int i = 0; i < gridSize; i++) {
            for (int j = 0; j < gridSize; j++) {
                grid[i][j] = random.nextBoolean() ? 1 : -1;
            }
        }
    }

    private static void runMonteCarloSimulation(double probability) {
        String dirPath = String.format("%s/%.4f", RESULTS_DIR, probability);
        File dir = new File(dirPath);

        if (!dir.exists() && !dir.mkdirs()) {
            System.err.println("Failed to create directory: " + dirPath);
            System.exit(1);
        }

        for (int step = 1; step <= monteCarloSteps; step++) {
            int i = random.nextInt(gridSize);
            int j = random.nextInt(gridSize);

            int neighborSum = grid[(i - 1 + gridSize) % gridSize][j] + grid[(i + 1) % gridSize][j] +
                    grid[i][(j - 1 + gridSize) % gridSize] + grid[i][(j + 1) % gridSize];

            int majorityOpinion = grid[i][j];
            if (neighborSum != 0)
                majorityOpinion = (neighborSum > 0) ? 1 : -1;

            if (random.nextDouble() <= probability)
                grid[i][j] = -grid[i][j];
            else
                grid[i][j] = majorityOpinion;

            if (step % saveInterval == 0)
                saveResults(step, dirPath);
        }
    }

    private static void saveResults(int iteration, String dirPath) {
        String fileName = String.format(resultFileNameTemplate, dirPath, iteration);
        int sum = 0;

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (int i = 0; i < gridSize; i++) {
                for (int j = 0; j < gridSize; j++) {
                    writer.write(grid[i][j] + " ");
                    sum += grid[i][j];
                }
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error writing to file: " + fileName);
            System.exit(1);
        }

        results.add(sum);
    }

    private static void saveGeneralResults(Double probability) {
        String fileName = String.format("%s/general_%.4f.txt", RESULTS_DIR, probability);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (Integer result : results) {
                writer.write(Math.abs(result / (gridSize * gridSize)));
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error writing to file: " + fileName);
            System.exit(1);
        }
    }

}
