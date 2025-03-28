package ar.edu.itba.ss;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class VoterModel {
    private static final int GRID_SIZE = 50;
    private static final int MONTE_CARLO_STEPS = 100000;
    private static final int SAVE_INTERVAL = GRID_SIZE*GRID_SIZE;

    private static final double[] PROBABILITIES = {0.01, 0.1, 0.9};
    private static int[][] grid = new int[GRID_SIZE][GRID_SIZE];
    private static Random random = new Random();

    public static void main(String[] args) {
        for (double probability : PROBABILITIES) {
            initializeGrid();
            runMonteCarloSimulation(probability);
        }
    }

    private static void initializeGrid() {
        for (int i = 0; i < GRID_SIZE; i++) {
            for (int j = 0; j < GRID_SIZE; j++) {
                grid[i][j] = random.nextBoolean() ? 1 : -1; // Random opinion
            }
        }
    }

    private static void runMonteCarloSimulation(double probability) {
        String dirPath = "result/p_" + probability;
        File dir = new File(dirPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }

        for (int step = 1; step <= MONTE_CARLO_STEPS; step++) {
            int i = random.nextInt(GRID_SIZE);
            int j = random.nextInt(GRID_SIZE);

            int neighborSum = grid[(i - 1 + GRID_SIZE) % GRID_SIZE][j] + grid[(i + 1) % GRID_SIZE][j] +
                    grid[i][(j - 1 + GRID_SIZE) % GRID_SIZE] + grid[i][(j + 1) % GRID_SIZE];

            int majorityOpinion = (neighborSum >= 0) ? 1 : -1;

            if ((majorityOpinion != grid[i][j]) && random.nextDouble() < probability) {
                grid[i][j] *= -1; // Change opinion
            }

            // Guardar cada SAVE_INTERVAL iteraciones
            if (step % SAVE_INTERVAL == 0) {
                saveResults(probability, step, dirPath);
            }
        }
    }

    private static void saveResults(double probability, int iteration, String dirPath) {
        String fileName = String.format("%s/result_%.2f_%d.txt", dirPath, probability, iteration);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(fileName))) {
            for (int i = 0; i < GRID_SIZE; i++) {
                for (int j = 0; j < GRID_SIZE; j++) {
                    writer.write(grid[i][j] + " ");
                }
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
