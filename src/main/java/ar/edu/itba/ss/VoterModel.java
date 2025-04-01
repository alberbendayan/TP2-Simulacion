package ar.edu.itba.ss;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.*;

public class VoterModel {

    private static final String RESULTS_DIR = "results";

    private static final List<Integer> results = new ArrayList<>();
    private static final Random random = new Random();

    private static int gridSize = 50;
    private static int monteCarloSteps = 40000;
    private static int metropolisSteps;
    private static int saveInterval;

    private static int[][] grid;
    private static double[] probabilities = {0.01, 0.1, 0.9};

    private static String resultsDirectory;
    private static String resultFileNameTemplate = "%%s/result_%%0%dd.txt";

    private static boolean saveStates = false;

    public static void main(String[] args) {
        if (args.length > 0) {
            try {
                gridSize = Integer.parseInt(args[0]);
                monteCarloSteps = Integer.parseInt(args[1]);
                if (args.length > 2) {
                    probabilities = Arrays.stream(args[2].split(",")).mapToDouble(Double::valueOf).toArray();
                    if (args.length > 3) {
                        saveStates = Boolean.parseBoolean(args[3]);
                    }
                }
            } catch (Exception e) {
                System.err.println("Usage: java VoterModel <grid_size> <monte_carlo_steps>");
                System.exit(1);
            }
        }

        grid = new int[gridSize][gridSize];
        saveInterval = gridSize * gridSize;
        metropolisSteps = monteCarloSteps * saveInterval;

        int resultMaxLengthTemplate = String.valueOf(metropolisSteps).length();
        resultFileNameTemplate = String.format(Locale.US, resultFileNameTemplate, resultMaxLengthTemplate);

        resultsDirectory = String.format(Locale.US, "%s/%s", RESULTS_DIR, new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss").format(new Date()));

        File dir = new File(resultsDirectory);
        if (!dir.exists() && !dir.mkdirs()) {
            System.err.println("Failed to create directory: " + dir);
            System.exit(1);
        }

        saveConfigurationJson();

        for (double probability : probabilities) {
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
        String dirPath = String.format(Locale.US, "%s/%.4f", resultsDirectory, probability);

        if (saveStates) {
            File dir = new File(dirPath);
            if (!dir.exists() && !dir.mkdirs()) {
                System.err.println("Failed to create directory: " + dir);
                System.exit(1);
            }
        }

        for (int step = 1; step <= metropolisSteps; step++) {
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
        String fileName = String.format(Locale.US, resultFileNameTemplate, dirPath, iteration);
        int sum = 0;

        if (saveStates) {
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
        } else {
            for (int i = 0; i < gridSize; i++) {
                for (int j = 0; j < gridSize; j++) {
                    sum += grid[i][j];
                }
            }
        }

        results.add(sum);
    }

    private static void saveGeneralResults(Double probability) {
        String fileName = String.format(Locale.US, "%s/general_%.4f.txt", resultsDirectory, probability);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (Integer result : results) {
                writer.write(String.valueOf(Math.abs((double) result / (gridSize * gridSize))));
                writer.newLine();
            }
        } catch (IOException e) {
            System.err.println("Error writing to file: " + fileName);
            System.exit(1);
        }
    }

    private static void saveConfigurationJson() {
        String fileName = String.format(Locale.US, "%s/config.json", resultsDirectory);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            writer.write("{\n");
            writer.write("  \"gridSize\": " + gridSize + ",\n");
            writer.write("  \"monteCarloSteps\": " + monteCarloSteps + ",\n");
            writer.write("  \"metropolisSteps\": " + metropolisSteps + ",\n");
            writer.write("  \"saveInterval\": " + saveInterval + ",\n");
            writer.write("  \"probabilities\": [" + String.join(", ", Arrays.stream(probabilities).mapToObj(String::valueOf).toArray(String[]::new)) + "]\n");
            writer.write("}\n");
        } catch (IOException e) {
            System.err.println("Error writing configuration to file: " + fileName);
            System.exit(1);
        }
    }

}
